Okay, let me start breaking down the problem. The user wants a Gradio app that takes a file input, checks its type, and converts its content to plain text using appropriate libraries. If there's no specific library, use LangChain. Hmm, first, I need to list all the allowed file types and map them to their respective processing libraries.

So the allowed extensions are .txt, .md, .json, .csv, .pdf, and the Microsoft Office ones: .doc, .docx, .xls, .xlsx, .ppt, .pptx. For each of these, I need to find the best Python library. Let's think:

- .txt is straightforward, just read the file.

- .md can be read as text, but maybe process markdown to plain text? Wait, the task says convert to plain text, so perhaps just read the markdown as text without rendering. The user might want the raw text, not the rendered version. So maybe just read the .md file as text.

- .json: Parse and maybe convert to a string representation. Like, json.dumps to make it readable.

- .csv: Read rows and convert to text, maybe each row as a line.

- .pdf: Use PyPDF2 or pdfplumber? PyPDF2 is common but sometimes has issues with text extraction. Maybe pdfplumber is better, but requires installation. Or PyMuPDF? Need to check which is more reliable.

- .doc: Older Word files. Python-docx doesn't handle .doc, only .docx. So for .doc, maybe use antiword or some other library. Wait, but antiword is a Linux tool. Alternatively, maybe use LibreOffice in headless mode to convert, but that's system-dependent. Alternatively, maybe using catdoc or other CLI tools, but that's not Pythonic. Hmm, this could be a problem. Alternatively, maybe use the textract library, which wraps multiple extractors. But textract may have dependencies. However, the user mentioned using LangChain as a fallback. Wait, maybe for .doc files, since there's no direct Python library, we can use LangChain's document loaders? Let's check. LangChain's UnstructuredFileLoader supports various files, including .doc, but requires the unstructured library and possibly other dependencies. So maybe for .doc, .ppt, .xls, we can use the UnstructuredFileLoader from LangChain.

Wait, the user's action step 4 says: for each allowed file type, use the most compatible library. If no specialized library exists, use LangChain. So for example, for .docx, we can use python-docx, but for .doc (old format), if there's no library, then use LangChain. Let me verify:

- .docx: python-docx can read them.

- .xlsx: openpyxl can read them.

- .pptx: python-pptx can read them.

- .doc: Maybe no direct Python library, so LangChain's UnstructuredFileLoader.

- .xls: Older Excel. Maybe use xlrd library? But xlrd has dropped support for xls files in newer versions. Alternatively, use pandas with engine='xlrd', but that might require specific versions. Or use LangChain here as well.

- .ppt: Older PowerPoint. Again, maybe no direct Python library, so LangChain.

Alternatively, perhaps use the unstructured library directly, which can handle many file types. But the user mentioned using LangChain as a fallback. So maybe the plan is:

- For each file type, check if a specific library exists (like PyPDF2 for pdf, python-docx for docx, openpyxl for xlsx, etc.), use that. For others (like doc, xls, ppt), use LangChain's document loaders, which in turn may use unstructured.

So let's list the processors:

- .txt: read directly.

- .md: read directly.

- .json: json.load and convert to string.

- .csv: read with csv module.

- .pdf: PyPDF2 or pdfplumber.

- .docx: python-docx.

- .xlsx: openpyxl.

- .pptx: python-pptx.

- .doc, .xls, .ppt: LangChain's UnstructuredFileLoader.

Wait, but the user's allowed extensions include .doc, .xls, .ppt. So we need to handle them. For .doc, if there's no direct Python library, then use LangChain. Similarly for .xls and .ppt.

But first, need to install all the required libraries. So in the code, we'll have to import the necessary modules, but only if they exist. Wait, no—since the code should handle each file type with the best library, we need to make sure the required libraries are installed. So the user must install them. Therefore, the code should include the necessary imports and assume the libraries are installed.

So for each file type:

- .txt: read as text.

- .md: read as text.

- .json: use json module to load and dump to string.

- .csv: use csv.reader to read and convert to text.

- .pdf: use PyPDF2's PdfReader to extract text from each page.

- .docx: use docx's Document to get paragraphs.

- .xlsx: use openpyxl's load_workbook to read cells.

- .pptx: use pptx's Presentation to get text in slides.

