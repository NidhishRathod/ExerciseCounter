import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Mediapipe initialization
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Function to calculate the angle
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Create the Tkinter window for file selection
def select_video_source():
    def open_video_source():
        choice = video_source_var.get()

        if choice == 'Webcam':
            cap = cv2.VideoCapture(0)
        elif choice == 'Video File':
            video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
            cap = cv2.VideoCapture(video_path)

        if cap.isOpened():
            process_video_feed(cap)
        else:
            print("Error: Unable to open video source.")

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Select Video Source")

    # Create a label for instructions
    label = tk.Label(root, text="Select Video Source:")
    label.pack(pady=10)

    # Create a variable for selecting between webcam and file
    video_source_var = tk.StringVar(value="Webcam")

    # Create radio buttons for video source selection
    webcam_radio = tk.Radiobutton(root, text="Webcam", variable=video_source_var, value="Webcam")
    webcam_radio.pack()

    file_radio = tk.Radiobutton(root, text="Video File", variable=video_source_var, value="Video File")
    file_radio.pack()

    # Create an "Open" button
    open_button = tk.Button(root, text="Open", command=open_video_source)
    open_button.pack(pady=20)

    root.mainloop()

# Process video feed for webcam or file
def process_video_feed(cap):
    # Curl counter variables for both hands
    counter_left = 0
    counter_right = 0
    stage_left = None
    stage_right = None

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            # Resize the video frame to match GUI size (640x480)
            frame = cv2.resize(frame, (640, 480))

            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = pose.process(image)

            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                # Left hand coordinates
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                # Right hand coordinates
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                # Calculate angles
                angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)
                angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)

                # Visualize angles
                cv2.putText(image, f"Left: {int(angle_left)}",
                            tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.putText(image, f"Right: {int(angle_right)}",
                            tuple(np.multiply(right_elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Left curl counter logic
                if angle_left > 160:
                    stage_left = "down"
                if angle_left < 30 and stage_left == 'down':
                    stage_left = "up"
                    counter_left += 1
                    print(f"Left Counter: {counter_left}")

                # Right curl counter logic
                if angle_right > 160:
                    stage_right = "down"
                if angle_right < 30 and stage_right == 'down':
                    stage_right = "up"
                    counter_right += 1
                    print(f"Right Counter: {counter_right}")

            except:
                pass

            # Render curl counter for both hands
            # Setup status box with adjusted width
            cv2.rectangle(image, (0, 0), (350, 73), (245, 117, 16), -1)  # Increased width to 350

            # Left rep data
            cv2.putText(image, 'LEFT REPS', (15, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_left),
                        (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Right rep data
            cv2.putText(image, 'RIGHT REPS', (115, 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_right),
                        (110, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Call the GUI function to start the video source selection
select_video_source()
