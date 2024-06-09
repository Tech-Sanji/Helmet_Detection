# Helmet_Detection
This project is focused on developing an interface and backend system to monitor and analyze video feeds from IP cameras, specifically to detect and classify motorcycle riders, helmets, and license plates. It encompasses several components, including a graphical user interface (GUI) for user interaction, image processing and object detection using deep learning models, and automated OCR (Optical Character Recognition) for extracting license plate information. The project is implemented primarily in Python, leveraging libraries such as OpenCV, Tkinter, and Pytorch, among others.

# Components
# 1. Interface (interface.py)
The interface.py script sets up a graphical user interface (GUI) using Tkinter. It allows the user to input an IP address for the camera, start and stop the main monitoring process, and configure default settings. Key functionalities include:

Dark Theme: Applied for better visual comfort.
IP Address Handling: Users can input an IP address, and the system checks camera availability.
Process Management: Start and stop the main process (main.py), and execute an additional script (txtapi.py) to handle OCR tasks.
Configuration: Save and read default IP settings from a configuration file.
Menu Options: Access different functionalities such as starting the API, setting default values, and exiting the application.
# 2. Main Monitoring Script (main.py)
The main.py script handles the core functionality of processing video streams from the specified IP address. It includes:

Video Capture: Connects to the IP camera and captures video frames.
Object Detection: Uses a YOLOv5 model to detect motorcycle riders, helmets, and license plates in the video frames.
Classification: Classifies whether detected heads are wearing helmets using a secondary deep learning model.
Output: Saves processed frames and relevant data (like detected rider images and number plates) to an output directory.
Alerts: Displays visual indicators on the video feed based on detection results.
# 3. Image Processing and Detection (my_functions.py)
The my_functions.py script contains helper functions for image classification and object detection:

YOLOv5 Model: Loads and uses a YOLOv5 model to detect objects in frames.
Image Classification: Uses a secondary model to classify whether a detected head is wearing a helmet.
Bounding Box Checking: Utility functions to check if one bounding box is inside another, which helps in associating detected heads with riders.
# 4. OCR and Data Management (txtapi.py)
The txtapi.py script is responsible for extracting and managing license plate information from saved images:

Image Preprocessing: Resizes and sharpens images to improve OCR accuracy.
OCR: Uses Tesseract OCR to extract text (license plates) from images.
Data Validation and Storage: Validates the extracted license plates and stores them in an Excel file with links for further information retrieval.
Continuous Processing: Monitors a specified directory for new images and processes them continuously until stopped.
# Key Features
User-Friendly Interface: Provides an intuitive way for users to interact with the system, input camera IP addresses, and control processes.
Real-Time Processing: Captures and processes video feeds in real-time, detecting and classifying objects dynamically.
Automated Data Management: Automatically extracts, validates, and stores license plate information, reducing manual effort.
Extensible Design: Modular code structure allows for easy addition of new functionalities and improvements.
# Libraries and Technologies
Python: Core programming language used for the entire project.
Tkinter: For creating the graphical user interface.
OpenCV: For video capture and image processing tasks.
Pytorch: For loading and using deep learning models (YOLOv5 and helmet classification model).
Tesseract: For OCR to extract text from images.
ConfigParser: For handling configuration files.
PSUtil: For process management.
Openpyxl: For handling Excel files.
# Usage Workflow
Launch the Interface: Run interface.py to open the GUI.
Input IP Address: Enter the IP address of the camera in the provided field.
Start Monitoring: Click the "Run" button to start the main monitoring script, which processes the video feed.
View Results: The processed video feed with detection overlays will be displayed.
Terminate Process: Use the "Terminate" button to stop the monitoring script.
Run OCR: Click the API menu option to start txtapi.py for processing saved images and extracting license plates.
Set Default Values: Use the "Default" menu option to set and save default IP addresses.
# Conclusion
This project provides a comprehensive solution for real-time monitoring and analysis of video feeds from IP cameras, focusing on the detection of motorcycle riders, helmets, and license plates. It integrates advanced deep learning techniques with a user-friendly interface, making it a powerful tool for applications such as traffic monitoring and law enforcement.