- For .doc, .xls, .ppt: use LangChain's UnstructuredFileLoader.

But wait, the user's action step 4 says if no specialized library exists, use LangChain. So for example, for .doc files, if there's a specialized library (like textract or antiword), but the user didn't mention that. Since the user's instruction says to use the most compatible library first, then fallback to LangChain.

Alternatively, maybe the code should first check the file extension, then route to the appropriate extractor function. Each function uses the specific library, and if that's not possible, then use LangChain.

But first, let's structure the code. The Gradio interface needs a function that takes a file path, processes it, and returns the text or an error.

So the main function will:

1. Check the file extension against allowed types. If not allowed, raise error.

2. Depending on the extension, call the appropriate text extraction function.

3. Save the extracted text to a .txt file.

4. Return the output filename or an error message.

Now, for each extension's extraction function:

Implement functions like extract_txt, extract_md, extract_pdf, etc.

But for some extensions, like .doc, .xls, .ppt, there may not be a direct Python library, so in those cases, use LangChain's UnstructuredFileLoader.

Wait, LangChain's document loaders can handle various file types. For example, the UnstructuredFileLoader uses the unstructured library, which supports many file types. So maybe instead of handling each file type with specific libraries, we could use the UnstructuredFileLoader for all except the ones that are better handled by other libraries. Wait, but the user's instruction says to use the most compatible library for each file type. For example, for PDFs, maybe PyPDF2 is more straightforward than using LangChain's loader. However, it's possible that using UnstructuredFileLoader via LangChain could handle all the file types, but the user wants to use specific libraries when available for better compatibility.

So perhaps the approach is to handle each file type with the best library, and for those that don't have a specific library, use LangChain's UnstructuredFileLoader.

Let me list each allowed extension and their respective libraries:

- .txt: built-in open.

- .md: built-in open.

- .json: json module.

- .csv: csv module.

- .pdf: PyPDF2 or pdfplumber.

- .docx: python-docx.

- .xlsx: openpyxl.

- .pptx: python-pptx.

- .doc, .xls, .ppt: LangChain's UnstructuredFileLoader.

So the code will have separate functions for each of these. Now, the code needs to handle these cases.

But wait, .xls (old Excel) can be read with xlrd library. However, xlrd 2.0+ no longer supports xls files. So pandas can read xls with engine='xlrd' if xlrd is installed. Alternatively, maybe use LangChain's loader here. But according to the user's action step 4, if a specialized library exists, use it. So perhaps for .xls, use xlrd, but need to handle that.

But this can get complicated. Maybe for .xls, .doc, .ppt, it's better to use LangChain's UnstructuredFileLoader since there might not be a straightforward Python library.

Alternatively, perhaps use the textract library, which can handle many file types. But the user didn't mention that. Since the problem statement says to use the most compatible library for each type, and if none exists, use LangChain.

So, proceeding with the original plan.

Now, code steps:

First, the Gradio interface. The input is a file path, and the output could be the saved filename or an error.

But Gradio's interface can take a file input component. So the user uploads a file, which in Gradio is handled as a temporary file path. The function then takes this path, processes it.

The main function will:

- Check the file extension. Split the filename to get the extension. But need to be careful with uppercase extensions, so convert to lowercase.

If the extension is not in the allowed list, return an error.

If allowed, determine which extractor function to use.

For example:

if ext == 'txt' or ext == 'md':

text = read the file directly.

elif ext == 'json':

load with json and convert to string.

elif ext == 'csv':

read with csv.reader and convert rows to text.

elif ext == 'pdf':

use PyPDF2 to extract text.

elif ext == 'docx':

use python-docx to get paragraphs.

elif ext == 'xlsx':

use openpyxl to read cells.

elif ext == 'pptx':

use python-pptx to get slides.

else (for doc, xls, ppt):

use LangChain's UnstructuredFileLoader.

Wait, but in the allowed list, .doc, .xls, .ppt are included, so the code needs to handle them. So for these, the code will call the LangChain loader.

So, code structure:

def process_file(file_path):

# get extension

ext = get_extension(file_path)

if ext not in allowed_extensions:

return "Error: Invalid file type."

# based on ext, call extractor

if ext in ['txt', 'md']:

text = read_file(file_path)

elif ext == 'json':

