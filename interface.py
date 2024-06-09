import configparser
import tkinter as tk
from tkinter import Entry, messagebox, Menu
import subprocess
from tkinter import ttk
import cv2
import threading
import psutil

# Function to set dark theme
def set_dark_theme():
    style = ttk.Style()
    style.theme_use('clam')  # 'clam' is one of the built-in dark themes

# Function to read the default IP address from the configuration file
def read_default_ip():
    config = configparser.ConfigParser()
    config.read('config.ini')  # Replace 'config.ini' with your configuration file path
    return config.get('DEFAULT', 'default_ip', fallback='')

def is_camera_available(ip_address):
    try:
        # Try to access the camera using OpenCV
        cap = cv2.VideoCapture(f'http://{ip_address}:8080/video')
        if cap.isOpened():
            cap.release()
            return True
        else:
            return False
    except cv2.error as e:
        # Display a custom error message in a popup
        error_message = f"Error checking camera availability: {e}"
        messagebox.showerror("Camera Error", error_message)
        return False

def terminate_main():
    global main_process
    if main_process:
        try:
            # Send the 'q' key to terminate main.py
            main_process.terminate()
            messagebox.showinfo("Termination", "main.py terminated successfully.")
        except Exception as e:
            print(f"Error terminating main.py: {e}")
            messagebox.showerror("Error", f"Error terminating main.py: {e}")
        finally:
            # Clear the running IP address
            ip_status_label.config(text="")
    else:
        print("No main process running.")
        messagebox.showinfo("Info", "No main process running.")

def close_interface():
    global closed
    closed = True  # Set the flag to indicate that close_interface has been called

    # Check if main_process is already terminated
    if main_process and main_process.poll() is None:
        terminate_main()  # Terminate main.py only if not already terminated

    root.destroy()  # Close the Tkinter window

def start_main():
    global main_process
    ip_address = ip_entry.get()

    # Check if main_process is already running
    if main_process and main_process.poll() is None:
        print("Main process is already running.")
        messagebox.showinfo("Info", "Main process is already running.")
    else:
        # Update error label to indicate camera availability check is in progress
        error_label.config(text="Checking camera availability...")

        # Use Timer to check camera availability asynchronously
        camera_timer = threading.Timer(0, check_and_start_main, args=(ip_address,))
        camera_timer.start()

def check_and_start_main(ip_address):
    global main_process

    # Check if the IP address is empty and use a default value
    if not ip_address:
        default_ip = read_default_ip()
        ip_address = default_ip if is_camera_available(default_ip) else ''

    if is_camera_available(ip_address):
        # Start main.py if the camera is available
        main_process = subprocess.Popen(["python", "main.py", "--ip", ip_address])
        # Display the running IP address
        ip_status_label.config(text=f"IP Address: {ip_address}", fg="blue")
        # Clear the input field
        ip_entry.delete(0, tk.END)
        # Clear the error label
        error_label.config(text="")
    else:
        # Clear the error label
        error_label.config(text="Camera not available.")
        # Display an error message
        messagebox.showerror("Error", "Camera not available.")

def api_button_clicked():
    # Check if the 'txtapi.py' process is already running
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if 'python' in process.info['name'] and 'txtapi.py' in ' '.join(process.info['cmdline']):
            messagebox.showinfo("API Button", "API is already running!")
            return

    try:
        # Execute the txtapi.py file
        subprocess.Popen(["python", "C:\\Users\\admin\\Desktop\\Final_Year\\TxtApi\\txtapi.py"])
        messagebox.showinfo("API Button", "API button clicked! txtapi.py is running.")
    except Exception as e:
        messagebox.showerror("Error", f"Error running txtapi.py: {e}")

def open_default_window():
    default_window = tk.Toplevel(root)
    default_window.title("Default Settings")

    # Create an Entry widget for the default value input
    default_entry_label = tk.Label(default_window, text="Enter default value:")
    default_entry_label.pack(pady=5)
    default_entry = Entry(default_window)
    default_entry.pack(pady=5)

    # Create a "Set" button
    set_button = tk.Button(default_window, text="Set", command=lambda: set_default_value(default_entry.get(), default_window))
    set_button.pack(pady=10)

def set_default_value(value, window):
    # Save the default IP address to the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')  # Replace 'config.ini' with your configuration file path
    config.set('DEFAULT', 'default_ip', value)
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
    messagebox.showinfo("Default Value Set", f"Default value set to: {value}")
    window.destroy()

# Create Tkinter window
root = tk.Tk()
root.title("Interface")

# Set background color to black
root.configure(bg="Cadet Blue")

# Set dark theme
set_dark_theme()

# Set a consistent font style
font_style = ("Helvetica", 12)

# Create a Menubutton for the dropdown navigation
menu_button = tk.Menubutton(root, text="Menu", font=font_style, bg="lightblue")
menu_button.pack(pady=5)

# Create a Menu for the dropdown
menu = Menu(menu_button, tearoff=0, font=font_style, bg="lightblue")

# Add API option to the menu
menu.add_command(label="API", command=api_button_clicked)

# Add Default option to the menu
menu.add_command(label="Default", command=open_default_window)

# Add separator
menu.add_separator()

# Add Exit option
menu.add_command(label="Exit", command=root.destroy)

# Associate the Menu with the Menubutton
menu_button['menu'] = menu

# Create an Entry widget for IP address input
ip_label = tk.Label(root, text="Enter IP address:", font=font_style, bg="CadetBlue4", fg="white")
ip_label.pack(pady=5)
ip_entry = Entry(root, font=font_style)
ip_entry.pack(pady=5)

# Create a "Run" button
run_button = tk.Button(root, text="Run", command=start_main, font=font_style, bg="CadetBlue4", fg="white")
run_button.pack(pady=10)

# Create a "Terminate" button
terminate_button = tk.Button(root, text="Terminate", command=terminate_main, font=font_style, bg="CadetBlue4", fg="white")
terminate_button.pack(pady=5)

# Create a "Close" button
close_button = tk.Button(root, text="Close", command=close_interface, font=font_style, bg="CadetBlue4", fg="white")
close_button.pack(pady=5)

# Create an error label
error_label = tk.Label(root, text="", fg="red", font=font_style, bg="CadetBlue4")
error_label.pack(pady=5)

# Create a label to display the running IP address
ip_status_label = tk.Label(root, text="", font=font_style, bg="CadetBlue4", fg="white")
ip_status_label.pack(pady=5)

# Initialize main_process as None
main_process = None

# Initialize flag for close_interface
closed = False

# Start the Tkinter event loop
root.mainloop()
