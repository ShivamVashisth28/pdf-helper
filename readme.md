# PDF Helper

A Flask-based web application for performing various operations on PDF files, such as merging, splitting, resizing, compressing, and extracting text.

## Features

- **Merge PDFs**: Combine multiple PDF files into a single PDF.
- **Split PDF**: Extract specific pages or a range of pages from a PDF.
- **Resize PDF Pages**: Scale the size of PDF pages by a specified factor.
- **Compress PDF**: Reduce the file size of a PDF by compressing its images.
- **Extract Text**: Extract text content from a PDF and save it as a `.txt` file.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- PyPDF2
- pdf2image
- Pillow
- reportlab

1. You can install the required Python packages using `pip`:

```bash
pip install Flask PyPDF2 pdf2image Pillow reportlab
```

2. Clone the Repository 

```bash
git clone https://github.com/yourusername/pdf-manipulation-tool.git
cd pdf-manipulation-tool
```

3. Run the Flash App

```bash
python app.py
```

4. Access the application:
```
Open your web browser and go to http://127.0.0.1:5000/ to use the tool. 
```
5. Upload PDFs and perform operations:

```
Use the web interface to upload PDF files and select the desired operation (merge, split, resize, compress, or extract text).
```
6. Download the processed files directly from the browser.


# Example Usage
## Merge PDFs
1. Upload multiple PDF files.

2. Click "Merge PDFs".

3. Download the merged PDF.

## Split PDF
1. Upload a PDF file.

2. Specify the pages to extract (e.g., 1,3,5-7).

3. Click "Split PDF".

4. Download the extracted pages as a new PDF.

## Resize PDF
1. Upload a PDF file.

2. Enter a scale factor (e.g., 0.8 for 80% of the original size).

3. Click "Resize PDF".

4. Download the resized PDF.

## Compress PDF
1. Upload a PDF file.

2. Click "Compress PDF".

3. Download the compressed PDF.

## Extract Text
1. Upload a PDF file.

2. Click "Extract Text".

3. Download the extracted text as a .txt file.