text = extract_json(file_path)

elif ext == 'csv':

text = extract_csv(file_path)

elif ext == 'pdf':

text = extract_pdf(file_path)

elif ext == 'docx':

text = extract_docx(file_path)

elif ext == 'xlsx':

text = extract_xlsx(file_path)

elif ext == 'pptx':

text = extract_pptx(file_path)

else:  # .doc, .xls, .ppt

text = extract_with_langchain(file_path)

# save text to .txt file

output_path = file_path + '.txt'  # or append before extension

# better to replace the extension

base = os.path.splitext(file_path)[0]

output_path = base + '.txt'

with open(output_path, 'w') as f:

f.write(text)

return output_path

But need to handle each extractor function.

Now, for each function:

extract_txt and extract_md are the same: just read the file.

def extract_txt(file_path):

with open(file_path, 'r') as f:

return f.read()

Similarly for md.

Wait, but maybe .md files can be read the same way as .txt. So in code, if ext is 'md' or 'txt', just read the file.

extract_json:

def extract_json(file_path):

import json

with open(file_path, 'r') as f:

data = json.load(f)

return json.dumps(data, indent=2)

extract_csv:

def extract_csv(file_path):

import csv

text = []

with open(file_path, 'r') as f:

reader = csv.reader(f)

for row in reader:

text.append(', '.join(row))

return '\n'.join(text)

extract_pdf using PyPDF2:

def extract_pdf(file_path):

from PyPDF2 import PdfReader

reader = PdfReader(file_path)

text = []

for page in reader.pages:

page_text = page.extract_text()

if page_text:

text.append(page_text)

return '\n'.join(text)

extract_docx:

def extract_docx(file_path):

from docx import Document

doc = Document(file_path)

return '\n'.join([para.text for para in doc.paragraphs])

extract_xlsx:

def extract_xlsx(file_path):

from openpyxl import load_workbook

wb = load_workbook(filename=file_path, read_only=True)

text = []

for sheet in wb:

for row in sheet.iter_rows(values_only=True):

text.append('\t'.join(str(cell) for cell in row))

return '\n'.join(text)

extract_pptx:

def extract_pptx(file_path):

from pptx import Presentation

prs = Presentation(file_path)

text = []

for slide in prs.slides:

for shape in slide.shapes:

if hasattr(shape, "text"):

text.append(shape.text)

return '\n'.join(text)

For the LangChain fallback (doc, xls, ppt):

def extract_with_langchain(file_path):

from langchain.document_loaders import UnstructuredFileLoader

loader = UnstructuredFileLoader(file_path)

docs = loader.load()

return '\n'.join([doc.page_content for doc in docs])

But need to ensure that the necessary dependencies for unstructured are installed. For example, for .doc files, the unstructured library requires additional components. The user may need to install 'unstructured' and other dependencies like 'unstructured[local-inference]' or 'libmagic'.

This could complicate the setup, but according to the problem statement, the user is to install necessary libraries.

Now, error handling. For example, if a PDF is corrupted, or a DOCX file is invalid. Need to catch exceptions and return appropriate errors.

So in each extractor function, wrap the code in try-except blocks and propagate errors.

But in the main process_file function, handle exceptions and return error messages.

Also, Gradio expects the function to return either the output or an error message.

Now, putting it all together.

But wait, the file input in Gradio: when a user uploads a file, Gradio provides a temporary file path. The code needs to read from that path.

The Gradio interface would have a function that takes the file object, gets its path, and processes it.

But in Gradio, the file input component can return different things depending on the type. For example, using gr.File() gives a list of file paths, but if using gr.UploadButton or gr.File with type='filepath', it returns the path.

Assuming that the input is a single file path, the function will process it.

So the Gradio app would have:

import gradio as gr

allowed_extensions = {

'txt', 'md', 'json', 'csv', 'pdf',

'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'

}

def process_file(file_path):

# Check if the file exists

if not os.path.exists(file_path):

return "Error: File not found."

# Get file extension

ext = os.path.splitext(file_path)[1][1:].lower()

if ext not in allowed_extensions:

return f"Error: File type {ext} is not allowed."

try:

# Determine the extractor based on extension

if ext in ['txt', 'md']:

with open(file_path, 'r', encoding='utf-8') as f:

