https://chatgpt.com/share/67c006ad-186c-8000-b7b4-742b63778b6b

Here is your updated prompt in the **C.R.A.F.T.** format:

---

**Context:**  
You are tasked with developing a Python application that uses the Gradio library to provide a web UI. This interface should prompt the user for an input filename and then convert the content of the file into plain text. The application must verify the file type before processing—allowing files that are inherently text-based (such as plain text, markdown, JSON, CSV, PDF) as well as typical Microsoft Office file types (e.g., DOC, DOCX, XLS, XLSX, PPT, PPTX). For each file type, the program should use the most compatible Python library or libraries to extract the full text content. In cases where no specialized file converter library is available for the file type, the app should default to using LangChain to ensure complete text extraction.

**Role:**  
You are a top-tier Python developer and AI systems integrator with over two decades of experience in creating robust, user-friendly applications. Your expertise includes web UI development with Gradio, file handling in Python, text extraction techniques using various libraries, and integrating advanced frameworks such as LangChain when needed. You will provide a detailed, step-by-step solution that covers all aspects of the application’s functionality.

**Action:**  
1. **Initialize the Project:**  
   - Set up a new Python project and install necessary libraries, including Gradio, LangChain (if required), and any file processing libraries (e.g., PyPDF2 for PDFs, markdown2 for Markdown, python-docx for DOCX files, openpyxl for XLSX files, etc.).
2. **Design the Web UI:**  
   - Use Gradio to create a simple user interface that accepts an input filename.
3. **File Type Validation:**  
   - Implement logic to check the file extension. Allow files with extensions such as `.txt`, `.md`, `.json`, `.csv`, `.pdf` as well as typical Microsoft Office file types like `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, and `.pptx`.
   - If the file extension does not match any of these allowed types, trigger an error message popup in the UI.
4. **File Content Extraction:**  
   - For each allowed file type, integrate the most compatible Python library or libraries to extract the full text content.  
   - If no specialized library exists for a specific file type, use LangChain as the fallback solution to extract content.
5. **File Saving:**  
   - Once text is successfully extracted, save the output to a new file with the original filename appended with a `.txt` suffix.
6. **Error Handling and User Feedback:**  
   - Ensure the app gracefully handles any errors that occur during file validation or content extraction, providing clear feedback to the user.

**Format:**  
- Provide the solution as well-documented Python code, using markdown formatting for clarity.  
- Include inline comments and a brief explanation of each major code section.  
- Optionally, present the solution in a step-by-step tutorial format, ensuring it is accessible even to developers with intermediate Python skills.

**Target Audience:**  
This prompt is intended for advanced AI systems (such as ChatGPT 4.0, ChatGPT 3.5, Google Gemini, Claude AI, Copilot, or DeepSeek) that are capable of generating complex, detailed code examples and technical documentation. The audience includes experienced developers and AI engineers looking to implement robust file processing applications with dynamic web interfaces.
