import re

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai import BadRequestError
from config.settings import PROJECT_ENDPOINT, AGENT_NAME

CITATION_PATTERN = re.compile(r"【[^】]*】")


class FoundryService:

    def __init__(self):
        self.project = AIProjectClient(
            endpoint=PROJECT_ENDPOINT,
            credential=DefaultAzureCredential(),
        )

        self.client = self.project.get_openai_client(
            agent_name=AGENT_NAME
        )

        # Create one conversation
        self.conversation = self.client.conversations.create()

    @staticmethod
    def _clean_text(text: str) -> str:
        """Remove raw markers like 【12:1†source】."""
        text = CITATION_PATTERN.sub("", text)
        text = re.sub(r"\s+([.,;:])", r"\1", text)  # no space before punctuation
        text = re.sub(r"[ \t]{2,}", " ", text)      # collapse double spaces
        return text.strip()

    def ask_question(self, question):
        try:
            response = self.client.responses.create(
                conversation=self.conversation.id,
                input=question
            )
        except BadRequestError as e:
            if "content_filter" in str(e):
                return ("This question was blocked by the content filter "
                    "(it detected personal names). Try rephrasing it.", [])
            
        sources = []

        for item in response.output:
            for content in getattr(item, "content", None) or []:
                for a in getattr(content, "annotations", None) or []:
                    if getattr(a, "type", "") == "file_citation":
                        filename = getattr(a, "filename", None)
                        if filename:
                            sources.append(filename)

        answer = self._clean_text(response.output_text)
        unique_sources = list(dict.fromkeys(sources))  # dedupe, keep order

        return answer, unique_sources