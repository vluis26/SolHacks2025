import spacy
import NER.main as tool
from dateparser import parse

nlp = spacy.load("/Users/kevingomez/solhacks/SolHacks2025/assignment_model")
pdf_path = "backend/NER/PLAN 363 - Syllabus - Spring 2025 v3.pdf"


syllabus_text = tool.pdf_to_text(pdf_path)
# print(syllabus_text)
# Use the trained model to predict entities on new text
text = "The final paper is due on April 30, 2026."
doc = nlp(text)


# Print the detected entities
for ent in doc.ents:
    print(ent.text, ent.label_)
