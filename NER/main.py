import PyPDF2
import re
import spacy
from spacy.tokens import DocBin

# Function to extract text from PDF
def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract dates and assignments
def extract_assignments(text):
    pattern = r"(\d{1,2}/\d{1,2})\s+(.*?(?:Quiz|Exam|Financial Plan|Paper|Due).*)"
    matches = re.findall(pattern, text)

    extracted_data = []
    for match in matches:
        date, assignment = match
        extracted_data.append((date, assignment))

    return extracted_data

# Function to format data for SpaCy training
def create_training_data(train_data, nlp):
    db = DocBin()
    for date, assignment in train_data:
        text = f"{date} {assignment}"
        doc = nlp.make_doc(text)
        ents = []

        start_date = 0
        end_date = len(date)
        start_assign = end_date + 1
        end_assign = start_assign + len(assignment)

        entities = [(start_date, end_date, "DATE"), (start_assign, end_assign, "ASSIGNMENT")]
        
        for start, end, label in entities:
            span = doc.char_span(start, end, label=label)
            if span is not None:
                ents.append(span)

        doc.ents = ents
        db.add(doc)
    return db

# Main execution
if __name__ == "__main__":
    pdf_path = "NER/PLAN 363 - Syllabus - Spring 2025 v3.pdf"
    
    print("Extracting text from PDF...")
    syllabus_text = pdf_to_text(pdf_path)

    print("Identifying assignments and dates...")
    assignments = extract_assignments(syllabus_text)

    for date, assignment in assignments:
        print(f"{date} -> {assignment}")

    print("Formatting data for SpaCy training...")
    nlp = spacy.blank("en")
    db = create_training_data(assignments, nlp)

    training_data_path = "./training_data.spacy"
    db.to_disk(training_data_path)

    print(f"Training data saved to {training_data_path}.")
