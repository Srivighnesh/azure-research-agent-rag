# 🔎 Research Agent RAG

A document-based research assistant built with **Microsoft Foundry, Azure AI Search, Azure Blob Storage, Python, and Streamlit**.

Documents are stored in **Azure Blob Storage** and indexed by **Azure AI Search**, which acts as the knowledge base. Ask natural-language questions and a Foundry Agent uses the **Azure AI Search tool** to retrieve relevant content and generate a grounded answer (Retrieval-Augmented Generation).

## Architecture

```text
   Document owners                         USER
          │                                  │
          ▼                                  ▼
 ┌──────────────────┐               ┌─────────────────┐
 │ Azure Blob       │               │  Streamlit UI   │
 │ Storage          │               └────────┬────────┘
 │ (source docs)    │                        │ question
 └────────┬─────────┘                        ▼
          │ indexer                    FoundryService
          ▼                                  │
 ┌──────────────────┐                        ▼
 │ Azure AI Search  │◄──── retrieval ── Microsoft Foundry Agent
 │ (knowledge base) │   (AI Search tool)      │
 └──────────────────┘                        ▼
                                  Grounded Answer + Citations
                                             │
                                             ▼
                                        Streamlit UI
```

**Ingestion** (outside the app): upload files to the Blob container, and the Azure AI Search indexer chunks, embeds, and indexes them automatically.
**Query** (inside the app): the user asks a question, the agent searches the index, and the answer comes back with sources.

## Features

- Ask questions and get answers grounded in your indexed documents
- Azure AI Search as the knowledge base (hybrid keyword + vector search)
- Documents managed in Azure Blob Storage (add or remove files without touching the app)
- Source and citation display, with links back to the blob file
- Modular service-based architecture
- Azure authentication via `DefaultAzureCredential` (no hardcoded secrets)

**Supported files:** PDF, TXT, Markdown, DOCX, PPTX, JSON, HTML

## Project Structure

```text
research-agent-rag/
├── app.py                  # Streamlit app (chat UI only)
├── config/settings.py      # Environment configuration
├── services/
│   ├── foundry_service.py  # Foundry Agent communication
│   ├── search_service.py   # Azure AI Search queries / index info
├── components/             # Streamlit UI (chat, citations)
├── utils/helpers.py
├── requirements.txt
└── .env
```

## Prerequisites

- A Microsoft Foundry project with an agent deployed
- An Azure Storage account with a container holding your documents
- An Azure AI Search service with:
  - a data source pointing to the Blob container
  - an indexer and index (with vector field recommended)
- The AI Search service added as a **connection** in your Foundry project
- RBAC roles for your identity:
  - `Search Index Data Reader` on the Search service
  - `Storage Blob Data Reader` on the storage account
  - Access to the Foundry project

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

**3. Sign in to Azure**

```bash
az login
```

**4. Create a `.env` file**

```env
AZURE_PROJECTS_ENDPOINT=YOUR_FOUNDRY_PROJECT_ENDPOINT
AGENT_NAME=YOUR_AGENT_NAME

# Azure AI Search (knowledge base)
AI_SEARCH_CONNECTION_NAME=YOUR_FOUNDRY_SEARCH_CONNECTION
AI_SEARCH_ENDPOINT=https://YOUR_SERVICE.search.windows.net
AI_SEARCH_INDEX_NAME=YOUR_INDEX_NAME

# Azure Blob Storage (document source)
AZURE_STORAGE_ACCOUNT_URL=https://YOUR_ACCOUNT.blob.core.windows.net
AZURE_STORAGE_CONTAINER=YOUR_CONTAINER_NAME
```

> Never commit `.env`. Add `.venv/`, `.env`, `__pycache__/`, and `*.pyc` to `.gitignore`.

**5. Run the app**

```bash
python -m streamlit run app.py
```

## Managing Documents

Documents are no longer uploaded through the app.

1. Upload or delete files in the Blob container (Azure Portal, Storage Explorer, `azcopy`, or a pipeline).
2. The Azure AI Search indexer picks up changes on its schedule (or run it manually).
3. New content is available to the agent once indexing completes.

## Usage

1. Make sure your documents are in Blob Storage and indexed.
2. Ask a question, e.g. *"What methodology was used in this research?"*
3. Read the answer and check the cited sources.

## Tech Stack

Python · Streamlit · Microsoft Foundry · Azure AI Search · Azure Blob Storage · Azure AI Projects SDK · Azure Identity · azure-search-documents · azure-storage-blob · python-dotenv

## Status

**Active development.**

In progress: reliable source/citation display, conversation history, and deployment.

Planned: multiple indexes/collections, streaming responses, page-level citations, web search tool, and RAG evaluation.

## Author

**Sri Vignesh** — Generative AI · RAG · AI Agents · Azure · Python
