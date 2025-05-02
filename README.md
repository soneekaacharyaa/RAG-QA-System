
# Movie Trivia Q&A System

## Description
The **Movie Trivia Q&A System** is a RAG (Retrieval-Augmented Generation) question-answering platform designed to answer movie-related queries. It combines **semantic search** using **Sentence Transformers**, **fast vector retrieval** with **FAISS**, and **gpt-4o** from OpenAI for generating contextually relevant answers.

The system uses a pre-loaded movie trivia database to answer questions about movies, including details like actors, directors, release years, and plot summaries. If the database doesn't have an answer, it can fetch additional information via web search using **SerpAPI**.

Built with **Streamlit**, the application provides a user-friendly interface for asking movie trivia questions and receiving answers in real time.

---

### Required Environment Variables:
Make sure to set the following environment variables in a `.env` file:
- `OPENAI_API_KEY`: Your OpenAI API key for gpt-4o.
- `SERPAPI_KEY`: Your API key for SerpAPI to perform web searches.

## Installation and Setup

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/soneekaacharyaa/RAG-QA-System.git
   cd RAG-QA-System
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv rag_env
   rag_env\Scripts\activate  #On Linux use source rag_env/bin/activate
   ```

3. Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Add your API keys in the `.env` file:

   ```
   OPENAI_API_KEY=your-openai-api-key
   SERPAPI_KEY=your-serpapi-api-key
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

## Architecture & Design
```

User Question
   │
   ▼
[Streamlit Frontend]
   │
   ▼
[SentenceTransformer Encoder]
   │
   ▼
[FAISS Vector Search]
   │
   ▼
[Context Construction from Movie Dataset or Web Search]
   │
   ▼
[OpenAI gpt-4o]
   │
   ▼
Generated Answer
```

Components
- Embedding Model: all-MiniLM-L6-v2 from sentence-transformers
- Vector Store: FAISS index built from movie plots, actors, directors, etc.
- LLM: OpenAI gpt-4o for generating answers using retrieved context
- Fallback: If local data fails, falls back to SerpAPI web search
- UI: Built with Streamlit for interactive QA


## Project Strcuture
```
├── data
│   └── movie_trivia.json       # JSON file containing movie data
├── src
│   ├── generate_answers.py     # Core logic: loading, retrieval, and QA generation
│   ├── app.py                  # Streamlit frontend
│   └── evaluate.py             # Evaluation script for test queries
├── .env example                # Contains example to setup .env file 
├── requirements.txt            # Python dependencies
├── .gitignore                  # Files to ignore in Git
└── README.md                   # Project documentation
```

## Evaluation

The evaluation script tests the system's performance with a predefined set of questions. The accuracy is measured based on whether the system provides the correct answer or appropriately responds with "I don't know."

### Running the Evaluation:

To run the evaluation, execute the following:

```bash
python evaluate.py
```

## To-Do
- Improve fallback to summarize or refine web results
- Caching repeated queries
- Add interface to view source chunk(s) behind each answer
- Filter non-movie-based queries
