import pdfplumber
from docx import Document

def extract_pdf_to_word(pdf_path, output_docx_path):
    # Create a new Word document
    doc = Document()
    
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from each page
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Add extracted text as a paragraph
                doc.add_paragraph(text)
                # Add a page break after each page's text, except for the last page
                if i < len(pdf.pages) - 1:
                    doc.add_page_break()
    
    # Save the document
    doc.save(output_docx_path)
    print(f"Text extracted from {pdf_path} and saved to {output_docx_path}")

# Example usage
if __name__ == "__main__":
    pdf_file = r"C:\Users\josha\Downloads\bookToConvert.pdf"  # Use raw string
    word_file = r"C:\Users\josha\Downloads\bookToConvert4.docx"  # Use raw string
    extract_pdf_to_word(pdf_file, word_file)