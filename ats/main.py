'''GUI working
prints matched skills in a secondary GUI window'''

import os
import docx2txt
import PyPDF2
import textract
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
from tkinter import *
from PIL import Image, ImageTk

def extract_text(filepath):
    """
    Extract text from a file using its file extension.
    """
    extension = os.path.splitext(filepath)[1][1:].lower()
    if extension == 'txt':
        with open(filepath, 'r') as f:
            text = f.read()
    elif extension == 'docx':
        text = docx2txt.process(filepath)
    elif extension == 'pdf':
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f, strict=False)
            pages = [reader.pages[i].extract_text() for i in range(len(reader.pages))]

            text = '\n'.join(pages)
    else:
        text = textract.process(filepath).decode('utf-8')

    return text.lower()


def search_applicants(skills_needed, threshold):
    """
    Search for applicants whose files contain the given skills.
    """
    matching_files = []
    for filename in os.listdir('resumes'):
        filepath = os.path.join('resumes', filename)
        text = extract_text(filepath)
        skills_matched = [skill for skill in skills_needed if skill.lower() in text]
        if len(skills_matched) / len(skills_needed) >= threshold:
            matching_files.append((filename, skills_matched))

    return matching_files


def find_candidates():
    skills_needed = skills_input.get().split(",")
    threshold = float(threshold_input.get())
    matching_files = search_applicants(skills_needed, threshold)
    if len(matching_files) == 0:
        messagebox.showinfo("No matches found", "There are no candidates matching the specified skills.")
        return

    # Save the results to a CSV file
    with open('matching_files.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Filename", "Skills matched"])
        for filename, skills_matched in matching_files:
            writer.writerow([filename, ', '.join(skills_matched)])

    messagebox.showinfo("Results", f"{len(matching_files)} candidates found. The results have been saved to 'matching_files.csv'.")

    # Create a new window to display the results
    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.geometry("500x400")

    # Create a label to display the number of matching candidates
    result_label = tk.Label(result_window, text=f"{len(matching_files)} candidates found.")
    result_label.pack(padx=10, pady=10)

    # Create a text widget to display the matching files
    result_text = tk.Text(result_window)
    result_text.pack(expand=True, fill="both", padx=10, pady=10)

    # Add the matching files to the text widget
    for filename, skills_matched in matching_files:
        result_text.insert("end", f"{filename}\n")
        result_text.insert("end", f"Skills matched: {', '.join(skills_matched)}\n\n")

    result_text.configure(state="disabled")


# Create the main GUI window
root = tk.Tk()
root.title("Candidate Search")
root.geometry("720x400")
image = Image.open("templates/bg4.jpg")
photo = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image=photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# Add label for the title
l1 = Label(root , text='Skill Scout the "Applicant Tracking System"' , fg='#ffffff',bg='#292826',font=("Times New Roman", 16), justify=CENTER)
l1.pack(pady=20)

# Skills input
skills_label = tk.Label(root, text="Enter skills needed (comma-separated):")
skills_label.pack(padx=10, pady=10)

skills_input = tk.Entry(root)
skills_input.pack(padx=10, pady=10)

# Threshold input
threshold_label = tk.Label(root, text="Threshold (0-1):")
threshold_label.pack(padx=10, pady=10)

threshold_input = tk.Entry(root)
threshold_input.pack(padx=10, pady=10)

# Find candidates button
find_candidates_button = tk.Button(root, text="Find Candidates", command=find_candidates)
find_candidates_button.pack(padx=10, pady=10)


root.mainloop()

