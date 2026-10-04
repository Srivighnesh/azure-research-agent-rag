import os
import tempfile
from pathlib import Path
from urllib import response

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from config.settings import PROJECT_ENDPOINT


class FileSearchService:

    def __init__(self):
        self.project = AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=DefaultAzureCredential()
        )
        self.file_names = {}
        self.client = self.project.get_openai_client()

    def upload_file(self, vector_store_id: str, uploaded_file):

        file_name = uploaded_file.name
        file_bytes = uploaded_file.getvalue()
        suffix = Path(file_name).suffix

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
            ) as temp_file:

                temp_file.write(file_bytes)
                temp_path = temp_file.name

            with open(temp_path, "rb") as file_handle:

                result = self.client.vector_stores.files.upload_and_poll(
                    vector_store_id=vector_store_id,
                    file=file_handle
                )

            # self.file_names[result.id] = file_name

            return result

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    def get_vector_store(self, vector_store_id: str):

        return self.client.vector_stores.retrieve(
            vector_store_id
        )

    def list_files(self, vector_store_id: str):
        return self.client.vector_stores.files.list(vector_store_id)

    def delete_file(self, vector_store_id: str, file_id:str):
        return self.client.vector_stores.files.delete(
            vector_store_id=vector_store_id,
            file_id=file_id
        )