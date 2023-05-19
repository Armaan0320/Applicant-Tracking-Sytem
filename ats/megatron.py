import os   
import glob
import PyPDF2
import docx2txt
import docx
import textract
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import csv
from datetime import datetime
import re


# Create a dictionary of predetermined skills
SKILLS = {
    'python': ['python', 'PYTHON'],
    'ml': ['machine learning', 'ml', 'ML'],
    'ai': ['artificial intelligence', 'ai', 'AI'],
    'ds': ['data science', 'ds', 'DS'],
    'sql': ['sql', 'SQL', 'mysql', 'MYSQL'],
    'r': ['r', 'R'],
    'dsa': ['DATA STRUCTURE AND ALGORITHM', 'data structure and algrorithm', 'DSA'],
    'php': ['PHP', 'php'],
    'java': ['JAVA', 'java'],
    'javascript': ['JAVASCRIPT', 'javascript', 'nodejs'],
    'html': ['HTML', 'html', 'Hyper text markup language'],
    'css': ['CSS', 'css', 'cascaded style sheet'],
    'hadoop': ['HADOOP', 'hadoop', 'bigdata', 'BIGDATA', 'hdfs', 'HDFS', 'mapreduce', 'MAPREDUCE', 'hive', 'HIVE', 'pig', 'PIG', 'mahoot', 'MAHOOT', 'hbase', 'HBASE'],
    'problem_solving': ['problem solving'],
    'data_acquisition': ['daav', 'DAAV'],
    'critical_thinking': ['critical thinking'],
    'teamwork': ['teamwork'],
    'leadership': ['leadership'],
    'reasoning_skills': ['reasoning skills'],
    'software_development': ['software development'],
    'computer_networks': ['cn', 'CN']
}

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

def extract_email(filepath):
    """
    Extract email from the applicant file.
    """
    text = extract_text(filepath)
    # Regular expression pattern to match email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    if matches:
        return matches[0]
    else:
        return ""

def get_current_date():
    '''Get the current date in the desired format.'''
    today=datetime.now()
    return today.strftime("%Y-%m-%d")

RESULTS_FOLDER = 'C:/Users/Administrator/Desktop/ats/matched_candidates'

def save_results_to_csv(csv_filename, results):
    csv_filepath = os.path.join(RESULTS_FOLDER, csv_filename)
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(csv_filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['File Name', 'Email', 'Matched Skills'])
        for result in results:
            filename, email, skills_matched = result[:3]  # Limit unpacking to three values
            writer.writerow([filename, email, ', '.join(skills_matched)])
    print(f"Results saved to {csv_filepath}")

def search_applicants(skills_needed, threshold):
    skills_needed = skills_entry.get().split(",")
    threshold = float(threshold_entry.get())
    matched_skills = []
    num_matched_skills = 0
    for filename in os.listdir('C:/Users/Administrator/Desktop/ats/resumes'):
        filepath = os.path.join('resumes', filename)
        text = extract_text(filepath)
        skills_matched = [skill for skill in skills_needed if skill.lower() in text]
        
        if len(skills_matched) / len(skills_needed) >= threshold:
            num_matched_skills += len(skills_matched)
            matched_skills.append((filename, extract_email(filepath), skills_matched))
            
    return matched_skills, num_matched_skills

def find_candidates():
    matched_skills, num_matched_skills = search_applicants()
    if len(matched_skills) == 0:
        messagebox.showinfo("No matches found", "There are no candidates matching the specified skills.")
        return

    # Generate the current date for the CSV filename
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create the filename with the current date
    csv_filename = f"{current_date}.csv"

    # Save the matching files to the CSV file
    save_results_to_csv(csv_filename, matched_skills)

    # Display a message box with the confirmation
    messagebox.showinfo("Results", f"{len(matched_skills)} candidates found. The results have been saved to '{csv_filename}'.")

def display_matching_files(matched_skills):
    # Create a new GUI root for displaying the matching files
    results_root = tk.Toplevel(root)
    results_root.title("Matching Files")
    results_root.geometry("600x400")

    # Results text box
    results_text = tk.Text(results_root)
    results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Display the results in the text box
    results_text.insert(tk.END, "Matching files:\n")
    for filename, email, matched_skills in matched_skills:
        results_text.insert(tk.END, f"Filename: {filename}\n")
        results_text.insert(tk.END, f"Email: {email}\n")
        results_text.insert(tk.END, f"Matched Skills: {', '.join(matched_skills)}\n")
        results_text.insert(tk.END, "\n")

    # Disable the text box to make it uneditable
    results_text.configure(state="disabled")

def find_candidates():
    skills_needed = skills_entry.get().split(",")
    threshold = float(threshold_entry.get())
    matched_skills, num_matched_skills = search_applicants(skills_needed, threshold)
    if len(matched_skills) == 0:
        messagebox.showinfo("No matches found", "There are no candidates matching the specified skills.")
        return

    # Generate the current date for the CSV filename
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create the filename with the current date
    csv_filename = f"{current_date}.csv"

    # Save the matching files to the CSV file
    save_results_to_csv(csv_filename, matched_skills)

    # Display a message box with the confirmation
    messagebox.showinfo("Results", f"{len(matched_skills)} candidates found. The results have been saved to '{csv_filename}'.")

    # Display the matching files in a separate window
    display_matching_files(matched_skills)


# Create the main GUI root
root = tk.Tk()
root.title("Skill Scout")
root.geometry("720x400")
image = Image.open("templates/bg1.jpg")
photo = ImageTk.PhotoImage(image)
bg_label = tk.Label(root, image=photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Add label for the title
l1 = Label(root , text='Skill Scout the "Applicant Tracking System"' , fg='#ffffff',bg='#292826',font=("Times New Roman", 16), justify=CENTER)
l1.pack(pady=20)

# Skills label and entry
skills_label = tk.Label(root, text="Skills Needed (comma-separated):")
skills_label.pack(padx=10, pady=10)
skills_entry = tk.Entry(root)
skills_entry.pack()

# Threshold label and entry
threshold_label = tk.Label(root, text="Threshold (0 to 1):")
threshold_label.pack(padx=10, pady=10)
threshold_entry = tk.Entry(root)
threshold_entry.pack()


# Search button
search_button = tk.Button(root, text="Find Candidates", command=find_candidates)
search_button.pack(padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
