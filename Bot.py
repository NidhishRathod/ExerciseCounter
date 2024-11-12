import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess  # Added for running external scripts

# Load pre-trained GPT-2 model and tokenizer from Hugging Face
model_name = "gpt2"  # You can use different versions like "gpt2-medium" or "gpt2-large" depending on the available resources
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Ensure the model is in evaluation mode
model.eval()

# Function to generate a structured workout and diet plan based on the user's goal
def get_personalized_plan(name, age, weight, height, goal, vegetarian, gender):
    # Goal-specific templates
    goal_templates = {
        "Muscle Gain": """Create a muscle gain workout plan and a high-protein diet plan. The workout plan should include exercises for the chest, back, shoulders, legs, and arms, with sets and reps for each day. The diet plan should focus on high-protein meals like chicken, eggs, tofu, and quinoa, with portion sizes and snack ideas. Also, include rest day suggestions. All of this should be in a structured tabular format.""",
        "Weight Loss": """Create a weight loss workout plan with a focus on cardio, HIIT, and calorie-burning exercises. Include exercises like running, cycling, and bodyweight exercises, along with sets and reps. The diet plan should be low-calorie with healthy foods like salads, fruits, and lean protein, including meal portion sizes and snack ideas. All of this should be in a structured tabular format.""",
        "Maintain": """Create a balanced workout plan with both strength training and cardio exercises for overall fitness. Include exercises like squats, push-ups, and running. The diet plan should be balanced with proteins, carbs, and healthy fats, with meal portion sizes and snack ideas. Include rest days and recovery tips. All of this should be in a structured tabular format."""
    }

    # Construct the prompt
    prompt = f"""
    Create a highly detailed and structured {goal.lower()} workout and diet plan for the following user:
    Name: {name}
    Age: {age}
    Weight: {weight}kg
    Height: {height}m
    Fitness Goal: {goal}
    Vegetarian: {'Yes' if vegetarian else 'No'}
    Gender: {gender}

    {goal_templates[goal]}
    """

    # Tokenize the prompt and generate a response using greedy decoding (no randomness)
    inputs = tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)

    # Generate text using the GPT-2 model with sampling
    with torch.no_grad():
        outputs = model.generate(inputs,
                                 max_length=600,    # Increase max_length if necessary
                                 num_return_sequences=1,
                                 do_sample=True,    # Enable sampling for more varied responses
                                 top_k=50,          # Top-k sampling for diversity
                                 top_p=0.95,        # Nucleus sampling for better results
                                 no_repeat_ngram_size=2,  # Prevent repeating n-grams
                                 temperature=0.7)   # Adjust temperature for randomness

    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text


# Function to calculate BMI
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 24.9:
        status = "Normal weight"
    elif 25 <= bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obese"
    return bmi, status


# Function to save user progress to file
def save_progress(name, goal, weight, height):
    with open("user_progress.txt", "a") as file:
        file.write(f"Name: {name}, Goal: {goal}, Weight: {weight}kg, Height: {height}m\n")


# Function to open Exercises.py file in the same directory
def open_exercises_file():
    try:
        # Running the Exercises.py script using subprocess
        subprocess.run(["python", "Exercises.py"], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open Exercises.py: {str(e)}")


# Main function to handle user input and generate plans
def generate_plan():
    try:
        # Collect user input from the UI
        name = name_entry.get()
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        goal_input = goal_combobox.get()
        is_vegetarian = vegetarian_var.get()
        gender = gender_var.get()

        # Validate inputs
        if age <= 0 or weight <= 0 or height <= 0:
            messagebox.showerror("Error", "Please enter valid positive values.")
            return

        # Calculate BMI and determine status
        bmi, status = calculate_bmi(weight, height)

        # Generate dynamic workout and diet plans
        plan_text.delete(1.0, tk.END)
        plan_text.insert(tk.END, f"Hello {name}! Here's your personalized plan:\n\n")
        plan_text.insert(tk.END, f"Your BMI: {bmi:.2f} ({status})\n\n")

        # Get personalized workout and diet plan using the free GPT-2 model
        personalized_plan = get_personalized_plan(name, age, weight, height, goal_input, is_vegetarian, gender)

        if personalized_plan:
            plan_text.insert(tk.END, personalized_plan)

        # Save progress to file
        save_progress(name, goal_input, weight, height)

        # Show "Open Exercises" button after plan generation
        open_exercises_button.grid(row=10, column=0, pady=10, sticky="ew")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# GUI Setup
root = tk.Tk()
root.title("AI-Powered Workout and Diet Planner")

frame = tk.Frame(root, bg="#F1FAEE", padx=20, pady=20)
frame.pack(padx=20, pady=20)

# Name input
tk.Label(frame, text="Name:", font=("Arial", 12), bg="#F1FAEE").grid(row=0, column=0, sticky="w")
name_entry = tk.Entry(frame, font=("Arial", 12))
name_entry.grid(row=0, column=1)

# Age input
tk.Label(frame, text="Age:", font=("Arial", 12), bg="#F1FAEE").grid(row=1, column=0, sticky="w")
age_entry = tk.Entry(frame, font=("Arial", 12))
age_entry.grid(row=1, column=1)

# Weight input
tk.Label(frame, text="Weight (kg):", font=("Arial", 12), bg="#F1FAEE").grid(row=2, column=0, sticky="w")
weight_entry = tk.Entry(frame, font=("Arial", 12))
weight_entry.grid(row=2, column=1)

# Height input
tk.Label(frame, text="Height (m):", font=("Arial", 12), bg="#F1FAEE").grid(row=3, column=0, sticky="w")
height_entry = tk.Entry(frame, font=("Arial", 12))
height_entry.grid(row=3, column=1)

# Goal dropdown (combobox)
tk.Label(frame, text="Fitness Goal:", font=("Arial", 12), bg="#F1FAEE").grid(row=4, column=0, sticky="w")
goal_combobox = ttk.Combobox(frame, values=["Muscle Gain", "Weight Loss", "Maintain"], font=("Arial", 12))
goal_combobox.grid(row=4, column=1)

# Vegetarian checkbox
vegetarian_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Vegetarian", variable=vegetarian_var, font=("Arial", 12), bg="#F1FAEE").grid(row=5,
                                                                                                         column=1,
                                                                                                         sticky="w")

# Gender radio buttons
gender_var = tk.StringVar(value="Male")
tk.Label(frame, text="Gender:", font=("Arial", 12), bg="#F1FAEE").grid(row=6, column=0, sticky="w")
tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male", font=("Arial", 12), bg="#F1FAEE").grid(row=6,
                                                                                                          column=1,
                                                                                                          sticky="w")
tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female", font=("Arial", 12), bg="#F1FAEE").grid(row=7,
                                                                                                                 column=1,
                                                                                                                 sticky="w")

# Generate plan button
generate_button = tk.Button(frame, text="Generate Plan", font=("Arial", 14), command=generate_plan)
generate_button.grid(row=8, columnspan=2, pady=20)

# Text box to display the generated plan
plan_text = tk.Text(frame, height=12, width=40, font=("Arial", 12))
plan_text.grid(row=9, columnspan=2)

# Button to open the Exercises.py file
open_exercises_button = tk.Button(frame, text="Exercises Counter", font=("Arial", 12), command=open_exercises_file)

# Start the Tkinter GUI loop
root.mainloop()
