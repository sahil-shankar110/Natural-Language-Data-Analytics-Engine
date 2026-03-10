# 📊 Natural Language Data Analytics Engine

> Explore and analyze datasets using simple natural language queries.

---

## 📌 Overview

**Natural Language Data Analytics Engine** is an intelligent, GenAI-powered data analytics application that allows anyone to explore and analyze datasets using plain English — no SQL, no coding, no technical background required.

Users simply upload a dataset (CSV, Excel, JSON, or SQLite), ask a question in plain English, and the system automatically:
- Converts the question into an accurate SQL query using LLaMA4 Scout via Groq
- Executes the query securely on a read-only SQLite database
- Returns results with interactive visualizations and plain English explanations

This project demonstrates how large language models can be seamlessly integrated with data analytics pipelines to build powerful, accessible, and intelligent data exploration tools.

---
## ✨ Key Features

| Feature | Description |
|---|---|
| 🗣️ **Natural Language Queries** | Ask questions in plain English — no SQL knowledge needed |
| 📁 **Multi-Format Support** | Upload CSV, Excel, JSON, SQLite, or .db files |
| 🤖 **AI-Powered Engine** | (meta-llama/llama-4-scout-17b-16e-instruct) via Groq API for fast, accurate SQL generation |
| 📊 **Auto Visualization** | Intelligent chart selection — bar, line, pie, scatter |
| 💬 **Plain English Explanations** | Every result explained in simple, human-readable language |
| 🔒 **Secure & Read-Only** | Files are never modified — auto-deleted after session ends |
| 🕐 **Session Query History** | Last 10 queries saved and accessible throughout the session |
| 💡 **Smart Suggestions** | Context-aware question suggestions based on your data |
| 🎯 **Demo Datasets** | Practice with built-in datasets — no upload required |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Programming Language** | Python 3.11+ |
| **UI Framework** | Streamlit |
| **LLM Provider** | Groq API — `meta-llama/llama-4-scout-17b-16e-instruct` |
| **LLM Orchestration** | LangChain |
| **Data Engine** | SQLite3 (read-only, session-isolated) |
| **Data Processing** | Pandas, SQLite ,  tempfile, os (for file loading) |
| **Visualization** | Plotly |
| **Package Manager** | uv |

---
## ⚙️ How It Works

```
① Upload File          CSV / Excel / JSON / SQLite
         │
         ▼
② Convert to SQLite    Read-only, in-memory database
         │
         ▼
③ Ask a Question       "Show top 5 students by marks"
         │
         ▼
④ LangChain + Groq     Schema-aware prompt → SQL + chart type
         │
         ▼
⑤ Execute Query        Safe SELECT-only execution
         │
         ▼
⑥ Display Results      📊 Chart → 📋 Table → 💬 Explanation → 🔍 SQL
```

---

## 📂 Project Structure

```
natural-language-data-analytics-engine/
│
├── streamlit_app.py        # Entry point — UI & orchestration
├── pyproject.toml          # uv dependency management
├── .env.example            # Environment variable template
├── README.md
│
├── app/
│   ├── prompts.py          # LangChain prompt templates (the brain)
│   ├── llm.py              # Groq LLM chain — NL → SQL + explanation
│   ├── database.py         # SQLite3 read-only query execution
│   ├── file_loader.py      # Multi-format file → SQLite conversion
│   └── visualizer.py       # Auto Plotly chart generation
│
├── Demo_Files/
│   ├── Student_Data.csv    # Student performance dataset
│   └── Sales_Data.csv      # Sales analytics dataset
```

---

## 🔒 Security Model

The application follows a strict **zero-modification** security model:

- **Read-Only Database** — SQLite opened with `?mode=ro` URI flag
- **SELECT-Only Enforcement** — All queries validated before execution. `INSERT`, `UPDATE`, `DELETE`, `DROP` are blocked at two layers: prompt level and code level
- **Session Isolation** — Each user session gets an independent temp database
- **Auto Cleanup** — Temp files deleted automatically when session ends
- **No Persistent Storage** — Zero user data retained between sessions
- **Secure Secrets** — API keys loaded from `.env`, never hardcoded

---

### Run The Project

```
bash
# 1. Clone the repository
git clone https://github.com/yourusername/nl-data-analytics-engine.git
cd nl-data-analytics-engine

# 2. Install dependencies
uv sync

# 3. Launch the application
uv run streamlit run streamlit_app.py
```

---

## 👤 Author

**Sahil Shankar**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sahil-shankar110)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sahil-shankar-974135334)

---

<div align="center">

⭐ Star this repo if you found it helpful!

</div>

