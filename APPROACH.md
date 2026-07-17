# Tri9T AI Engineering Internship Assignment - Approach Documentation

## 1. Architecture Decisions

### 1.1 Clean Architecture
The project follows a layered clean architecture to ensure separation of concerns and maintainability:
- **API Layer (`app/api/`)**: FastAPI routes that handle HTTP requests and responses
- **Service Layer (`app/services/`)**: Core business logic for documents, selections, and version comparison
- **Data Model Layer (`app/models/`)**: SQLAlchemy ORM models defining database schema
- **LLM Layer (`app/llm/`)**: Encapsulated logic for LLM interaction and artifact storage
- **Parser Layer (`app/parser/`)**: Existing PDF parsing and hierarchy extraction logic
- **Schema Layer (`app/schemas/`)**: Pydantic models for request/response validation

### 1.2 Key Principles
- **Dependency Inversion**: Services interact with databases and LLMs through abstractions (where possible)
- **Fallback Mechanisms**: JSON file storage as a fallback if MongoDB is not configured
- **Backward Compatibility**: Preserved all existing working APIs and code structure

---

## 2. Database Design

### 2.1 Primary Database (SQLite)
SQLite was chosen for its simplicity, file-based storage, and seamless integration with SQLAlchemy:
- **`documents` table**: Stores document metadata (id, name, description, created_at)
- **`document_versions` table**: Tracks version history (id, document_id, version_number, file_name, created_at)
- **`nodes` table**: Stores parsed content with logical IDs, hashes, and hierarchical relationships (id, version_id, parent_id, logical_node_id, heading, body, level, section_number, content_hash, node_order, created_at)
- **`selections` table**: Stores named selections of nodes (id, selection_name, version_id, created_at)
- **`selection_nodes` table**: Junction table for many-to-many relationship between selections and nodes (id, selection_id, node_id)
- **`generation_references` table**: Metadata for generated artifacts (id, selection_id, artifact_type, mongo_document_id, json_file_path, source_hash, created_at)

### 2.2 Optional Database (MongoDB)
MongoDB is used as an optional storage backend for generated artifacts:
- Stores full generated content (test cases, requirements, traceability matrix)
- Falls back to JSON file storage in `generated_artifacts/` directory if MongoDB is unavailable
- Uses `mongo_document_id` and `json_file_path` in `generation_references` to track storage location

---

## 3. Versioning Strategy

### 3.1 Document Versioning
- Each PDF ingestion creates a new `document_version` with incrementing `version_number`
- Versions are tied to a specific document
- File name and creation timestamp are stored for audit

### 3.2 Node Versioning
- Each node has a `content_hash` (SHA-256) computed from normalized heading + body
- Nodes are linked to a specific `document_version`
- `logical_node_id` allows tracking the same logical section across versions
- `node_order` maintains the original document structure order

---

## 4. Selection Strategy

### 4.1 Selection Creation
- POST `/selections` accepts `selection_name`, `version_id`, and list of `node_ids`
- All `node_ids` are validated to exist and belong to the specified `version_id`
- Selection metadata is stored in SQLite `selections` table
- Node associations are stored in `selection_nodes` junction table

### 4.2 Selection Retrieval
- GET `/selections` lists all selections
- GET `/selections/{id}` retrieves a specific selection with its node IDs
- Selections are immutable once created (tied to a specific version)

---

## 5. Generation Strategy

### 5.1 Artifact Types
Supports three artifact types:
1. **test_cases**: Comprehensive test cases based on selected content
2. **requirements**: Extracted and formalized requirements
3. **traceability_matrix**: Traceability between requirements and sections

### 5.2 LLM Integration
- Supports both Google Gemini and OpenAI LLMs
- Uses environment variables (`GEMINI_API_KEY`, `OPENAI_API_KEY`) for authentication
- Prompt is constructed by combining selected nodes' headings and bodies
- Prompt templates are tailored per artifact type

### 5.3 Source Hash
- Computed by combining `content_hash` of all selected nodes (sorted by node ID)
- Stored with the generated artifact for staleness detection

### 5.4 Storage
- **MongoDB (Preferred)**: Stores artifact in `tri9t.artifacts` collection
- **JSON File (Fallback)**: Stores artifact in `generated_artifacts/` directory as JSON file
- Storage method is tracked in `generation_references` table

---

## 6. Staleness Strategy

### 6.1 Detection Logic
- GET `/staleness/{generated_id}` retrieves the generation reference
- Computes current source hash from the selection's nodes
- Compares current hash with stored `source_hash`
- Returns `stale: true` if hashes differ

### 6.2 Changed Nodes
- Returns list of node IDs from the selection (simplified for this implementation)
- More granular change detection can be added by comparing individual node hashes

---

## 7. Key Implementation Details

- **Maintained Existing Code**: No changes to existing PDF parser, version comparison, or search APIs
- **SQLAlchemy ORM**: All database operations use SQLAlchemy for consistency
- **Pydantic Schemas**: All request/response payloads are validated with Pydantic
- **Environment Variables**: Uses `python-dotenv` to load configuration
- **Gitignore**: Ignores sensitive files (`.env`, `tri9t.db`, `__pycache__`, `generated_artifacts/`)
