# Ewakili Legal Research Agent

A sophisticated AI-powered legal research assistant specialized in East African jurisprudence, particularly Kenyan, Ugandan, and Tanzanian law. The system uses embedding-based semantic search with Neo4j database to provide comprehensive legal analysis and case law research.

## Overview

The Ewakili Legal Research Agent is designed to assist legal practitioners, researchers, and students in finding relevant case law, analyzing legal principles, and understanding judicial precedents across East African jurisdictions. It combines advanced AI capabilities with a robust legal database to deliver accurate, contextual legal research.

## Features

- **Semantic Search**: Advanced embedding-based similarity search for legal concepts
- **Multi-jurisdictional Support**: Focus on Kenya, Uganda, Tanzania, and other East African jurisdictions
- **Comprehensive Case Analysis**: Multiple search approaches including:
  - Legal principle-based searches
  - Case summary analysis
  - Statutory law application
  - Legal precedent research
  - Issue-based analysis
  - Prayer/relief analysis
- **Neo4j Integration**: High-performance graph database for complex legal relationships
- **AI-Powered Analysis**: Uses Google's Gemini models for natural language understanding
- **Professional Citations**: Proper legal citation formats for East African jurisdictions

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Legal Agent    │───▶│   Neo4j DB      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Toolbox Server  │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Embedding API   │
                       └─────────────────┘
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Neo4j Database (4.0+)
- Google Cloud Project with Vertex AI API enabled
- Docker (for Neo4j if using containerized setup)

### Dependencies

Install the required Python packages:

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### System Requirements

**Minimum Requirements:**
- Python 3.8+
- 8GB RAM (16GB recommended)
- 10GB free disk space
- Neo4j 4.0+ with APOC and GDS plugins
- Internet connection for Google AI services

**Recommended Setup:**
- Python 3.10+
- 16GB RAM
- SSD storage
- Docker for containerized services
- Linux/macOS (Windows supported but not optimal)

### Key Dependencies

- `langchain-google-genai`: Google Generative AI integration
- `langgraph`: Agent framework for complex workflows
- `toolbox-langchain`: Custom toolbox for legal research tools
- `neo4j`: Neo4j database driver
- `google-generativeai`: Google's generative AI SDK

### Health Checks

After installation, verify all components:

```bash
# Check Python version
python --version

# Verify Neo4j connection
python -c "from neo4j import GraphDatabase; print('Neo4j driver OK')"

# Test Google AI authentication
python -c "import google.generativeai as genai; print('Google AI SDK OK')"

# Verify toolbox connectivity
curl -s http://localhost:5000/health || echo "Toolbox server not running"
```

## Setup

### 1. Neo4j Database Configuration

Configure your Neo4j database connection in `tools.yaml`:

```yaml
sources:
  legal_db:
    kind: "neo4j"
    uri: "bolt://localhost:7687"  # or your Neo4j instance
    user: "neo4j"
    password: "your_password"
    database: "neo4j"
```

### 2. Google Cloud Authentication

Set up authentication using one of these methods:

#### Option A: Service Account Key
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service_account_key.json"
```

#### Option B: API Key
```bash
export GOOGLE_API_KEY="your_google_api_key"
```

### 3. Toolbox Server Setup

The toolbox server is required to run the legal research tools. Follow these steps to set it up:

#### Starting the Toolbox Server

1. **Navigate to the toolbox directory** (if toolbox is in a separate directory):
   ```bash
   cd /path/to/toolbox
   ```

2. **Start the toolbox server**:
   ```bash
   # Option 1: Using the toolbox binary (if available)
   ./toolbox serve --port 5000 --config ../ewakili_agent/tools.yaml
   
   # Option 2: Using Python toolbox module
   python -m toolbox serve --port 5000 --config ../ewakili_agent/tools.yaml
   
   # Option 3: Direct execution (if toolbox is executable)
   toolbox serve --port 5000 --config tools.yaml
   ```

3. **Verify the server is running**:
   ```bash
   # Check if the server is responding
   curl http://localhost:5000/health
   
   # Or check the tools endpoint
   curl http://localhost:5000/tools
   ```

#### Toolbox Configuration

The toolbox server reads configuration from `tools.yaml` and connects to your Neo4j database. Ensure:

- Neo4j is running and accessible
- Database credentials are correct in `tools.yaml`
- All required Neo4j plugins are installed (APOC, GDS)

#### Alternative: Docker Setup

If you prefer using Docker for the toolbox:

```bash
# Build the toolbox container (if Dockerfile is available)
docker build -t legal-toolbox .

