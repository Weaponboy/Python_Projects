import PyPDF2
from docx import Document

def extract_pdf_to_word(pdf_path, output_docx_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        
        # Extract text from each page
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Create a new Word document
        doc = Document()
        doc.add_paragraph(text)
        
        # Save the document
        doc.save(output_docx_path)
        print(f"Text extracted from {pdf_path} and saved to {output_docx_path}")

# Example usage
if __name__ == "__main__":
    pdf_file = "C:/Users/josha/Downloads/bookToConvert.pdf"
    word_file = "C:/Users/josha/Downloads/bookToConvert2.docx"
    extract_pdf_to_word(pdf_file, word_file)