text = f.read()

elif ext == 'json':

text = extract_json(file_path)

elif ext == 'csv':

text = extract_csv(file_path)

elif ext == 'pdf':

text = extract_pdf(file_path)

elif ext == 'docx':

text = extract_docx(file_path)

elif ext == 'xlsx':

text = extract_xlsx(file_path)

elif ext == 'pptx':

text = extract_pptx(file_path)

else:  # doc, xls, ppt

text = extract_with_langchain(file_path)

# Save the text to a new file

base = os.path.splitext(file_path)[0]

output_path = f"{base}.txt"

with open(output_path, 'w', encoding='utf-8') as f:

f.write(text)

return f"File saved as {output_path}"

except Exception as e:

return f"Error processing file: {str(e)}"

Then, set up the Gradio interface:

with gr.Blocks() as app:

gr.Markdown("# File to Text Converter")

file_input = gr.File(label="Upload a file", file_types=list(allowed_extensions))

output = gr.Textbox(label="Output Message")

submit_btn = gr.Button("Convert")

submit_btn.click(

fn=process_file,

inputs=file_input,

outputs=output

)

But wait, in Gradio's gr.File, the file_types parameter expects a list of allowed extensions, each starting with a dot. For example, ['.txt', '.md', ...]. So in the code, allowed_extensions should be a list like ['.txt', '.md', ...], but the current allowed_extensions is a set of strings without dots.

So need to adjust that.

Also, the gr.File component returns a list of temporary file paths if multiple is allowed. Since we're expecting a single file, set file_count='single'.

Wait, perhaps the code should use gr.File with file_count='single' and file_types as the list of allowed extensions with dots.

So adjust the allowed_extensions to a list:

allowed_extensions = [

'.txt', '.md', '.json', '.csv', '.pdf',

'.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'

]

Then, in the gr.File component:

file_input = gr.File(label="Upload a file", file_types=allowed_extensions, file_count='single')

But when the user uploads a file, the file_input component's value is a dictionary with the 'name' key pointing to the temporary file path. Wait, in Gradio's newer versions, when using gr.File, the input is a list of files if multiple is allowed. But for file_count='single', it's a single file object. Wait, perhaps it's better to use gr.UploadButton with type='filepath' to get the path directly.

Alternatively, the code can handle the file input as a path. For example:

In the process_file function, the input is the file path. So the Gradio code would have:

file_input = gr.File(label="Upload a file", file_types=allowed_extensions, file_count='single')

But when the user uploads a file, the input to the function is a list of temporary file paths. Wait, no: in Gradio, when you use gr.File with file_count='single', the input is a single file object, which is a dictionary with 'name' and other keys, or perhaps the path directly. This depends on the Gradio version.

Alternatively, perhaps use gr.Textbox for the input filename, but that's not user-friendly. The better approach is to use gr.File and then extract the path from the uploaded file.

Wait, maybe the code should use the gr.File component and then in the process_file function, get the file path from the uploaded file's 'name' attribute.

Alternatively, use gr.UploadButton, which allows the user to upload a file, and returns the path as a string.

Let me check Gradio's documentation. For gr.File, when a user uploads a file, the component returns the path as a string if file_count is 'single'. Wait, no: in Gradio, the gr.File component returns a list of file objects when multiple is allowed, and a single file object when file_count is 'single'. Each file object is a dictionary with keys like 'name', 'size', etc. So to get the path, the code would need to access file_input.name.

Wait, perhaps the code should use the following:

file_input = gr.File(label="Upload file", file_types=allowed_extensions)

...

def process_file(file_obj):

file_path = file_obj.name

# process the file at file_path

But in newer versions of Gradio, the gr.File component returns a list of temp files when uploaded. Wait, maybe this is getting too complicated. Alternatively, use gr.components.File with type='filepath' which returns the path directly.

Wait, perhaps the correct approach is to use gr.File with type='filepath', which returns the path as a string. So the code would be:

file_input = gr.File(label="Upload a file", file_types=allowed_extensions, type='filepath')

Then, the process_file function would receive the file path as a string.

Yes, that makes sense. So the Gradio interface setup would be:

