import tkinter as tk
import subprocess
import os

# Path to the Python executable in your virtual environment
python_executable = r"C:\Users\Predator\PycharmProjects\pythonProject1\Bot\venv\Scripts\python.exe"

# Function to run a selected exercise script
def run_script(script_name):
    # Check if the script file exists
    if os.path.exists(script_name):
        # Use the virtual environment's Python executable to run the script
        subprocess.run([python_executable, script_name])
    else:
        print(f"Error: {script_name} not found.")

# Create the main Tkinter window
root = tk.Tk()
root.title("Exercises Counter GUI")

# Set window size and position
root.geometry("300x200")

# Create a label with instructions
label = tk.Label(root, text="Select an Exercise to Start:", font=("Helvetica", 14))
label.pack(pady=20)

# Create buttons for each exercise
bicep_button = tk.Button(root, text="Bicep Counter", command=lambda: run_script("BicepsCounter.py"), width=20)
bicep_button.pack(pady=5)

pushup_button = tk.Button(root, text="Push-Up Counter", command=lambda: run_script("PushupsCounter.py"), width=20)
pushup_button.pack(pady=5)

squat_button = tk.Button(root, text="Squat Counter", command=lambda: run_script("SquatsCounter.py"), width=20)
squat_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