# Run the toolbox container
docker run -p 5000:5000 -v $(pwd)/tools.yaml:/app/tools.yaml legal-toolbox

# Or using docker-compose (if available)
docker-compose up toolbox
```

## Quick Start Guide

### Step-by-Step System Startup

Follow these steps to get the complete system running:

#### 1. Start Neo4j Database

**Option A: Using Docker**
```bash
# Start Neo4j with required plugins
docker run -d \
  --name neo4j-legal \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/f7DEfxd9wy5. \
  -e NEO4J_PLUGINS='["apoc", "graph-data-science"]' \
  -v neo4j_data:/data \
  neo4j:5.0
```

**Option B: Using Local Installation**
```bash
# Start Neo4j service
sudo systemctl start neo4j

# Or if using Neo4j Desktop, start the database from the interface
```

#### 2. Verify Neo4j is Running

```bash
# Check Neo4j status
curl http://localhost:7474

# Access Neo4j Browser
open http://localhost:7474
```

#### 3. Start the Toolbox Server

```bash
# Navigate to your project directory
cd /home/ngobiro/projects/ewakili_agent

# Start toolbox server (choose one method)
./toolbox serve --port 5000 --config tools.yaml

# Verify toolbox is running
curl http://localhost:5000/health
```

#### 4. Run the Legal Research Agent

```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the agent
python agent.py
```

#### 5. Troubleshooting Startup Issues

**Neo4j Connection Issues:**
```bash
# Check Neo4j logs
docker logs neo4j-legal

# Test connection
neo4j-admin server console
```

**Toolbox Server Issues:**
```bash
# Check if port is available
netstat -tlnp | grep :5000

# Test tools configuration
./toolbox validate --config tools.yaml
```

**Agent Runtime Issues:**
```bash
# Check Python dependencies
pip check

# Verify Google Cloud credentials
gcloud auth application-default print-access-token
```

## Usage

### Basic Usage

```python
from agent import main

# Run the agent
main()
```

### Interactive Usage

You can also run the agent interactively:

```bash
# Start Python interactive session
python -i agent.py

# Then use individual functions
embedding = get_text_embedding("contract law")
query_params = create_embedding_query("employment disputes", "KE")
```

### Custom Queries

The agent supports various types of legal research queries:

```python
# Example queries
queries = [
    "Find cases related to contract law disputes in Kenya",
    "Search for employment law cases involving wrongful termination",
    "Look for property law cases about land disputes",
    "What are the legal requirements for contract formation?",
    "Find precedents on constitutional interpretation",
    "Cases dealing with breach of contract remedies"
]
```

### Available Tools

The system provides multiple specialized search tools:

1. **`get_similar_cases_by_legal_principle`**: Search based on legal doctrines and principles
2. **`get_similar_cases_by_case_summary`**: Search based on case facts and summaries
3. **`get_similar_cases_by_law_applied`**: Search based on specific statutes and laws
4. **`get_similar_cases_by_legal_precedents`**: Search for authoritative precedents
5. **`get_similar_cases_by_legal_issues_raised`**: Search based on legal issues
6. **`get_similar_cases_by_prayer`**: Search based on relief/remedies sought
7. **`get_cases_by_country`**: Jurisdiction-specific case retrieval
8. **`get_cases_by_case_type`**: Category-based case searches
9. **`get_cases_by_case_sub_type`**: Specialized sub-category searches

## Configuration

### Tools Configuration (`tools.yaml`)

The tools are configured with optimized Neo4j Cypher queries for performance:

```yaml
tools:
  get_similar_cases_by_legal_principle:
    kind: neo4j-cypher
    source: legal_db
    description: "Get similar cases based on legal principles."
    parameters:
      - name: query_embedding
        type: string
        description: "JSON string of the query embedding vector"
      - name: country_code
        type: string
        description: "Country code to filter cases by (e.g., KE, UG, TZ)"
    statement: |
      # Optimized Cypher query for legal principle searches
      CALL {
          MATCH (c:Case)-[:HAS_LEGAL_PRINCIPLES]->(lp:LegalPrinciple)
          WHERE lp.case_legal_principle_embeddings IS NOT NULL
          AND c.metadata_country = $country_code
          WITH c, lp, gds.similarity.cosine(lp.case_legal_principle_embeddings, 
               apoc.convert.fromJsonList($query_embedding)) AS similarity
          WHERE similarity > 0.7
          RETURN c, lp, similarity
      }
      # ... additional query logic
