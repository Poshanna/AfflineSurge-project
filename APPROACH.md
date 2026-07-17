# Approach Documentation

## Architecture Decisions
- **Clean Architecture**: Separated API, service, model, and LLM layers for maintainability
- **Dependency Inversion**: Services depend on abstractions, not concrete implementations
- **Fallback Mechanisms**: JSON storage fallback if MongoDB unavailable

## Database Design
- **SQLite**: Primary database for documents, versions, nodes, selections, generation references
- **Tables**:
  - `documents`: Document metadata
  - `document_versions`: Version history
  - `nodes`: Parsed content with logical IDs and hashes
  - `selections`: Named node selections
  - `selection_nodes`: Junction table for selection-node mapping
  - `generation_references`: Metadata for generated artifacts
- **MongoDB (Optional)**: Stores actual generated artifact content

## Versioning Strategy
- Semantic version numbering per document
- Content hashing for change detection
- Logical node IDs to track same sections across versions

## Selection Strategy
- Selections are tied to a specific document version
- Node IDs are validated to belong to the specified version
- Selection metadata stored in SQLite

## Generation Strategy
- Prompt engineering per artifact type
- Support for both Gemini and OpenAI LLMs
- Source hash computed from combined node hashes
- Flexible storage backend (MongoDB or JSON files)

## Staleness Strategy
- Compares stored source hash with current node hashes
- Marks artifact as stale if hashes differ
- Returns list of potentially changed nodes
