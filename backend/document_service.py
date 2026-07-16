"""
document_service.py

Reads uploaded documents.
"""

from PyPDF2 import PdfReader

from docx import Document


class DocumentService:

    def read_document(
        self,
        uploaded_file
    ):

        """
        Read uploaded file and return text.
        """

        if uploaded_file is None:
            return ""

        file_name = uploaded_file.name.lower()

        # ---------------- PDF ----------------

        if file_name.endswith(".pdf"):

            pdf = PdfReader(uploaded_file)

            text = ""

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

            return text

        # ---------------- DOCX ----------------

        elif file_name.endswith(".docx"):

            doc = Document(uploaded_file)

            text = ""

            for paragraph in doc.paragraphs:

                text += paragraph.text + "\n"

            return text

        # ---------------- TXT ----------------

        elif file_name.endswith(".txt"):

            return uploaded_file.read().decode("utf-8")

        else:

            return ""


document_service = DocumentService()