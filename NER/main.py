import PyPDF2
import re
import spacy
from spacy.tokens import DocBin

# Function to extract text from PDF
# def pdf_to_text(pdf_path):
#     text = ""
#     with open(pdf_path, 'rb') as pdf_file:
#         reader = PyPDF2.PdfReader(pdf_file)
#         for page in reader.pages:
#             text += page.extract_text() + "\n"
#     return text

def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    # Clean up the extracted text
    text = preprocess_text(text)
    
    return text

def preprocess_text(text):
    # Step 1: Remove any excessive line breaks or tabular breaks (PDFs often insert '\n' between text)
    text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space

    # Step 2: Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/tabs with a single space

    # Step 3: Remove spaces before or after punctuation marks (if needed)
    text = re.sub(r'\s([?.!,¿])', r'\1', text)  # Remove space before punctuation

    # Step 4: Handle any other common formatting errors, such as broken words or columns
    # For example, if text like "Well -Being" is split, we can fix that
    text = re.sub(r'(\w)- (\w)', r'\1\2', text)  # Remove space between words split by a hyphen
    
    # Step 5: Return the cleaned-up text
    return text


# Function to extract class title 
def extract_class_title(text):
    pattern = r'\b[A-Za-z]{3,4}\s?\d{3,}\b'
    matches = re.findall(pattern, text, re.IGNORECASE)

    extracted_data = []
    for data in matches:
        extracted_data.append(data)
    return extracted_data

# Function to extract class location
def extract_class_location(text):
    pattern = r'\b(?:class(?:room| location)|lecture hall)\s*:\s*([A-Za-z0-9\s\-]+)'
    match = re.findall(pattern, text, re.IGNORECASE)
    split_txt = match[0].split()
    if split_txt[2].strip()[0].upper() == 'H':
        return " ".join(split_txt[0:3])
    if split_txt[2][0] != 'H' or split_txt[2][0] != 'h':
        return " ".join(split_txt[0:2])
    else:
        return " ".join(split_txt[0:3])

# Creating Training Data
train_data = [
    # Format: (text, {"entities": [(start, end, label)]})
    ("Midterms are on Feb 3, Mar 3, and April 7.",
     {"entities": [
         (17, 23, "DATE"),   # Feb 3
         (25, 30, "DATE"),   # Mar 3
         (36, 44, "DATE"),   # April 7
         (0, 8, "ASSIGNMENT")  # Midterms
     ]}),
]

train_data += [
    ("Th. 3/6 NO NEW READING  Argument Analysis Exercise #2",
     {"entities": [
         (4, 7, "DATE"),  # 3/6
         (26, 60, "ASSIGNMENT")  # Argument Analysis Exercise #2
     ]}),
]

train_data += [
    (
        "Week 6 Well -Being Day 2/10 NO CLASS Quiz #1 2/12 Quiz #1",
        {
            "entities": [
                (30, 35, "DATE"),       # 2/10
                (60, 65, "DATE"),       # 2/12
                (66, 74, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]



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
    print(syllabus_text)


    # print("Formatting data for SpaCy training...")
    # nlp = spacy.blank("en")
    # db = create_training_data(assignments, nlp)

    # training_data_path = "./training_data.spacy"
    # db.to_disk(training_data_path)

    # print(f"Training data saved to {training_data_path}.")
