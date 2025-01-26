# AI-Powered Workout and Diet Planner

This project is an AI-powered workout and diet planner that provides personalized fitness plans based on user input. It leverages the GPT-2 model for generating tailored workout and diet plans, integrated with a GUI built using Tkinter for an intuitive user experience. Additionally, the project includes a script for exercise counters using computer vision and Mediapipe.

## Features

- **Personalized Workout and Diet Plan**: Based on the user's goal (e.g., Muscle Gain, Weight Loss, Maintenance), age, weight, height, and dietary preferences, the system generates a detailed workout and diet plan.
- **BMI Calculation**: Automatically calculates the user's BMI and provides health status (Underweight, Normal weight, Overweight, Obese).
- **Exercise Counters**: Integrated exercise counter scripts for push-ups, squats, and biceps, utilizing computer vision techniques with Mediapipe.
- **User Progress Saving**: Saves user details and fitness progress in a text file for future reference.
- **GUI Interface**: User-friendly interface built with Tkinter for input collection and displaying the generated plans.

## Requirements

- Python 3.6 or later
- PyTorch
- transformers
- Mediapipe
- OpenCV
- Tkinter 

## Installation

1. Create a virtual environment and activate it:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2. Install the required dependencies:
    ```
    pip install torch torchvision torchaudio transformers mediapipe opencv-python
    ```

4. Download the pre-trained GPT-2 model and tokenizer:
    ```
    python -c "from transformers import GPT2LMHeadModel, GPT2Tokenizer; model = GPT2LMHeadModel.from_pretrained('gpt2'); tokenizer = GPT2Tokenizer.from_pretrained('gpt2')"
    ```

5. Run the application:
    ```
    python Bot.py
    ```

## Usage

- **Start the Application**: After running the application, a window will pop up where you can input your details, select your fitness goal, and choose your dietary preferences.
- **Generate a Plan**: After entering the required details, click "Generate Plan" to receive a personalized workout and diet plan.
- **Exercise Counters**: You can also use the exercise counter feature by selecting a script (Biceps, Push-Up, Squat) and running it.

## Acknowledgements

- GPT-2 model from Hugging Face
- Mediapipe for pose detection
- OpenCV for video processing
- Tkinter for GUI creation

