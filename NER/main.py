import PyPDF2

def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return text

print(pdf_to_text('NER/PLAN 363 - Syllabus - Spring 2025 v3.pdf'))
