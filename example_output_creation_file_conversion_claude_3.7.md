# File to Text Extractor Application with Gradio

I'll create a comprehensive Python application that extracts text from various file formats using a Gradio web UI. This solution handles multiple file types and implements appropriate extraction methods for each.

## Setup and Imports

Let's start with the necessary imports and core functionality:

```python
import os
import gradio as gr
import tempfile
import shutil
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("file_extractor")

# Core libraries for basic file handling
import json
import csv
import pandas as pd

# Import specialized file processing libraries
try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    logger.warning("PyPDF2 not installed. PDF extraction may be limited.")

try:
    from docx import Document
    DOCX_SUPPORT = True
except ImportError:
    DOCX_SUPPORT = False
    logger.warning("python-docx not installed. DOCX extraction may be limited.")

try:
    from openpyxl import load_workbook
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False
    logger.warning("openpyxl not installed. Excel extraction may be limited.")

try:
    from pptx import Presentation
    PPTX_SUPPORT = True
except ImportError:
    PPTX_SUPPORT = False
    logger.warning("python-pptx not installed. PowerPoint extraction may be limited.")

try:
    import markdown2
    MARKDOWN_SUPPORT = True
except ImportError:
    MARKDOWN_SUPPORT = False
    logger.warning("markdown2 not installed. Markdown extraction may be limited.")

# Import LangChain components for advanced extraction
try:
    from langchain.document_loaders import (
        TextLoader,
        UnstructuredMarkdownLoader,
        JSONLoader,
        CSVLoader,
        PyPDFLoader,
        Docx2txtLoader,
        UnstructuredWordDocumentLoader,
        UnstructuredExcelLoader,
        UnstructuredPowerPointLoader
    )
    LANGCHAIN_SUPPORT = True
except ImportError:
    LANGCHAIN_SUPPORT = False
    logger.warning("LangChain not installed. Will use fallback extraction methods.")
```

## File Validation and Text Extraction Functions

```python
def validate_file_extension(filename: str) -> bool:
    """Check if the file has a supported extension."""
    allowed_extensions = [
        # Text-based formats
        ".txt", ".md", ".json", ".csv", ".pdf",
        # Microsoft Office formats
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
    ]
    _, extension = os.path.splitext(filename.lower())
    return extension in allowed_extensions

def extract_text_with_langchain(file_path: str) -> Optional[str]:
    """Extract text using LangChain document loaders."""
    if not LANGCHAIN_SUPPORT:
        return None
        
    _, extension = os.path.splitext(file_path.lower())
    
    try:
        if extension == ".txt":
            loader = TextLoader(file_path, encoding='utf-8')
        elif extension == ".md":
            loader = UnstructuredMarkdownLoader(file_path)
        elif extension == ".json":
            # Extract JSON content
            def json_content_formatter(data: dict) -> str:
                return json.dumps(data, indent=2)
            
            loader = JSONLoader(
                file_path=file_path,
                jq_schema=".",
                content_formatter=json_content_formatter
            )
        elif extension == ".csv":
            loader = CSVLoader(file_path)
        elif extension == ".pdf":
            loader = PyPDFLoader(file_path)
        elif extension == ".docx":
            loader = Docx2txtLoader(file_path)
        elif extension == ".doc":
            loader = UnstructuredWordDocumentLoader(file_path)
        elif extension in [".xlsx", ".xls"]:
            loader = UnstructuredExcelLoader(file_path)
        elif extension in [".pptx", ".ppt"]:
            loader = UnstructuredPowerPointLoader(file_path)
        else:
            return None
        
        documents = loader.load()
        return "\n\n".join([doc.page_content for doc in documents])
    
    except Exception as e:
        logger.warning(f"LangChain extraction failed: {str(e)}")
        return None

def extract_text_fallback(file_path: str) -> str:
    """Extract text using specialized libraries as fallback."""
    _, extension = os.path.splitext(file_path.lower())
    
    try:
        # Plain text files
        if extension == ".txt":
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                return file.read()
        
        # Markdown files        
        elif extension == ".md":
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                content = file.read()
                if MARKDOWN_SUPPORT:
                    return markdown2.markdown(content)
                return content
        
        # JSON files        
        elif extension == ".json":
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                data = json.load(file)
                return json.dumps(data, indent=2)
        
        # CSV files        
        elif extension == ".csv":
            text_lines = []
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                reader = csv.reader(file)
                for row in reader:
                    text_lines.append(",".join(row))
            return "\n".join(text_lines)
        
        # PDF files        
        elif extension == ".pdf":
            if PDF_SUPPORT:
                text_parts = []
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(reader.pages)):
                        page_text = reader.pages[page_num].extract_text()
                        if page_text:
                            text_parts.append(page_text)
                return "\n\n".join(text_parts)
            else:
                return "PDF extraction requires PyPDF2 library."
        
        # Word documents        
        elif extension == ".docx":
            if DOCX_SUPPORT:
                doc = Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            else:
                return "DOCX extraction requires python-docx library."
        
        # Excel files        
        elif extension in [".xlsx", ".xls"]:
            try:
                df = pd.read_excel(file_path)
                return df.to_string()
            except Exception as e:
                if EXCEL_SUPPORT and extension == ".xlsx":
                    wb = load_workbook(file_path)
                    text_lines = []
                    for sheet in wb:
                        for row in sheet.iter_rows(values_only=True):
                            text_lines.append("\t".join([str(cell) for cell in row if cell is not None]))
                    return "\n".join(text_lines)
                return f"Excel extraction error: {str(e)}"
        
        # PowerPoint files        
        elif extension == ".pptx":
            if PPTX_SUPPORT:
                prs = Presentation(file_path)
                text_parts = []
                for slide in prs.slides:
                    for shape in slide.shapes:
                        if hasattr(shape, "text"):
                            text_parts.append(shape.text)
                return "\n\n".join(text_parts)
            else:
                return "PPTX extraction requires python-pptx library."
        
        # Legacy formats that might need specialized libraries        
        elif extension in [".doc", ".ppt"]:
            try:
                import textract
                return textract.process(file_path).decode('utf-8')
            except ImportError:
                return f"{extension.upper()} extraction requires textract library."
        
        else:
            return f"No fallback extraction method available for {extension} files."
    
    except Exception as e:
        return f"Extraction error: {str(e)}"
```

