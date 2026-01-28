# 🤝 Proconnect: RAG-Powered LinkedIn Agent

![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-Agentic_RAG-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)
![SerpApi](https://img.shields.io/badge/API-SerpApi-red)
![Gradio](https://img.shields.io/badge/Frontend-Gradio-lightgrey)

---

## 📌 Project Overview

**ProConnect** is an AI-powered **Autonomous Agent** that automates the research required for professional networking. It uses a **Retrieval-Augmented Generation (RAG)** approach to search the live web for a person's recent activity and drafts a personalized LinkedIn connection request in seconds.

The project demonstrates:
- **Agentic Search:** Autonomously querying Google via **SerpApi** to find real-time information.
- **Smart Prioritization:** Automatically detecting and prioritizing **LinkedIn profiles** as the "source of truth."
- **Structured Extraction:** Using **LangChain** to parse unstructured web data into structured fields (Current Role, Company).
- **Modern UI:** A clean, responsive interface built with **Gradio**.

---

## 🚀 Features

- 🔍 **Real-Time Web RAG:** Scrapes the latest results from Google (not a static database).
- 🎯 **LinkedIn-First Logic:** Prioritizes official LinkedIn bios; falls back to news/articles if no profile is found.
- 🤖 **Role Extraction:** Intelligently identifies and isolates the user's current **Job Title** and **Company** for context.
- 🛡️ **Hallucination Guardrails:** Strict prompting ensures the AI only uses retrieved facts.

---

## 🧑‍💻 Skills & Technologies

- **Programming Language:** Python 3.12+
- **Package Manager:** uv (Modern, fast Python package installer)
- **LLM Framework:** LangChain (Chains, Prompts, Output Parsers)
- **Model Provider:** OpenAI (GPT-4o)
- **Search Engine:** SerpApi (Google Search Engine Results API)
- **Frontend:** Gradio (Web UI)

---

## ▶️ How to Run the Project

## 1. Prerequisites
Ensure you have `uv` installed (or use pip/poetry):
pip install uv

## 2. Prerequisites
git clone https://github.com/mojarrad353/proconnect_agent_rag.git

cd proconnect_agent_rag

## 3.Configure Environment
Create a .env file in the root directory and add your API keys

## 4. Install Dependencies
uv sync

## 5. Run the agent
For showing on the web using Gradio: 
uv run src/app.py

For showing in the terminal: 
uv run src/main.py

