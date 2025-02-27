# Python Application for File Text Extraction Using Gradio

This solution provides a Python application that uses Gradio to create a web UI for file text extraction. The application validates file types, extracts text using appropriate libraries, and falls back to LangChain when necessary. Below, I will break down the solution into steps, providing detailed explanations and well-documented code.

---

## Step 1: Initialize the Project

### 1.1 Install Required Libraries
First, set up a Python virtual environment and install the necessary libraries. Below is the list of libraries used for different file types:

- `gradio`: For creating the web UI.
- `PyPDF2`: For extracting text from PDF files.
- `markdown2`: For processing Markdown files.
- `python-docx`: For DOC and DOCX files.
- `openpyxl`: For XLS and XLSX files.
- `python-pptx`: For PPT and PPTX files.
- `langchain`: As a fallback for unsupported file types.
- `pandas`: For CSV files.

Run the following command to install the libraries:

```bash
pip install gradio PyPDF2 markdown2 python-docx openpyxl python-pptx langchain pandas
```

### 1.2 Project Structure
Create a new Python file, e.g., `file_text_extractor.py`. This file will contain the entire application code.

---

## Step 2: Design the Web UI

We will use Gradio to create a simple UI with a text input for the filename and an output area for displaying results or error messages.

### Code:

```python
import gradio as gr
import os
import json
import pandas as pd
from PyPDF2 import PdfReader
from markdown2 import markdown
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
from langchain.document_loaders import UnstructuredFileLoader

# Main function to handle file processing (defined later)
def process_file(filename):
    pass  # Placeholder for now

# Gradio interface
def create_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# File Text Extractor")
        gr.Markdown("Enter the path to a file to extract its text content.")
        
        filename_input = gr.Textbox(label="Input Filename", placeholder="e.g., /path/to/file.pdf")
        output_text = gr.Textbox(label="Result", interactive=False)
        
        submit_button = gr.Button("Extract Text")
        submit_button.click(
            fn=process_file,
            inputs=filename_input,
            outputs=output_text
        )
    
    return demo

# Launch the UI
if __name__ == "__main__":
    ui = create_ui()
    ui.launch()
```

### Explanation:
- The UI consists of a text input for the filename and a readonly output textbox for displaying results or errors.
- A "Extract Text" button triggers the `process_file` function (defined later).
- The UI is launched using `ui.launch()`.

---

## Step 3: File Type Validation

We will implement logic to validate the file extension and ensure it is one of the allowed types.

### Code:

```python
# Allowed file extensions
ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.json', '.csv', '.pdf',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
}

def validate_file(filename):
    """
    Validates the file extension and checks if the file exists.
    
    Args:
        filename (str): Path to the input file.
    
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    # Check if file exists
    if not os.path.exists(filename):
        return False, "Error: File does not exist."
    
    # Get file extension
    file_ext = os.path.splitext(filename)[1].lower()
    
    # Check if extension is allowed
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"Error: Unsupported file type '{file_ext}'. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    return True, ""
```

### Explanation:
- `ALLOWED_EXTENSIONS` is a set of valid file extensions.
- `validate_file` checks if the file exists and has an allowed extension.
- Returns a tuple: `(is_valid, error_message)`.

---

## Step 4: File Content Extraction

We will implement text extraction for each file type using the most compatible library. For unsupported types, we will use LangChain as a fallback.

### Code:

```python
def extract_text_from_txt(filename):
    """Extracts text from a plain text file."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_md(filename):
    """Extracts text from a Markdown file."""
    with open(filename, 'r', encoding='utf-8') as f:
        md_content = f.read()
        return markdown(md_content, extras=['fenced-code-blocks'])

def extract_text_from_json(filename):
    """Extracts text from a JSON file."""
    with open(filename, 'r', encoding='utf-8') as f:
        json_content = json.load(f)
        return json.dumps(json_content, indent=2)

def extract_text_from_csv(filename):
    """Extracts text from a CSV file."""
    df = pd.read_csv(filename)
    return df.to_string()

def extract_text_from_pdf(filename):
    """Extracts text from a PDF file."""
    reader = PdfReader(filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(filename):
    """Extracts text from a DOCX file."""
    doc = Document(filename)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_text_from_xlsx(filename):
    """Extracts text from an XLSX file."""
    wb = load_workbook(filename)
    text = ""
    for sheet in wb:
        for row in sheet.rows:
            for cell in row:
                if cell.value:
                    text += str(cell.value) + " "
            text += "\n"
    return text

def extract_text_from_pptx(filename):
    """Extracts text from a PPTX file."""
    prs = Presentation(filename)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text + "\n"
    return text

def extract_text_with_langchain(filename):
    """Fallback: Extracts text using LangChain for unsupported file types."""
    loader = UnstructuredFileLoader(filename)
    documents = loader.load()
    return "\n".join([doc.page_content for doc in documents])

def extract_text(filename):
    """
    Extracts text from the given file based on its extension.
    
    Args:
        filename (str): Path to the input file.
    
    Returns:
        tuple: (str, str) - (extracted_text, error_message)
    """
    file_ext = os.path.splitext(filename)[1].lower()
    
    try:
        if file_ext == '.txt':
            return extract_text_from_txt(filename), ""
        elif file_ext == '.md':
            return extract_text_from_md(filename), ""
        elif file_ext == '.json':
            return extract_text_from_json(filename), ""
        elif file_ext == '.csv':
            return extract_text_from_csv(filename), ""
        elif file_ext == '.pdf':
            return extract_text_from_pdf(filename), ""
        elif file_ext == '.docx' or file_ext == '.doc':
            return extract_text_from_docx(filename), ""
        elif file_ext == '.xlsx' or file_ext == '.xls':
            return extract_text_from_xlsx(filename), ""
        elif file_ext == '.pptx' or file_ext == '.ppt':
            return extract_text_from_pptx(filename), ""
        else:
            # Fallback to LangChain for unsupported types
            return extract_text_with_langchain(filename), ""
    except Exception as e:
        return "", f"Error extracting text: {str(e)}"
```

### Explanation:
- Each file type has a dedicated extraction function (e.g., `extract_text_from_pdf`, `extract_text_from_docx`).
- The `extract_text` function determines the file type and calls the appropriate extraction function.
- If an error occurs, it returns an empty string and an error message.
- LangChain's `UnstructuredFileLoader` is used as a fallback for unsupported file types.

---

## Step 5: File Saving

After extracting the text, we will save it to a new `.txt` file with the original filename appended with `_extracted.txt`.

### Code:

```python
def save_extracted_text(filename, text):
    """
    Saves the extracted text to a new file.
    
    Args:
        filename (str): Original filename.
        text (str): Extracted text.
    
    Returns:
        str: Success or error message.
    """
    try:
        output_filename = os.path.splitext(filename)[0] + "_extracted.txt"
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Text successfully saved to {output_filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"
```

### Explanation:
- The output filename is generated by appending `_extracted.txt` to the original filename.
- The extracted text is saved using UTF-8 encoding.
- Returns a success or error message.

---

## Step 6: Main Processing Function and Error Handling

We will implement the `process_file` function, which ties together all the previous steps.

### Code:

```python
def process_file(filename):
    """
    Main function to process the input file and extract text.
