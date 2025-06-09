# LegalEdge AI

LegalEdge AI is a comprehensive legal document analysis and generation suite that leverages AI to assist with various legal tasks.

## Features

- **Legal Assistant**: Get answers to legal questions and guidance on legal matters
- **Document Generator**: Generate legal documents based on your requirements
- **Contract Analyzer**: Analyze contracts and identify key clauses, risks, and obligations
- **Compliance Checker**: Check legal documents for compliance with regulations
- **Document Simplifier**: Convert complex legal language into simpler terms

## Prerequisites

- Python 3.8 or higher
- Ollama (for running the LLM locally)
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/legal-edge-ai.git
cd legal-edge-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and start Ollama:
- Download and install Ollama from [ollama.ai](https://ollama.ai)
- Start the Ollama server:
```bash
ollama serve
```

5. Pull the required model:
```bash
ollama pull llama2
```

## Running the Application

1. Start the Ollama server (if not already running):
```bash
ollama serve
```

2. In a new terminal, start the FastAPI application:
```bash
uvicorn main:app --reload
```

3. Open your browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
legal-edge-ai/
├── main.py              # FastAPI application entry point
├── ollama_client.py     # Ollama API client
├── requirements.txt     # Python dependencies
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── legal-assistant.html
│   ├── document-generator.html
│   ├── contract-analyzer.html
│   ├── compliance-checker.html
│   └── document-simplifier.html
└── README.md
```

## Usage

### Legal Assistant
- Ask legal questions and get AI-powered responses
- Get guidance on legal matters and procedures

### Document Generator
- Generate legal documents based on your requirements
- Customize document templates with your specific needs

### Contract Analyzer
- Upload or paste contract text for analysis
- Get insights on key clauses, risks, and obligations
- Support for PDF uploads

### Compliance Checker
- Check legal documents for regulatory compliance
- Upload PDFs or paste text for analysis
- Get detailed compliance reports and recommendations

### Document Simplifier
- Convert complex legal language into simpler terms
- Make legal documents more accessible and understandable

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI and Ollama
- Uses the Llama2 model for AI-powered analysis
- Inspired by the need for accessible legal technology 