```

### Embedding Configuration

The system uses Google's text-embedding-004 model for semantic search:

```python
def get_text_embedding(text, model_name="text-embedding-004"):
    """
    Convert text to embeddings using Google's embedding model.
    """
    # Implementation with fallback for development
```

## Database Schema

The Neo4j database contains the following node types:

- **Case**: Legal cases with metadata
- **CaseSummary**: Case summaries with embeddings
- **LegalPrinciple**: Legal principles with embeddings
- **LegalIssue**: Legal issues raised in cases
- **LegalOutcome**: Case outcomes and decisions
- **Law**: Applied laws and statutes
- **Judge**: Judges involved in cases
- **LegalArgument**: Arguments presented in cases

### Relationships

- `Case -[:HAS_SUMMARY]-> CaseSummary`
- `Case -[:HAS_LEGAL_PRINCIPLES]-> LegalPrinciple`
- `Case -[:HAS_ISSUES]-> LegalIssue`
- `Case -[:HAS_OUTCOMES]-> LegalOutcome`
- `Case -[:HAS_LAWS_APPLIED]-> Law`
- `Case -[:HAS_JUDGES]-> Judge`
- `Case -[:HAS_ARGUMENTS]-> LegalArgument`

## API Reference

### Main Functions

#### `main()`
Initializes and runs the legal research agent with test queries.

#### `get_text_embedding(text, model_name="text-embedding-004")`
Converts text to embedding vectors for semantic search.

**Parameters:**
- `text` (str): Text to convert to embeddings
- `model_name` (str): Embedding model to use

**Returns:**
- `list`: 768-dimensional embedding vector

#### `create_embedding_query(query_text, country_code="KE")`
Creates properly formatted input for embedding-based searches.

**Parameters:**
- `query_text` (str): Search query
- `country_code` (str): Country code filter

**Returns:**
- `dict`: Formatted input parameters

## Development

### Project Structure

```
ewakili_agent/
├── agent.py                 # Main agent implementation
├── tools.yaml              # Tool configurations
├── requirements.txt        # Python dependencies
├── service_account_key.json # Google Cloud credentials
├── README.md               # This file
└── retrievers/             # Custom retriever implementations
    ├── __init__.py
    ├── case_summaries_retriever.py
    ├── legal_principles_retriever.py
    └── ...
```

### Adding New Tools

1. Define the tool in `tools.yaml`
2. Implement the Neo4j query with proper embeddings
3. Add appropriate parameters and descriptions
4. Test with the agent system

### Extending Search Capabilities

To add new search types:

1. Create new node types in Neo4j
2. Add embeddings for the new content
3. Define new tools in `tools.yaml`
4. Update the agent prompt to include new capabilities

## Performance Optimization

### Query Optimization

- Use indexed properties for filtering
- Implement proper similarity thresholds (0.7 for high-quality matches)
- Use UNION queries for multiple search paths
- Limit results appropriately (typically 30 cases)

### Embedding Optimization

- Cache embeddings for common queries
- Use batch processing for large datasets
- Implement proper error handling and fallbacks

## Security Considerations

- Store credentials securely (excluded from git)
- Use environment variables for sensitive configuration
- Implement proper authentication for database access
- Validate input parameters to prevent injection attacks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support or questions:
- Check the GitHub Issues page
- Review the documentation
- Contact the development team

## Changelog

### v1.0.0 (Current)
- Initial release with basic legal research capabilities
- Neo4j integration with embedding-based search
- Support for multiple East African jurisdictions
- Comprehensive tool suite for legal research

### Planned Features
- Enhanced prompt system for better legal analysis
- Support for additional jurisdictions
- Improved citation formats
- Advanced legal reasoning capabilities
- Integration with legal document management systems

---

*Last updated: July 14, 2025*
