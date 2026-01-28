# 🤝 ProConnect: RAG-Powered LinkedIn Agent

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Agentic_RAG-green?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange?style=for-the-badge&logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Gradio](https://img.shields.io/badge/Frontend-Gradio-lightgrey?style=for-the-badge&logo=gradio&logoColor=white)

**ProConnect** is an advanced AI-powered autonomous agent designed to streamline professional networking. Leveraging **Retrieval-Augmented Generation (RAG)**, it autonomously searches the web for a target's recent activity, prioritizes verifiable sources (like LinkedIn), and drafts highly personalized connection requests.

---

## 🚀 Key Features

- **🔎 Autonomous Web RAG**: Performs real-time semantic searches using SerpApi (Google) to fetch the latest data.
- **🧠 Intelligent Source Prioritization**: Automatically detects and prioritizes official LinkedIn profiles as the "source of truth," falling back to news articles if necessary.
- **📄 Structured Data Extraction**: Parses unstructured web content into structured fields (Current Role, Company, Recent News).
- **🛡️ Production-Ready Architecture**: Built with a modular service layer, centralized configuration, and comprehensive error handling.
- **🐳 Dockerized**: Fully containerized for easy deployment.

---

## �️ Tech Stack

- **Core**: Python 3.12+, `uv` (Package Management)
- **AI/LLM**: LangChain, OpenAI GPT-4o
- **Search**: SerpApi (Google Search Results)
- **Interface**: Gradio (Web UI) & Typer (CLI)
- **Infra**: Docker, Docker Compose
- **Quality**: Pytest, Pydantic Settings

---

## ⚡ Getting Started

### Prerequisites

- **Python 3.12+** (if running locally)
- **Docker** (optional, for containerized run)
- **API Keys**:
  - `OPENAI_API_KEY`
  - `SERPAPI_API_KEY`

### 1. clone the Repository

```bash
git clone https://github.com/mojarrad353/proconnect_agent_rag.git
cd proconnect_agent_rag
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-your-openai-key
SERPAPI_API_KEY=your-serpapi-key
```

### 3. Run with Docker (Recommended)

Simply use Docker Compose to build and start the service:

```bash
docker-compose up --build
```

Access the Web UI at **http://localhost:7860**.

---

## 💻 Local Development

If you prefer to run locally using `uv`:

1.  **Install Dependencies**:
    ```bash
    uv sync
    ```

2.  **Run the Web App**:
    ```bash
    uv run src/proconnect_agent_rag/app.py
    ```

3.  **Run the CLI**:
    ```bash
    uv run src/proconnect_agent_rag/main.py
    ```

4.  **Run Tests**:
    ```bash
    uv run pytest
    ```

---

## 📂 Project Structure

```text
src/proconnect_agent_rag/
├── app.py              # Gradio Web Interface
├── main.py             # CLI Entry Point
├── config.py           # Configuration (Pydantic)
├── services/           # Business Logic Layer
│   └── icebreaker.py   # RAG Engine
└── utils/              # Utilities (Logging, etc.)
```
