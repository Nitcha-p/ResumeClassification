import os
import random
import shutil
import pdfplumber

DATASET_FOLDER = "PDF_Dataset"
WRONG_THRESHOLD = 0.3  # If the incorrect resumes exceed 30%, delete the folder

# Function to Check if a Resume Matches Its Category
def is_resume_wrong(resume_text, category):
    if category.lower() in resume_text.lower():  # Check if the Category Name Exists in the Resume
        return False  
    return True  

# Check Each Folder
folders_to_delete = []
for category in os.listdir(DATASET_FOLDER):
    category_path = os.path.join(DATASET_FOLDER, category)
    
    if os.path.isdir(category_path):
        resume_files = [f for f in os.listdir(category_path) if f.endswith(".pdf")]
        total_files = len(resume_files)

        # Adjust the Number of Files to Check
        if total_files <= 50:
            total_checked = total_files  # If Less Than 50 Files → Check All
        else:
            total_checked = min(30, int(0.3 * total_files))  # Check 30% or a Maximum of 30 Files
        
        wrong_count = 0

        # Randomly Select Resumes for Checking
        sampled_files = random.sample(resume_files, total_checked)

        for file in sampled_files:
            pdf_path = os.path.join(category_path, file)
            with pdfplumber.open(pdf_path) as pdf:
                text = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                if is_resume_wrong(text, category):
                    wrong_count += 1

        # Calculate the percentage of incorrect resumes
        error_percentage = wrong_count / total_checked
        print(f"Category: {category} - Wrong: {wrong_count}/{total_checked} ({error_percentage*100:.2f}%)")

        # If incorrect resumes exceed 30%, delete the folder
        if error_percentage > WRONG_THRESHOLD:
            folders_to_delete.append(category_path)

# Delete incorrect folders.
for folder in folders_to_delete:
    shutil.rmtree(folder)
    print(f"Deleted folder: {folder}")
