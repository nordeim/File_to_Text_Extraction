```python
# Import necessary libraries
import os
import csv
import json
import gradio as gr
from typing import Optional
from PyPDF2 import PdfReader
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
from langchain.document_loaders import UnstructuredFileLoader

# Define allowed file extensions
ALLOWED_EXTENSIONS = [
    '.txt', '.md', '.json', '.csv', '.pdf',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
]

def get_file_extension(file_path: str) -> str:
    """Extract and normalize file extension"""
    return os.path.splitext(file_path)[1].lower()

def validate_file_type(ext: str) -> bool:
    """Check if file extension is allowed"""
    return ext in ALLOWED_EXTENSIONS

def extract_text_content(file_path: str) -> str:
    """Main text extraction router"""
    ext = get_file_extension(file_path)
    
    # Text-based files
    if ext in ['.txt', '.md']:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    
    # Structured data files
    if ext == '.json':
        with open(file_path, 'r') as f:
            return json.dumps(json.load(f), indent=2)
    
    if ext == '.csv':
        with open(file_path, 'r') as f:
            return '\n'.join([', '.join(row) for row in csv.reader(f)])
    
    # PDF files
    if ext == '.pdf':
        text = []
        reader = PdfReader(file_path)
        for page in reader.pages:
            if page_text := page.extract_text():
                text.append(page_text)
        return '\n'.join(text)
    
    # Modern Office formats
    if ext == '.docx':
        return '\n'.join([p.text for p in Document(file_path).paragraphs])
    
    if ext == '.xlsx':
        wb = load_workbook(file_path, read_only=True)
        return '\n'.join(
            '\t'.join(str(cell) for cell in row)
            for sheet in wb
            for row in sheet.values
        )
    
    if ext == '.pptx':
        return '\n'.join(
            shape.text
            for slide in Presentation(file_path).slides
            for shape in slide.shapes
            if hasattr(shape, "text")
        )
    
    # Legacy formats using LangChain fallback
    loader = UnstructuredFileLoader(file_path)
    return '\n'.join([doc.page_content for doc in loader.load()])

def process_file(file_obj: gr.FileData) -> str:
    """Gradio processing function with error handling"""
    try:
        file_path = file_obj.path
        ext = get_file_extension(file_path)
        
        if not validate_file_type(ext):
            return f"Error: Unsupported file type {ext}"
        
        text_content = extract_text_content(file_path)
        output_path = os.path.splitext(file_path)[0] + '.txt'
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
            
        return f"Success! Output saved to:\n{output_path}"
    
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="File to Text Converter") as interface:
    gr.Markdown("# 📄 File to Text Converter\nUpload a file to extract its text content")
    
    with gr.Row():
        file_input = gr.File(
            label="Upload File",
            file_types=ALLOWED_EXTENSIONS,
            type='filepath',
            height=100
        )
    
    with gr.Row():
        output = gr.Textbox(label="Processing Status", interactive=False)
    
    with gr.Row():
        gr.Button("Convert").click(
            fn=process_file,
            inputs=file_input,
            outputs=output
        )

if __name__ == "__main__":
    interface.launch(server_port=7860, show_error=True)
```

**Implementation Notes:**

1. **Dependency Management:**
   ```bash
   pip install gradio PyPDF2 python-docx openpyxl python-pptx langchain unstructured
   ```

2. **Key Components:**
   - **File Type Validation:** Uses extension whitelisting with comprehensive Office format support
   - **Modular Extraction:** Specialized handlers for each file type ensure optimal text extraction
   - **LangChain Fallback:** Handles legacy formats using Unstructured.io's powerful parsing
   - **Error Handling:** Comprehensive try/catch blocks with user-friendly error messages

3. **Advanced Features:**
   - Text encoding handling with error replacement
   - Memory-efficient Excel/PDF processing
   - Context-aware PowerPoint text extraction
   - Full support for modern Office Open XML formats

4. **Recommended System Setup:**
   - Install LibreOffice for best legacy format support
   - Allocate sufficient memory for large file processing
   - Consider GPU acceleration for PDF processing at scale

This implementation provides a robust solution that balances specificity of handling with fallback generality, ensuring maximum file format compatibility while maintaining extraction quality.
