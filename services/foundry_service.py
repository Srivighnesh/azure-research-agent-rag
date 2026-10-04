from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from config.settings import PROJECT_ENDPOINT, AGENT_NAME


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

    def ask_question(self, question):

        response = self.client.responses.create(
            conversation=self.conversation.id,
            input=question
        )
        sources = []

        for item in response.output:
            for content in getattr(item, "content", []):
                for a in getattr(content, "annotations", []):
                    if getattr(a, "type", "") == "file_citation":
                        sources.append(a.filename)

        return response.output_text, sources