allowed_extensions = ['.txt', '.md', '.json', '.csv', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']

with gr.Blocks() as app:

gr.Markdown("# File to Text Converter")

file_input = gr.File(label="Upload a file", file_types=allowed_extensions, type='filepath')

submit_btn = gr.Button("Convert")

output = gr.Textbox(label="Output Message")

submit_btn.click(

fn=process_file,

inputs=file_input,

outputs=output

)

app.launch()

Now, the process_file function receives the file path as a string.

Now, error handling: if the user uploads a file with an allowed extension but the processing fails (e.g., a corrupt PDF), the code should catch exceptions and return an error message.

So in the process_file function, wrap everything in a try-except block.

Now, about saving the output file: the code saves it with the original filename plus .txt. But if the original file is in a read-only directory (like the temporary upload directory), saving might fail. So perhaps the code should save the output in the current working directory or a specific output directory, using the original filename.

But the problem statement says to save the output to a new file with the original filename appended with .txt. So if the input is "document.pdf", the output is "document.pdf.txt"? Or replace the extension? The user says "appended with a .txt suffix", which suggests adding .txt to the original filename. So "document.pdf" becomes "document.pdf.txt". But maybe the user wants to replace the existing extension. For example, "document.docx" becomes "document.txt". That would make more sense. So, better to split the filename into base and extension, then append .txt.

So, using os.path.splitext:

original_path = 'path/to/document.docx'

base, ext = os.path.splitext(original_path)

output_path = base + '.txt'

So for 'document.docx', output is 'document.txt'.

That's better. So in the code:

base = os.path.splitext(file_path)[0]

output_path = f"{base}.txt"

But the file_path may include directories. So when saving, it will be saved in the same directory as the input file. If the input is a temporary file (as in Gradio uploads), the output may not persist. Hmm, that's a problem. Because Gradio's uploaded files are stored in a temporary directory which may be cleaned up after the function returns. So saving the output in the same directory as the input (temporary) would result in the output file being deleted. So the code should save the output to a different directory, perhaps the current working directory, using the original filename.

But how to handle that. Maybe extract the original filename from the file_path, then save to the current directory.

Wait, but the user might want the output file to be saved in a specific location. The problem statement doesn't specify, but says to save it with the original filename plus .txt. So perhaps, regardless of the input file's path, save the output in the current working directory, using the original filename.

But the original filename may have a path. For example, if the input file is '/tmp/somefile.docx', then the output would be 'somefile.txt' in the current directory.

So to get the original filename without the path:

original_filename = os.path.basename(file_path)

base, ext = os.path.splitext(original_filename)

output_filename = base + '.txt'

output_path = os.path.join(os.getcwd(), output_filename)

But this could overwrite existing files. Alternatively, create a unique name, but the problem says to use the original filename appended with .txt. So perhaps the code should save the output in the current directory with the original name plus .txt.

But if the input file is in a temporary directory (like when uploaded via Gradio), the code must save the output to a permanent location. So the current working directory is a safe choice.

So in the code:

original_filename = os.path.basename(file_path)

base, ext = os.path.splitext(original_filename)

output_filename = base + '.txt'

output_path = os.path.join(os.getcwd(), output_filename)

But this could lead to overwriting if multiple files with the same name are processed. But according to the problem statement, the app should save the output with the original filename appended with .txt. So even if that means overwriting, that's up to the user.

Now, the code would save the output to the current working directory.

Now, putting all the pieces together.

Also, note that some libraries require specific installations. For example, python-docx, openpyxl, PyPDF2, python-pptx, langchain, and unstructured.

So the user needs to install these:

pip install gradio PyPDF2 python-docx openpyxl python-pptx langchain unstructured

Additionally, the unstructured library may require additional system dependencies. For example, for processing .doc files, unstructured requires libreoffice or other tools installed. So on Linux, you might need to install libreoffice. On Mac, perhaps via Homebrew. This could complicate things, but the problem statement says to use LangChain as a fallback, which uses these tools.

But that's beyond the code's control; the user must ensure the dependencies are met.

Now, error handling in each extractor function. For example, when processing a PDF, if PyPDF2 can't read it, the code should catch the exception and return an error.

But in the current code, the extractor functions are called within a try-except block in the process_file function. So any exceptions raised in the extractor functions will be caught there.

Now, writing the code with all these considerations.

Finally, the code should include inline comments explaining each major section.
