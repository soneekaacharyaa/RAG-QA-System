import json
from sentence_transformers import SentenceTransformer
import faiss
from openai import OpenAI
import os
from dotenv import load_dotenv
from serpapi.google_search import GoogleSearch

load_dotenv()

def load_system():
    """Initialize and return all system components"""
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    with open("..\data\movie_trivia.json", 'r') as f:
        movies = json.load(f)
    
    processed_data = preprocess_data(movies)
    index = create_vector_db(processed_data, embedding_model)
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    return index, processed_data, embedding_model, openai_client

def preprocess_data(movies):
    processed_chunks = []
    for movie in movies:
        movie_text = f"Title: {movie['title']}. Year: {movie['year']}. Plot: {movie['plot']}. Actors: {movie['actors']}. Director: {movie['director']}."
        processed_chunks.append(movie_text)   
    return processed_chunks

def create_vector_db(processed_data, embedding_model):
    embeddings = embedding_model.encode(processed_data)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def retrieve(query, index, chunks, embedding_model, top_k=3):
    query_embedding = embedding_model.encode([query])
    scores, indices = index.search(query_embedding, top_k)
    retrieved_chunks = []
    for idx in indices[0]:
        if idx != -1: 
            retrieved_chunks.append(chunks[idx])
    return retrieved_chunks


def generate_from_context(question, context, openai_client):
    prompt = f"""Answer the question using ONLY the context below. 
    If unsure, say "I don't know".

    Context:
    {context}

    Question: {question}"""

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def search_web(query):
    try:
        params = {
            "q": query,
            "hl": "en",
            "gl": "us",
            "api_key": os.getenv("SERPAPI_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        description = results.get("knowledge_graph", {}).get("description", "")
        snippets = [result.get("snippet", "") for result in results.get("organic_results", []) if result.get("snippet")]
        combined_context = description + " " + " ".join(snippets[:3]) 

        return combined_context.strip()
    except:
        return None

def generate_answer(question, index, processed_data, embedding_model, openai_client):
    retrieved_chunks = retrieve(question, index, processed_data, embedding_model)  
    context = "\n---\n".join(retrieved_chunks)
    
    if not retrieved_chunks:
        message = "I couldn’t find information about this."
        return None,  "no-context", message
    
    answer = generate_from_context(question, context, openai_client)
    
    if "i don't know" in answer.lower():
        web_results = search_web(question)
        message = "Retrieved from Web Search"
        if web_results:
            answer = generate_from_context(question, web_results, openai_client)
            if "i don't know" not in answer.lower():
                return answer, "web_search", message
            else: 
                message = "I couldn't find a definitive answer. Please try rephrasing or asking a different question."
                return None, "no_context", message
        else:
            message = "I couldn't find a definitive answer. Please try rephrasing or asking a different question."
            return None, "no_context", message
    else:
        message = "Retreived from Local Database"
        return answer, "local_search", message