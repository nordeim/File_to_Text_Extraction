# Core dependencies
import os
import gradio as gr
from typing import Optional

# File processing libraries
from PyPDF2 import PdfReader
import markdown2
import json
import csv
from docx import Document
import openpyxl

# LangChain integration
from langchain_community.document_loaders import UnstructuredFileLoader

ALLOWED_EXTENSIONS = {
    '.txt', '.md', '.json', '.csv', '.pdf',
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
}

def validate_file(file_path: str) -> Optional[str]:
    """Validate file type and existence"""
    if not os.path.exists(file_path):
        return "Error: File not found"
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return f"Error: Unsupported file type {ext}"
    
    return None

def extract_text(file_path: str) -> str:
    """Main text extraction logic with format-specific handlers"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        elif ext == '.md':
            with open(file_path, 'r', encoding='utf-8') as f:
                return markdown2.markdown(f.read())
                
        elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
                
        elif ext == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                return '\n'.join([','.join(row) for row in csv.reader(f)])
                
        elif ext == '.pdf':
            with open(file_path, 'rb') as f:
                pdf = PdfReader(f)
                return '\n\n'.join([page.extract_text() for page in pdf.pages])
                
        elif ext in ('.doc', '.docx'):
            doc = Document(file_path)
            return '\n'.join([p.text for p in doc.paragraphs])
            
        elif ext in ('.xls', '.xlsx'):
            wb = openpyxl.load_workbook(file_path)
            return '\n'.join(
                ','.join(str(cell.value) for cell in row)
                for sheet in wb
                for row in sheet.iter_rows()
            )
            
        # Fallback to LangChain for PPT and other unsupported types
        return langchain_fallback(file_path)
        
    except Exception as e:
        return f"Processing Error: {str(e)}"

def langchain_fallback(file_path: str) -> str:
    """Fallback text extraction using LangChain"""
    try:
        loader = UnstructuredFileLoader(file_path)
        docs = loader.load()
        return '\n\n'.join([doc.page_content for doc in docs])
    except Exception as e:
        return f"LangChain Error: {str(e)}"

def save_output(content: str, original_path: str) -> str:
    """Save extracted text to output file"""
    try:
        base = os.path.splitext(original_path)[0]
        output_path = f"{base}_extracted.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return output_path
    except Exception as e:
        return f"Save Error: {str(e)}"

def process_file(file_obj) -> str:
    """Main processing pipeline"""
    # Validate file
    if error := validate_file(file_obj.name):
        return error
    
    # Extract content
    content = extract_text(file_obj.name)
    
    # Handle extraction errors
    if "Error" in content:
        return content
    
    # Save output
    output_path = save_output(content, file_obj.name)
    
    return f"Success! Output saved to:\n{output_path}\n\nExtracted Content:\n{content[:2000]}..." 

# Gradio interface configuration
interface = gr.Interface(
    fn=process_file,
    inputs=gr.File(label="Upload Document", file_count="single"),
    outputs=gr.Textbox(label="Processing Results", lines=10),
    title="Advanced Document Text Extractor",
    description="Supports: " + ', '.join(ALLOWED_EXTENSIONS),
    allow_flagging="never"
)

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860)
