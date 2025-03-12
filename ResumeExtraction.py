import os
import pandas as pd
import pdfplumber

# Define the main dataset folder
DATASET_FOLDER = "PDF_Dataset"
OUTPUT_FILE = "Extracted_Resumes.xlsx"

def extract_text_from_pdf(pdf_path):
    """Extract text from the first page of a PDF file using pdfplumber, ensuring spaces between words."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            if pdf.pages:
                text = pdf.pages[0].extract_text(x_tolerance=2, y_tolerance=2)
                if text:
                    return " ".join(text.split())  # Ensure spaces between words
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")
    return ""

def process_pdfs():
    """Iterate through folders, extract text from PDFs, and save to Excel."""
    data = []
    
    for category in os.listdir(DATASET_FOLDER):
        category_path = os.path.join(DATASET_FOLDER, category)
        
        if os.path.isdir(category_path):  # Ensure it's a folder
            for file in os.listdir(category_path):
                if file.endswith(".pdf"):
                    pdf_path = os.path.join(category_path, file)
                    print(f"Processing: {pdf_path}")  # Show progress
                    extracted_text = extract_text_from_pdf(pdf_path)
                    
                    if extracted_text:
                        data.append({"Category": category, "Extracted Text": extracted_text})
    
    # Save to Excel
    df = pd.DataFrame(data)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Extraction complete! Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_pdfs()