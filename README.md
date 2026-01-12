# 🍃 Greenwash Hunter

### **Trust, but Verify.**
**Greenwash Hunter** is an autonomous AI agent designed to audit Corporate Sustainability Reports. It ingests complex PDF documents, extracts specific ESG (Environmental, Social, and Governance) promises, and cross-references them with real-world news and legal records to detect inconsistencies.

Built for analysts who need to cut through corporate marketing jargon and find the truth.

---

## 🚀 Key Features

* **📄 Intelligent PDF Ingestion:** Parses "High-Value" sections of annual reports, filtering out marketing fluff to find concrete claims.
* **🧠 Cognitive Extraction:** Uses **Google Gemini Pro** to identify and structure specific sustainability goals (e.g., "Net Zero by 2040").
* **🕵️‍♂️ Automated Investigation:** Spawns a **LangChain** agent to scour the web (DuckDuckGo) for scandals, lawsuits, and pollution violations related to those specific claims.
* **⚖️ The Verdict Engine:** Synthesizes internal promises vs. external reality to generate a "PASS/FAIL" risk assessment.

---

## 🛠️ Tech Stack

* **Core:** Python 3.10+
* **Frontend:** Streamlit (UI/UX)
* **LLM Engine:** Google Gemini Pro (via `google-generativeai`)
* **Orchestration:** LangChain Community Tools
* **Search Layer:** DuckDuckGo Search API
* **Processing:** PyPDF2

---

## ⚙️ Installation & Usage

### **1. Clone the Repository**
```bash
git clone [https://github.com/YourUsername/greenwash-hunter.git](https://github.com/YourUsername/greenwash-hunter.git)
cd greenwash-hunter