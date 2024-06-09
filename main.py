# this file name is main.py
import os
import cv2
import time
import argparse
from my_functions import is_bounding_box_inside, image_classify, object_detection
import pygame
import threading

# Initialize pygame mixer
#pygame.mixer.init()

# Function to play audio alert in a separate thread
# def play_sound_async(file_path):
#     print(f"Loading audio file: {file_path}")
#     pygame.mixer.music.load(file_path)
#     print("Audio file loaded successfully")
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

def main(ip_address):
    global main_process_pid  # Declare main_process_pid as global
    # Create the output folder if it doesn't exist
    output_folder = 'output_folder'  # Specify the output folder name
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set up video capture and output
    source = f'http://{ip_address}:8080/video'  # Use the provided IP address in the source URL
    cap = cv2.VideoCapture(source)
    frame_size = (800, 480)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    current_datetime = time.strftime("%Y%m%d_%H%M%S")  # Get the current date and time stamp
    output_video_path = os.path.join(output_folder, f'output_video/output_{current_datetime}.avi')  # Specify the output video path
    out = cv2.VideoWriter(output_video_path, fourcc, 20.0, frame_size)

    # Main loop
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, frame_size)
            original_frame = frame.copy()
            # Assuming object_detection function returns the processed frame and results
            frame, results = object_detection(frame)

            rider_list = []
            head_list = []
            number_list = []

            for result in results:
                x1, y1, x2, y2, conf, clas = result
                if clas == 0:
                    rider_list.append(result)
                elif clas == 1:
                    head_list.append(result)
                elif clas == 2:
                    number_list.append(result)

                for rdr in rider_list:
                    time_stamp = str(time.time())
                    x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                    for hd in head_list:
                        x1h, y1h, x2h, y2h, cnfh, clash = hd
                        if is_bounding_box_inside([x1r, y1r, x2r, y2r], [x1h, y1h, x2h, y2h]):
                            try:
                                head_img = original_frame[y1h:y2h, x1h:x2h]
                                helmet_present = image_classify(head_img)
                            except:
                                helmet_present[0] = None

                            if helmet_present[0] == True:  # if helmet present
                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 0), 1)
                                frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                            elif helmet_present[0] == None:  # If poor prediction, draw yellow rectangle and display uncertainty message
                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                                uncertainty_message = "Uncertain"
                                frame = cv2.putText(frame, uncertainty_message, (x1h, y1h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 255), 1, cv2.LINE_AA)
                                frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                            elif helmet_present[0] == False:  # if helmet absent
                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                                frame = cv2.putText(frame, f'{round(helmet_present[1], 1)}', (x1h, y1h + 40),
                                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                                try:
                                    cv2.imwrite(os.path.join(output_folder, f'riders_pictures/{time_stamp}.jpg'),
                                            original_frame[y1r:y2r, x1r:x2r])
                                    print('Rider saved')
                                except:
                                    print('could not save rider')

                                for num in number_list:
                                    x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                    if is_bounding_box_inside([x1r, y1r, x2r, y2r], [x1_num, y1_num, x2_num, y2_num]):
                                        try:
                                            num_img = original_frame[y1_num:y2_num, x1_num:x2_num]
                                            cv2.imwrite(os.path.join(output_folder, f'number_plates/{current_datetime}_{conf_num}.jpg'),
                                                        num_img)
                                            print("Number plate saved successfully")
                                        except:
                                            print('could not save number plate')

            # Display the processed frame
            cv2.imshow('Frame', frame)

            # Write to video file
            out.write(frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break

    # Release the capture and close all windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print('Execution completed')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.102", help="Camera IP address")
    args = parser.parse_args()
    main_process_pid = os.getpid()  # Get the PID of the current process
    main(args.ip)
