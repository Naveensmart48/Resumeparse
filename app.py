import re
import os
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for
import PyPDF2
import docx

app = Flask(__name__)

def extract_information(resume_text):
    """Extract structured information from resume text."""
    print("[DEBUG] Starting resume extraction process")
    information = {}

    # Extract Name
    name_match = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", resume_text)
    information['Name'] = name_match.group(0).strip() if name_match else "No Name Found"

    # Extract Phone Number
    phone_match = re.search(r"\+?\d{1,3}?[-.\s]?\(?\d{2,4}?\)?[-.\s]?\d{3,4}[-.\s]?\d{4,6}", resume_text)
    information['Phone'] = phone_match.group(0).strip() if phone_match else "No Phone Found"

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
    information['Email'] = email_match.group(0).strip() if email_match else "No Email Found"

    # Extract Location
    location_match = re.search(r"(?:Location|Address)\s*:\s*(.*)", resume_text, re.IGNORECASE)
    information['Location'] = location_match.group(1).strip() if location_match else "No Location Found"

    # Extract Education
    education_section = re.search(r"Education\s*(.*?)\s*(?:Skills|CERTIFICATIONS|Experience|$)", resume_text, re.DOTALL)
    information['Education'] = education_section.group(1).strip().replace("\n", " ") if education_section else "No Education Found"

    # Extract Skills
    skills_section = re.findall(r"\b(?:Python|Flask|React|JavaScript|SQL|Docker|Git)\b", resume_text, re.IGNORECASE)
    information['Skills'] = ", ".join(set(skills_section)) if skills_section else "No Skills Found"

    # Extract Certifications
    certifications_section = re.search(r"CERTIFICATIONS\s*(.*?)\s*(?:Experience|$)", resume_text, re.DOTALL)
    information['Certifications'] = certifications_section.group(1).strip().replace("\n", " ") if certifications_section else "No Certifications Found"

    # Extract Experience
    experience_section = re.search(r"Experience\s*(.*?)\s*(?:Projects|Education|$)", resume_text, re.DOTALL)
    information['Experience'] = experience_section.group(1).strip().replace("\n", " ") if experience_section else "No Experience Found"

    print(f"[DEBUG] Extracted Information: {information}")  # Debugging extracted info
    return information

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        print("[DEBUG] Received POST request to extract resume")
        
        resume_text = request.form.get("resume_text", "").strip()
        file = request.files.get("resume_file")

        # ✅ Handle File Upload
        if file and file.filename:
            print(f"[DEBUG] File uploaded: {file.filename}")
            file_extension = file.filename.split(".")[-1].lower()
            text = ""

            if file_extension == "pdf":
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
            elif file_extension in ["docx", "doc"]:
                doc = docx.Document(file)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            elif file_extension == "txt":
                text = file.read().decode("utf-8")
            else:
                return jsonify({'error': 'Unsupported file type'}), 400

            resume_text = text.strip()  # ✅ Extract text from file

        if not resume_text:
            print("[ERROR] No resume provided")
            return jsonify({'error': 'No resume provided'}), 400

        extracted_info = extract_information(resume_text)
        print("[DEBUG] Redirecting to results page with extracted information")
        return render_template('results.html', extracted_info=extracted_info)

    print("[DEBUG] Rendering upload page")
    return render_template('upload.html')

if __name__ == '__main__':
    print("[INFO] Starting Flask Application...")
    app.run(debug=True)
