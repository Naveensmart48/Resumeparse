import re
import os  # For file handling
from flask import Flask, render_template, request, jsonify  # For web interface

app = Flask(__name__)

# ... (rest of the extract_information function from before goes here) ...

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    extracted_info = {}  # Initialize

    if request.method == 'POST':
        if 'resume_file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['resume_file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            try:
                filename = file.filename
                filepath = os.path.join(app.root_path, filename) #saves file in the same directory as the script
                file.save(filepath) #saves the uploaded file

                file_extension = filename.split(".")[-1].lower()  # Get file extension

                text = ""

                if file_extension == "pdf":
                    import PyPDF2 #you need to install PyPDF2 using pip install PyPDF2
                    pdf_reader = PyPDF2.PdfReader(filepath)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
                elif file_extension in ["docx", "doc"]: #you need to install python-docx using pip install python-docx
                    import docx
                    doc = docx.Document(filepath)
                    for paragraph in doc.paragraphs:
                        text += paragraph.text + "\n"
                elif file_extension == "txt":
                    with open(filepath, 'r', encoding='utf-8') as f: #adding encoding to handle different characters
                        text = f.read()
                else:
                    return jsonify({'error': 'Unsupported file type'})
                
                extracted_info = extract_information(text)
                os.remove(filepath) #deletes the uploaded file after processing

                return jsonify(extracted_info) #returns the extracted information as a json

            except Exception as e:
                return jsonify({'error': str(e)}) #returns the error as a json

    return render_template('upload.html', extracted_info=extracted_info) #renders the upload.html template


if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False in production