# AffineSurge - Tri9T AI Engineering Internship Assignment

## Project Overview
AffineSurge is a FastAPI-based application for document version management, search, comparison, and AI-powered artifact generation (test cases, requirements, traceability matrix).

## Architecture
- **API Layer**: FastAPI routes for all endpoints
- **Service Layer**: Business logic for documents, selections, generation
- **Data Layer**: SQLAlchemy ORM for SQLite, optional MongoDB for generated artifacts
- **LLM Layer**: Gemini/OpenAI integration for content generation
- **Parser Layer**: PDF parsing and hierarchy extraction

## Setup Instructions

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
- Copy `.env.example` to `.env`
- Add your API keys (GEMINI_API_KEY or OPENAI_API_KEY)
- Optional: Configure MongoDB URI

3. **Run the Server**
```bash
uvicorn app.main:app --reload
```

4. **Access API Docs**
Open http://localhost:8000/docs in your browser

## API List

### Documents
- `GET /documents/` - List all documents
- `GET /documents/{document_id}` - Get document details
- `GET /documents/{document_id}/versions` - List document versions
- `GET /documents/versions/{version_id}/nodes` - Get nodes for a version

### Search
- `GET /search?q={query}` - Search nodes by heading, body, or section number

### Compare
- `GET /compare?version1={id}&version2={id}` - Compare two document versions

### Selections
- `POST /selections/` - Create a new selection of nodes
- `GET /selections/` - List all selections
- `GET /selections/{selection_id}` - Get selection details

### Generation
- `POST /generate` - Generate an artifact (test_cases, requirements, traceability_matrix) from a selection
- `GET /generated/{generation_id}` - Retrieve a previously generated artifact
- `GET /staleness/{generation_id}` - Check if a generated artifact is stale

## How Versioning Works
Each time a PDF is ingested, a new DocumentVersion is created. Nodes are parsed and stored with content hashes for change detection.

## How Search Works
Search uses SQLAlchemy ilike queries on node heading, body, and section number. Results are ordered by node order.

## How Compare Works
Compares nodes from two versions using logical node IDs and content hashes to detect additions, deletions, and modifications.

## How Generation Works
1. Loads a selection and its nodes
2. Combines node content into a prompt
3. Calls configured LLM (Gemini or OpenAI)
4. Stores generated artifact with source hash for staleness detection
5. Supports MongoDB or JSON file storage