## Main Processing Function and Gradio Interface

```python
def process_file(file_obj) -> Tuple[str, str]:
    """Process the uploaded file and extract text content."""
    if file_obj is None:
        return "Error: No file uploaded.", ""
    
    # Create a temporary working directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Get the original filename and create a working path
        original_filename = os.path.basename(file_obj.name)
        temp_file_path = os.path.join(temp_dir, original_filename)
        
        # Copy the uploaded file to temp location
        shutil.copy2(file_obj.name, temp_file_path)
        
        # Validate file type
        if not validate_file_extension(original_filename):
            file_ext = os.path.splitext(original_filename)[1]
            return f"Error: Unsupported file type '{file_ext}'.", ""
        
        # Try extraction with LangChain first
        text_content = None
        method_used = ""
        
        if LANGCHAIN_SUPPORT:
            text_content = extract_text_with_langchain(temp_file_path)
            if text_content:
                method_used = "LangChain"
        
        # If LangChain failed or isn't available, use fallback methods
        if text_content is None:
            text_content = extract_text_fallback(temp_file_path)
            method_used = "specialized libraries"
        
        if not text_content:
            return "Error: Failed to extract text from the file.", ""
        
        # Save extracted text to a new file
        output_filename = f"{os.path.splitext(original_filename)[0]}.txt"
        output_path = os.path.join(os.getcwd(), output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        
        return f"Text successfully extracted using {method_used} and saved to '{output_filename}'.", text_content
    
    except Exception as e:
        return f"Error processing file: {str(e)}", ""
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def create_gradio_interface():
    """Create and launch the Gradio web interface."""
    with gr.Blocks(title="File to Text Extractor") as app:
        gr.Markdown("# File to Text Extractor")
        gr.Markdown("Upload a file to extract its text content.")
        gr.Markdown("Supported formats: .txt, .md, .json, .csv, .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx")
        
        with gr.Row():
            file_input = gr.File(label="Select File")
        
        extract_button = gr.Button("Extract Text")
        
        with gr.Row():
            status_output = gr.Textbox(label="Status")
        
        with gr.Row():
            text_output = gr.Textbox(label="Extracted Text", lines=20)
        
        extract_button.click(
            fn=process_file,
            inputs=[file_input],
            outputs=[status_output, text_output]
        )
    
    return app

# Main execution
if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch()
```

## Requirements.txt File

Here's the requirements.txt file for the application:

```
gradio>=3.50.0
langchain>=0.0.267
PyPDF2>=3.0.0
markdown2>=2.4.10
pandas>=2.0.0
python-docx>=0.8.11
openpyxl>=3.1.2
python-pptx>=0.6.21
# Optional for legacy formats (.doc and .ppt)
textract>=1.6.5
```

## How The Application Works

1. **File Upload**: Users upload files through the Gradio interface
2. **Validation**: The app checks if the file extension is supported
3. **Extraction Process**: 
   - First attempts extraction using LangChain (if available)
   - Falls back to specialized libraries if LangChain fails or isn't installed
4. **Results**: Displays the extracted text and saves it as a .txt file

The application handles a variety of formats intelligently and provides clear feedback to the user about the extraction process.
