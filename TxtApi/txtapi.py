import os
import cv2
import pytesseract
import openpyxl
import shutil
import time
import re

def resize_and_overwrite(image_path, scale_factor=3.0, sharpen_strength=2.5):
    # Read the original image
    original_image = cv2.imread(image_path)

    if original_image is None:
        print(f"Error reading the image: {image_path}")
        return None

    # Calculate the new dimensions based on the scale factor
    new_height = int(original_image.shape[0] * scale_factor)
    new_width = int(original_image.shape[1] * scale_factor)

    # Resize the image using Bicubic interpolation
    resized_image = cv2.resize(original_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    # Apply Unsharp Mask (USM) for sharpening
    blurred = cv2.GaussianBlur(resized_image, (0, 0), scale_factor)
    sharpened = cv2.addWeighted(resized_image, 1.0 + sharpen_strength, blurred, -sharpen_strength, 0)

    # Overwrite the original image with the resized and sharpened one
    cv2.imwrite(image_path, sharpened)

    return image_path

def process_images_continuously(folder_path, workbook, sheet, stop_processing):
    while not stop_processing:
        # Get the list of image files in the folder
        image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        print(f"Found {len(image_files)} image(s) in the folder.")

        if not image_files:
            print("No more images to process. Terminating...")
            stop_processing = True
            break

        for image_file in image_files:
            if stop_processing:
                break

            image_path = os.path.join(folder_path, image_file)

            # Resize and overwrite the original image
            resized_image_path = resize_and_overwrite(image_path, scale_factor=3.0)

            if resized_image_path is None:
                continue

            try:
                # Use pytesseract for OCR on the resized image
                ocr_result = pytesseract.image_to_string(resized_image_path, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

                # Extract number plate from OCR result
                license_plate = extract_number_plate(ocr_result)

                if license_plate:
                    print("License Plate:", license_plate)

                    # Validate the license plate
                    if is_valid_license_plate(license_plate):
                        # Save the license plate in the Excel sheet
                        link = f"https://www.carinfo.app/rc-details/{license_plate}"
                        sheet.append([license_plate, link])
                        workbook.save('number_plate_links.xlsx')

                        # Move the original image to the 'success' folder
                        success_folder = os.path.join(folder_path, 'success')
                        os.makedirs(success_folder, exist_ok=True)
                        shutil.move(resized_image_path, os.path.join(success_folder, image_file))

                        print(f"Link saved for number plate {license_plate} from image {image_file}")
                    else:
                        print("Invalid license plate detected")

                        # Move the original image to the 'Invalid' folder
                        invalid_folder = os.path.join(folder_path, 'Invalid')
                        os.makedirs(invalid_folder, exist_ok=True)
                        shutil.move(resized_image_path, os.path.join(invalid_folder, image_file))
                else:
                    print("No number plate detected")

                    # Move the original image to the 'Trash' folder
                    trash_folder = os.path.join(folder_path, 'Trash')
                    os.makedirs(trash_folder, exist_ok=True)
                    shutil.move(resized_image_path, os.path.join(trash_folder, image_file))

            except Exception as e:
                print(f"Error during OCR: {e}")

        # Wait before checking for new images again
        time.sleep(0)

def extract_number_plate(ocr_result):
    license_plate = ""
    detected_numbers = []

    for text in ocr_result.split():
        if text.isdigit():
            detected_numbers.append(int(text))
        license_plate += text

    license_plate = license_plate.replace(" ", "")

    return license_plate if detected_numbers else None

def is_valid_license_plate(license_plate):
    """
    Checks if a license plate is valid.

    Args:
    license_plate: The license plate to check.

    Returns:
    True if the license plate is valid, False otherwise.
    """

    # Check if the license plate is the correct length.
    if len(license_plate) != 7:
        return False

    # Check if the license plate starts with two letters.
    if not re.match(r'^[A-Z]{2}', license_plate):
        return False

    # Check if the license plate has three numbers in the middle.
    if not re.match(r'^[A-Z]{2}\d{3}', license_plate):
        return False

    # Check if the license plate ends with two letters.
    if not re.match(r'^[A-Z]{2}\d{3}[A-Z]{2}$', license_plate):
        return False

    # The license plate is valid.
    return True

# Initialize flag to signal the image processing to terminate
stop_processing = False

# Specify the folder path
folder_path = 'C:\\Users\\admin\\Desktop\\Final_Year\\output_folder\\number_plates'

# Create or load the Excel workbook
try:
    workbook = openpyxl.load_workbook('number_plate_links.xlsx')
except FileNotFoundError:
    workbook = openpyxl.Workbook()

# Select the active worksheet
sheet = workbook.active

# Main loop for continuous image processing
try:
    print("Starting image processing...")
    process_images_continuously(folder_path, workbook, sheet, stop_processing)
except Exception as e:
    print(f"Error processing images: {e}")
finally:
    print("Image processing terminated.")
