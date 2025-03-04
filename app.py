import os
from flask import Flask, render_template, request, send_file, redirect, url_for
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
from reportlab.pdfgen import canvas

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Merge PDFs
@app.route("/merge", methods=["POST"])
def merge_pdfs():
    uploaded_files = request.files.getlist("pdfs")
    merger = PyPDF2.PdfMerger()

    if not uploaded_files:
        return "No files uploaded", 400

    pdf_paths = []
    for file in uploaded_files:
        if file.filename.endswith(".pdf"):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            pdf_paths.append(file_path)
            merger.append(file_path)

    merged_pdf_path = os.path.join(PROCESSED_FOLDER, "merged.pdf")
    merger.write(merged_pdf_path)
    merger.close()

    return send_file(merged_pdf_path, as_attachment=True)

#  Split PDF (Extract Specific Pages)
@app.route("/split", methods=["POST"])
def split_pdf():
    file = request.files["pdf"]
    pages = request.form["pages"]  # Example: "1,3,5-7"

    if not file.filename.endswith(".pdf"):
        return "Invalid file format", 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()
    
    page_numbers = []
    for part in pages.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            page_numbers.extend(range(start - 1, end))
        else:
            page_numbers.append(int(part) - 1)

    for num in page_numbers:
        if num < len(reader.pages):
            writer.add_page(reader.pages[num])

    split_pdf_path = os.path.join(PROCESSED_FOLDER, "split.pdf")
    with open(split_pdf_path, "wb") as output_file:
        writer.write(output_file)

    return send_file(split_pdf_path, as_attachment=True)

#  Resize PDF Pages
@app.route("/resize", methods=["POST"])
def resize_pdf():
    file = request.files["pdf"]
    scale_factor = float(request.form["scale"])

    if not file.filename.endswith(".pdf"):
        return "Invalid file format", 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    images = convert_from_path(pdf_path)
    resized_images = []
    
    for img in images:
        width, height = img.size
        new_size = (int(width * scale_factor), int(height * scale_factor))
        resized_images.append(img.resize(new_size, Image.ANTIALIAS))

    resized_pdf_path = os.path.join(PROCESSED_FOLDER, "resized.pdf")
    resized_images[0].save(resized_pdf_path, save_all=True, append_images=resized_images[1:])

    return send_file(resized_pdf_path, as_attachment=True)

#  Compress PDF (Reduce File Size)
@app.route("/compress", methods=["POST"])
def compress_pdf():
    file = request.files["pdf"]

    if not file.filename.endswith(".pdf"):
        return "Invalid file format", 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    images = convert_from_path(pdf_path)
    compressed_images = []

    for img in images:
        img = img.convert("RGB")
        compressed_images.append(img)

    compressed_pdf_path = os.path.join(PROCESSED_FOLDER, "compressed.pdf")
    compressed_images[0].save(compressed_pdf_path, save_all=True, append_images=compressed_images[1:], quality=50)

    return send_file(compressed_pdf_path, as_attachment=True)

#    Extract Text from PDF
@app.route("/extract", methods=["POST"])
def extract_text():
    file = request.files["pdf"]

    if not file.filename.endswith(".pdf"):
        return "Invalid file format", 400

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    reader = PyPDF2.PdfReader(pdf_path)
    extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    text_file_path = os.path.join(PROCESSED_FOLDER, "extracted_text.txt")
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    return send_file(text_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
