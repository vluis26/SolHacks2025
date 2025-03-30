# import spacy

# nlp = spacy.load("/Users/kevingomez/solhacks/SolHacks2025/assignment_model")

# # Use the trained model to predict entities on new text
# text = "The final paper is due on April 30, 2026."
# doc = nlp(text)

# # Print the detected entities
# for ent in doc.ents:
#     print(ent.text, ent.label_)

import dateparser

def extract_dates(text):
    dates = []
    # Try to parse potential dates
    for date in dateparser.search.search_dates(text):
        dates.append(date[0])  # Extract the date
    return dates

import re

def extract_assignments(text):
    pattern = r"(midterm|quiz|exam|paper|assignment|due|test)[\s\S]+?(?=\d{1,2}[\/\-\.\s]?\d{1,2}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s?\d{1,2})"
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    return matches

def pair_assignments_and_dates(assignments, dates):
    paired_data = []
    
    for assignment in assignments:
        # Look for the closest date to the assignment
        closest_date = min(dates, key=lambda d: abs(d - assignment[0]))  # Find closest date
        paired_data.append((assignment, closest_date))
        
    return paired_data

text = """
The midterm exam is on February 3, 2023. The quiz is due March 15. 
The final exam will be held on May 5, 2023.
"""

dates = extract_dates(text)
assignments = extract_assignments(text)

paired_data = pair_assignments_and_dates(assignments, dates)
print(paired_data)