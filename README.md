# Medical AI Chatbot — RAG System

A state-of-the-art Medical AI Chatbot designed to answer medical queries based on a provided knowledge base (e.g., Gale Encyclopedia of Medicine) using the **Retrieval-Augmented Generation (RAG)** architecture. 

It uses a sleek, modern glassmorphism frontend and powerful backend models (Groq LLM and ChromaDB Cloud) to deliver rapid, accurate, and context-aware medical information.

---

## 🎯 Objective
The objective of this project is to provide a highly accurate, AI-powered medical assistant that retrieves contextual information from verified medical documents (PDFs) before generating answers. This significantly reduces hallucinations and ensures the chatbot only provides information rooted in the provided medical texts.

---

## ⚙️ Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (Premium Glassmorphism UI, marked.js for Markdown parsing)
- **Backend Framework**: Flask
- **LLM Engine**: Groq (`llama-3.1-8b-instant`)
- **Vector Database**: ChromaDB (Cloud)
- **RAG Orchestration**: LangChain

---

## 🚀 Step-by-Step Setup Guide

Follow these steps to configure, ingest your medical data, and run the chatbot locally.

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd MEDICAL_CHATBOT_USING_RAG
```

### 2. Set Up a Virtual Environment (Recommended)
It is highly recommended to use a virtual environment to manage dependencies.
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate
# Activate the virtual environment (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
Install all required Python libraries by running:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory of the project and add your API keys:
```env
# Groq API Key for the LLM
GROQ_API_KEY=your_groq_api_key_here

# Optional: Override default Groq model
GROQ_MODEL=llama-3.1-8b-instant

# Note: Add any ChromaDB Cloud API keys or endpoints if required by your src.helper implementation.
```

### 5. Add Your Knowledge Base (PDF Data)
Place your medical PDF documents (e.g., *Gale Encyclopedia of Medicine*) into the `data/` folder. The system will read these documents to build the chatbot's knowledge base.

### 6. Ingest Data to ChromaDB Cloud
Before starting the chatbot, you must convert the PDFs into text chunks, generate embeddings, and upload them to your Vector Database.
Run the indexing script:
```bash
python store_index.py
```
*You should see a console output detailing the ingestion progress and confirming the number of documents stored.*

### 7. Run the Application
Start the Flask web server:
```bash
python app.py
```
*You should see an output indicating the RAG components are loaded and the server is running on `http://0.0.0.0:5000`.*

---

## 💻 How to Operate the Project

1. **Access the Chatbot**: Open your web browser and go to `http://localhost:5000`.
2. **Ask Questions**: Use the input bar at the bottom to type medical questions (e.g., *"What are the symptoms of pneumonia?"* or *"Explain the causes of hypertension"*).
3. **View Formatted Answers**: The chatbot will search the ingested PDFs, send the relevant context to the LLM, and provide a structured, bulleted response directly in the chat window. 
4. **Suggestions**: Click on any of the suggested prompt chips on the welcome screen to quickly test the bot's capabilities.

---

## ⚠️ Disclaimer
**This is an AI assistant.** The information provided by this chatbot is generated for educational and informational purposes based on the provided documents. **Always consult a qualified healthcare professional for medical advice, diagnoses, or treatments.**