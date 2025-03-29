import random
import PyPDF2
import re
from spacy.tokens import DocBin
from spacy.training.example import Example
from spacy.training import offsets_to_biluo_tags


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
    # Remove any excessive line breaks or tabular breaks (PDFs often insert '\n' between text)
    text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space

    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/tabs with a single space

    # Remove spaces before or after punctuation marks (if needed)
    text = re.sub(r'\s([?.!,¿])', r'\1', text)  # Remove space before punctuation

    # Handle any other common formatting errors, such as broken words or columns
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
         (16, 21, "DATE"),   # Feb 3
         (23, 28, "DATE"),   # Mar 3
         (34, 41, "DATE"),   # April 7
         (0, 8, "ASSIGNMENT")  # Midterms
     ]}),
]

train_data += [
    ("Th. 3/6 NO NEW READING  Argument Analysis Exercise #2",
     {"entities": [
         (4, 7, "DATE"),  # 3/6
         (24, 53, "ASSIGNMENT")  # Argument Analysis Exercise #2
     ]}),
]

train_data += [
    (
        "Week 6 Well -Being Day 2/10 NO CLASS Quiz #1 2/12 Quiz #1",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 6 Well -Being Day 1/07 NO CLASS Quiz #1 3/22 Quiz #6",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 7 Well -Being Day 2/10 NO CLASS Quiz #1 2/12 Quiz #1",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Well -Being Day 9/20 NO CLASS Quiz #1 8/02 Quiz #5",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 3 Well -Being Day 3/11 NO CLASS Quiz #1 5/17 Quiz #2",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 1 Well -Being Day 3/10 NO CLASS Quiz #1 3/02 Quiz #5",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 6 Well -Being Day 2/24 NO CLASS Quiz #1 3/22 Quiz #5",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Well -Being Day 2/10 NO CLASS Quiz #1 2/12 Quiz #1",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 2 Well -Being Day 4/10 NO CLASS Quiz #1 9/12 Quiz #8",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 1 Well -Being Day 4/10 NO CLASS Quiz #1 4/12 Quiz #5",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 2 Well -Being Day 8/10 NO CLASS Quiz #1 8/02 Quiz #5",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 9 Well -Being Day 2/15 NO CLASS Quiz #1 2/17 Quiz #3",
        {
            "entities": [
                (23, 27, "DATE"),       # 2/10
                (45, 49, "DATE"),       # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
    "Week 5 Global dimensions of personal finance 2/3 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 2/5 Financial Plan #1 Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 127, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 12 Real Estate Chapter 8 Chapter 1 5 3/24 Financial Plan #2 due Financial Advisory Services Chapter 9 Chapter 19 3/26",
    {
        "entities": [
            (42, 46, "DATE"),       # 3/24
            (47, 64, "ASSIGNMENT"), # Financial Plan #2 due
            (118, 122, "DATE")      # 3/26
        ]
    }
)
]

train_data += [
    (
        "Week 15 Quiz #3 4/14 Quiz #3 Group Presentation 4/16",
        {
            "entities": [
                (16, 20, "DATE"),        # 4/14
                (21, 28, "ASSIGNMENT"),  # Quiz #3
                (29, 47, "ASSIGNMENT"),  # Group Presentation
                (48, 52, "DATE")         # 4/16
            ]
        }
    )
]

train_data += [
    (
        "Week 17 Personal Relationships & Money Chapters 13, 14 Chapter 30 -32 4/28 Financial Plan #3 due",
        {
            "entities": [
                (70, 74, "DATE"),        # 4/28
                (75, 96, "ASSIGNMENT")   # Financial Plan #3 due
            ]
        }
    )
]


train_data += [
    (
        "Week 13 Personal Relationships & Money Chapters 13, 14 Chapter 30 -32 4/24 Financial Plan #1 due",
        {
            "entities": [
                (70, 74, "DATE"),        # 4/28
                (75, 96, "ASSIGNMENT")   # Financial Plan #3 due
            ]
        }
    )
]

train_data+= [
    (
    "Exam on May 10",
    {
        "entities": [
            (8, 14, "DATE"),       # 3/24
            (0, 4, "ASSIGNMENT"), # Financial Plan #2 due
        ]
    }
)
]

train_data+= [
    (
    "Midterm exam on May 20th.",
    {
        "entities": [
            (16, 24, "DATE"),       # 3/24
            (0, 7, "ASSIGNMENT"), # Financial Plan #2 due
        ]
    }
)
]

train_data+= [
    (
    "Final exam on August 14th.",
    {
        "entities": [
            (14, 25, "DATE"),       # 3/24
            (0, 5, "ASSIGNMENT"), # Financial Plan #2 due
        ]
    }
)
]

train_data+= [
    (
    "Final exam on August 25th.",
    {
        "entities": [
            (14, 25, "DATE"),       # 3/24
            (0, 5, "ASSIGNMENT"), # Financial Plan #2 due
        ]
    }
)
]

train_data+= [
    (
    "The midterm exam will be on May 4th.",
    {
        "entities": [
            (28, 35, "DATE"),       # 3/24
            (4, 11, "ASSIGNMENT"), # Financial Plan #2 due
        ]
    }
)
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Financial Plan #4 Due",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 127, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 9 Investment Strategies 9/15 Stock Market & Bonds Chapters 14 & 16 Chapters 18 & 20 9/17 Financial Plan #6 Due",
        {
            "entities": [
                (29, 33, "DATE"),      # 2/10
                (89, 93, "DATE"),      # 2/12
                (94, 115, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
    "Week 19 Real Estate Chapter 8 Chapter 1 5 2/21 Financial Plan #3 due Financial Advisory Services Chapter 9 Chapter 19 2/10",
    {
        "entities": [
            (42, 46, "DATE"),       # 3/24
            (47, 64, "ASSIGNMENT"), # Financial Plan #2 due
            (118, 122, "DATE")      # 3/26
        ]
    }
)

]

train_data += [
    (
        "Week 2 Well -Being Day 2/19 NO CLASS Quiz #2 2/17 Quiz #2",
        {
            "entities": [
                (23, 27, "DATE"),      # 2/10
                (45, 49, "DATE"),      # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 3 Well -Being Day 8/11 NO CLASS Quiz #6 8/13 Quiz #6",
        {
            "entities": [
                (23, 27, "DATE"),      # 2/10
                (45, 49, "DATE"),      # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 8 Well -Being Day 9/12 NO CLASS Quiz #5 9/15 Quiz #5",
        {
            "entities": [
                (23, 27, "DATE"),      # 2/10
                (45, 49, "DATE"),      # 2/12
                (50, 57, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
    "Week 3 Global dimensions of personal finance 4/1 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 4/5 Financial Plan #8 Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 127, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 6 Global dimensions of personal finance 9/2 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 8/3 Financial Plan #7 Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 127, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 3 Global dimensions of personal finance 5/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 5/8 Financial Plan #6 Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 127, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Analysis Paper Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 124, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Final Project due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 123, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 4 Global dimensions of personal finance 9/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 8/8 Group Project Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 123, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 4 Global dimensions of personal finance 9/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 8/8 Presentation Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 122, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 4 Global dimensions of personal finance 3/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/3 Final Presentation due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 128, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
    "Week 4 Global dimensions of personal finance 1/9 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/3 Group Presentation Due",
    {
        "entities": [
            (45, 48, "DATE"),       # 2/3
            (102, 105, "DATE"),     # 2/5
            (106, 128, "ASSIGNMENT") # Financial Plan #1
        ]
    }
)
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Paper",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 111, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Midterm Paper due",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 123, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Final Paper due",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 121, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Research Paper due",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 124, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Homework",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 114, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

train_data += [
    (
        "Week 4 Global dimensions of personal finance 7/7 Cash Management & Debt Chapters 3 & 4 Chapters 5 & 8 7/8 Problem Sets due",
        {
            "entities": [
                (45, 48, "DATE"),      # 2/10
                (102, 105, "DATE"),      # 2/12
                (106, 122, "ASSIGNMENT")  # Quiz #1
            ]
        }
    )
]

# Function to format data for SpaCy training
# def create_training_data(train_data, nlp):
#     db = DocBin()
#     for date, assignment in train_data:
#         text = f"{date} {assignment}"
#         doc = nlp.make_doc(text)
#         ents = []

#         start_date = 0
#         end_date = len(date)
#         start_assign = end_date + 1
#         end_assign = start_assign + len(assignment)

#         entities = [(start_date, end_date, "DATE"), (start_assign, end_assign, "ASSIGNMENT")]
        
#         for start, end, label in entities:
#             span = doc.char_span(start, end, label=label)
#             if span is not None:
#                 ents.append(span)

#         doc.ents = ents
#         db.add(doc)
#     return db

# Main execution
if __name__ == "__main__":
    pdf_path = "NER/PLAN 363 - Syllabus - Spring 2025 v3.pdf"
    
    print("Extracting text from PDF...")
    syllabus_text = pdf_to_text(pdf_path)
    # print(syllabus_text)


    print("Formatting data for SpaCy training...")
    nlp = spacy.blank("en")

    # Add entity recognizer to the pipeline (if it doesn't already exist)
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    ner.add_label("DATE")
    ner.add_label("ASSIGNMENT")

    train_examples = []
    for text, annot in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annot)
        train_examples.append(example)

# Set up optimizer and other training configurations
    optimizer = nlp.begin_training()
    for epoch in range(40):  # Run for 10 epochs
        print(f"Epoch {epoch+1}")
        random.shuffle(train_examples)
        losses = {}
        # Batch training examples
        nlp.update(train_examples, drop=0.5, losses=losses)
        print(losses)

    eval_examples = []
    val_data = []

    val_data += [
    (
        "Week 11 Investment: Bonds & Stocks Chapter 9 Chapters 20 -23 3/17 Quiz #2 3/19 Quiz #2",
        {
            "entities": [
                (61, 65, "DATE"),        # 3/17
                (74, 78, "DATE"),        # 3/19
                (79, 86, "ASSIGNMENT")   # Quiz #2
            ]
        }
    )
    ]
    
    val_data += [
    (
        "Week 15 Quiz #3 4/14 Quiz #3 Group Presentation 4/16",
        {
            "entities": [
                (16, 20, "DATE"),        # 4/14
                (21, 28, "ASSIGNMENT"),  # Quiz #3
                (29, 47, "ASSIGNMENT"),  # Group Presentation
                (48, 52, "DATE")         # 4/16
            ]
        }
    )
    ]

    val_data += [
    (
        "Week 17 Personal Relationships & Money Chapters 13, 14 Chapter 30 -32 4/28 Financial Plan #3 due",
        {
            "entities": [
                (70, 74, "DATE"),        # 4/28
                (75, 96, "ASSIGNMENT")   # Financial Plan #3 due
            ]
        }
    )
    ]  

    for text, annot in val_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annot)
        eval_examples.append(example)

    # Evaluate the model
    scores = nlp.evaluate(eval_examples)
    print(scores)

    # Saving the model to local machine
    nlp.to_disk("assignment_model")
