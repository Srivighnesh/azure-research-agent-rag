from pathlib import Path

class DocumentService:

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".txt",
        ".md",
        ".docx",
        ".pptx",
        ".json",
        ".py",
        ".java",
        ".html",
    }

    MAX_FILE_SIZE = 512 * 1024 * 1024  # 512 MB

    def __init__(self):
        pass

    def validate_file(self, uploaded_file) -> None:
        """
        Validate a Streamlit UploadedFile before sending it to Foundry.
        """

        if uploaded_file is None:
            raise ValueError("No file was provided.")

        filename = uploaded_file.name

        extension = Path(filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        file_size = uploaded_file.size

        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(
                "File is larger than the 512 MB limit."
            )

    def get_filename(self, uploaded_file) -> str:
        """
        Return the uploaded file name.
        """
        return uploaded_file.name