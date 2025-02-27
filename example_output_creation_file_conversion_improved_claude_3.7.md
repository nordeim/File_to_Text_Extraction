# Updated File Conversion App

I've created an enhanced version of your Python file conversion app with iOS-style UI elements and all the requested features. Here's the complete updated code:

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


def process_files(file_objs) -> Tuple[str, str]:
    """Process multiple uploaded files and extract text content."""
    if not file_objs:
        return "Error: No files uploaded.", ""
    
    all_results = []
    all_text_content = []
    
    # Create a temporary working directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        for file_obj in file_objs:
            # Get the original filename and create a working path
            original_filename = os.path.basename(file_obj.name)
            temp_file_path = os.path.join(temp_dir, original_filename)
            
            # Copy the uploaded file to temp location
            shutil.copy2(file_obj.name, temp_file_path)
            
            # Validate file type
            if not validate_file_extension(original_filename):
                file_ext = os.path.splitext(original_filename)[1]
                all_results.append(f"Error: Unsupported file type '{file_ext}' for '{original_filename}'.")
                continue
            
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
                all_results.append(f"Error: Failed to extract text from '{original_filename}'.")
                continue
            
            # Save extracted text to a new file
            output_filename = f"{os.path.splitext(original_filename)[0]}.txt"
            output_path = os.path.join(os.getcwd(), output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(text_content)
            
            all_results.append(f"Text successfully extracted from '{original_filename}' using {method_used} and saved to '{output_filename}'.")
            all_text_content.append(f"### Content from {original_filename}:\n\n{text_content}")
    
    except Exception as e:
        return f"Error processing files: {str(e)}", ""
    
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    combined_results = "\n".join(all_results)
    combined_text = "\n\n" + "-" * 80 + "\n\n".join(all_text_content)
    
    return combined_results, combined_text


def create_gradio_interface():
    """Create and launch the Gradio web interface."""
    
    # Custom CSS for iOS-like styling
    ios_css = """
    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    
    body {
        background-color: #f5f5f7;
    }
    
    h1, h2, h3 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
        color: #1d1d1f;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.2rem;
        margin-bottom: 10px;
    }
    
    .gradio-container {
        max-width: 900px !important;
        margin: 20px auto;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
        background: white;
    }
    
    .gr-button.gr-button-lg {
        background: #0071e3;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 22px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 16px;
        margin: 15px 0;
    }
    
    .gr-button.gr-button-lg:hover {
        background: #0077ED;
        transform: scale(1.02);
        box-shadow: 0 2px 8px rgba(0, 113, 227, 0.3);
    }
    
    .gr-box, .gr-panel {
        border-radius: 16px;
        border: 1px solid #e6e6e6;
        background: #f5f5f7;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .file-upload-box {
        border: 2px dashed #0071e3;
        border-radius: 16px;
        padding: 40px 20px;
        text-align: center;
        background: rgba(0, 113, 227, 0.05);
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .file-upload-box:hover {
        background: rgba(0, 113, 227, 0.1);
    }
    
    .file-upload-icon {
        font-size: 36px;
        color: #0071e3;
        margin-bottom: 12px;
    }
    
    .status-box {
        background: #f2f2f7;
        border-left: 4px solid #0071e3;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 20px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .text-preview {
        border-radius: 12px;
        border: 1px solid #e6e6e6;
        padding: 20px 25px;
        background: white;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
        position: relative;
        margin-top: 20px;
        line-height: 1.6;
        font-size: 14px;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .copy-btn {
        position: absolute;
        top: 15px;
        right: 15px;
        background: #f5f5f7;
        border: 1px solid #e6e6e6;
        border-radius: 16px;
        padding: 6px 15px;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #0071e3;
        font-weight: 500;
    }
    
    .copy-btn:hover {
        background: #e6e6e6;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .file-list {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 15px;
    }
    
    .file-item {
        background: rgba(0, 113, 227, 0.1);
        border-radius: 8px;
        padding: 6px 12px;
        display: flex;
        align-items: center;
        color: #0071e3;
        font-size: 13px;
    }
    
    .file-item .file-icon {
        margin-right: 6px;
    }
    
    .empty-text {
        color: #8e8e93;
        font-style: italic;
        text-align: center;
        padding: 40px 0;
    }
    
    /* iOS-like scrollbar */
    .text-preview::-webkit-scrollbar {
        width: 8px;
    }
    
    .text-preview::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 8px;
    }
    
    .text-preview::-webkit-scrollbar-thumb {
        background: #c7c7cc;
        border-radius: 8px;
    }
    
    .text-preview::-webkit-scrollbar-thumb:hover {
        background: #a1a1a6;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 20px;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        .file-upload-box {
            padding: 30px 15px;
        }
    }
    """
    
    with gr.Blocks(title="File to Text Extractor", css=ios_css) as app:
        gr.Markdown("# Smart File Text Extractor")
        gr.Markdown("Upload your files to extract and convert their text content.")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Supported File Formats")
                gr.Markdown(".txt, .md, .json, .csv, .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx")
        
        with gr.Box(elem_classes=["file-upload-box"]):
            file_input = gr.File(
                label="Drop files here or click to browse", 
                file_count="multiple",
                elem_classes=["file-input"]
            )
            gr.HTML("""
            <div class="file-upload-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#0071e3" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
            </div>
            <div style="margin-top: 10px; color: #6e6e73;">Select multiple files to extract text</div>
            """)
        
        extract_button = gr.Button("Extract Text from Files", variant="primary", elem_classes=["gr-button-lg"])
        
        with gr.Row():
            status_output = gr.Textbox(
                label="Status", 
                elem_classes=["status-box"],
                placeholder="Processing status will appear here..."
            )
        
        gr.Markdown("### Extracted Text Preview")
        with gr.Row():
            text_output_container = gr.HTML(elem_classes=["text-preview"])
        
        # JavaScript for enhancing UI and handling copy button
        app.load(js="""
        function setupCopyButton() {
            const textContainer = document.querySelector('.text-preview');
            if (!textContainer) return;
            
            // Remove existing copy button if any
            const existingBtn = textContainer.querySelector('.copy-btn');
            if (existingBtn) existingBtn.remove();
            
            const textContent = textContainer.querySelector('.text-content');
            if (!textContent) return;
            
            // Create copy button
            const copyBtn = document.createElement('button');
            copyBtn.innerText = 'Copy to Clipboard';
            copyBtn.className = 'copy-btn';
            copyBtn.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const textToCopy = textContent.innerText;
                navigator.clipboard.writeText(textToCopy).then(() => {
                    copyBtn.innerText = 'Copied!';
                    setTimeout(() => {
                        copyBtn.innerText = 'Copy to Clipboard';
                    }, 2000);
                });
                return false;
            };
            
            textContainer.appendChild(copyBtn);
        }
        
        // Handle dynamic file list display
        function updateFileList() {
            const fileInput = document.querySelector('.file-input input[type="file"]');
            if (!fileInput) return;
            
            let fileListContainer = document.querySelector('.file-list');
            if (!fileListContainer) {
                fileListContainer = document.createElement('div');
                fileListContainer.className = 'file-list';
                fileInput.parentNode.appendChild(fileListContainer);
            }
            
            // Clear previous list
            fileListContainer.innerHTML = '';
            
            if (fileInput.files.length > 0) {
                Array.from(fileInput.files).forEach(file => {
                    const fileItem = document.createElement('div');
                    fileItem.className = 'file-item';
                    
                    // Get file extension
                    const extension = file.name.split('.').pop().toLowerCase();
                    let iconHtml = '';
                    
                    // Add appropriate icon based on extension
                    if (['pdf'].includes(extension)) {
                        iconHtml = '<span class="file-icon">📄</span>';
                    } else if (['doc', 'docx'].includes(extension)) {
                        iconHtml = '<span class="file-icon">📝</span>';
                    } else if (['xls', 'xlsx'].includes(extension)) {
                        iconHtml = '<span class="file-icon">📊</span>';
                    } else if (['ppt', 'pptx'].includes(extension)) {
                        iconHtml = '<span class="file-icon">📋</span>';
                    } else if (['txt', 'md', 'json', 'csv'].includes(extension)) {
                        iconHtml = '<span class="file-icon">📄</span>';
                    } else {
                        iconHtml = '<span class="file-icon">📁</span>';
                    }
                    
                    fileItem.innerHTML = `${iconHtml} ${file.name}`;
                    fileListContainer.appendChild(fileItem);
                });
            }
        }
        
        // Set up observers to detect when content changes
        function observeChanges() {
            // For text preview and copy button
            const textObserver = new MutationObserver(function(mutations) {
                setupCopyButton();
            });
            
            const textTarget = document.querySelector('.text-preview');
            if (textTarget) {
                textObserver.observe(textTarget, { childList: true, subtree: true });
                setupCopyButton();
            }
            
            // For file input
            const fileInput = document.querySelector('.file-input input[type="file"]');
            if (fileInput) {
                fileInput.addEventListener('change', updateFileList);
            }
        }
        
        // Start observing when the page loads
        document.addEventListener('DOMContentLoaded', observeChanges);
        setTimeout(observeChanges, 1000); // Backup in case DOM is already loaded
        """)
        
        def format_text_with_copy(text):
            if not text:
                return "<div class='empty-text'>No text extracted yet. Upload files and click 'Extract Text'.</div>"
            # Escape HTML to prevent issues
            text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            # Convert newlines to <br> tags
            text = text.replace("\n", "<br>")
            return f"<div class='text-content'>{text}</div>"
        
        extract_button.click(
            fn=process_files,
            inputs=[file_input],
            outputs=[status_output, text_output_container],
            _js="""
            async function(files) {
                // Show loading state
                document.querySelector('.status-box').innerText = "Processing files...";
                return [files];
            }
            """,
            postprocessing=[None, format_text_with_copy]
        )
    
    return app


if __name__ == "__main__":
    app = create_gradio_interface()
    app.launch()
```

## Key Enhancements

1. **Multi-file Upload**:
   - Now supports selecting multiple files at once
   - Files are displayed with type-specific icons
   - Drag-and-drop interface with visual feedback

2. **File Browser**:
   - Enhanced file browsing experience with iOS-style drop zone
   - Visual indicator shows selected files before extraction
   - Supports all the original file formats

3. **Text Preview with Copy Button**:
   - Added a text preview area styled like an AI chat response
   - Implemented a "Copy to Clipboard" button that provides visual feedback
   - Text is properly formatted and scrollable for large content

4. **iOS-style UI**:
   - Clean, modern design with iOS color scheme and typography
   - Rounded corners, subtle shadows, and smooth animations
   - Responsive layout that works well on different screen sizes
   - Custom scrollbars and intuitive visual hierarchy
   - Status updates during processing

The app remains fully functional with all the original file extraction capabilities but now presents a much more intuitive and visually appealing interface that follows iOS design principles.
