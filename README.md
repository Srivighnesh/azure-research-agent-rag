# 🔎 Research Agent RAG

A document-based research assistant built with **Microsoft Foundry, Azure AI, Python, and Streamlit**.

Upload documents to an Azure vector store, then ask natural-language questions. A Foundry Agent uses **File Search** to retrieve relevant content from your documents and generate a grounded answer (Retrieval-Augmented Generation).

## Architecture

```text
                        USER
                          │
                          ▼
                 ┌─────────────────┐
                 │  Streamlit UI   │
                 └────────┬────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      UPLOAD DOCUMENT             ASK QUESTION
             │                         │
             ▼                         ▼
     DocumentService            FoundryService
     (validate file)                   │
             │                         ▼
             ▼                 Microsoft Foundry Agent
     FileSearchService                 │
             │                         ▼
             │                  File Search Tool
             ▼                         │
     ┌────────────────────┐            │
     │ Azure Vector Store │◄───────────┘
     └─────────┬──────────┘
               │  relevant content
               ▼
        Foundry Agent
               │
               ▼
     Grounded Answer → Streamlit UI
```

## Features

- Upload, list, and delete documents in the vector store
- File type and size validation (up to 512 MB)
- Ask questions and get answers grounded in your documents
- Modular service-based architecture
- Azure authentication via `DefaultAzureCredential` (no hardcoded secrets)

**Supported files:** PDF, TXT, Markdown, DOCX, PPTX, JSON, Python, Java, HTML

## Project Structure

```text
research-agent-rag/
├── app.py                  # Streamlit app
├── config/settings.py      # Environment configuration
├── services/
│   ├── foundry_service.py  # Foundry Agent communication
│   ├── file_service.py     # Vector store / File Search operations
│   └── document_service.py # File validation
├── components/             # Streamlit UI (chat, upload, citations)
├── utils/helpers.py
├── requirements.txt
└── .env
```

## Setup

**1. Clone and create a virtual environment**

```bash
git clone <YOUR_REPOSITORY_URL>
cd research-agent-rag
python -m venv .venv
.venv\Scripts\activate        # Windows
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Sign in to Azure** (account needs access to the Foundry project)

```bash
az login
```

**4. Create a `.env` file**

```env
AZURE_PROJECTS_ENDPOINT=YOUR_FOUNDRY_PROJECT_ENDPOINT
AGENT_NAME=YOUR_AGENT_NAME
VECTOR_STORE_ID=YOUR_VECTOR_STORE_ID
```

> Never commit `.env`. Add `.venv/`, `.env`, `__pycache__/`, and `*.pyc` to `.gitignore`.

**5. Run the app**

```bash
python -m streamlit run app.py
```

## Usage

1. Upload a document (e.g. `research_paper.pdf`).
2. Ask a question, e.g. *"What methodology was used in this research?"*
3. Read the answer generated from your document.

## Tech Stack

Python · Streamlit · Microsoft Foundry · Azure AI Projects SDK · Azure Identity · OpenAI SDK · File Search · python-dotenv

## Status

**Active development.**

In progress: reliable source/citation display, conversation history, persistent document metadata, and deployment.

Planned: multiple document collections, streaming responses, page-level citations, web search tool, and RAG evaluation.

## Author

**Sri Vignesh** — Generative AI · RAG · AI Agents · Azure · Python
