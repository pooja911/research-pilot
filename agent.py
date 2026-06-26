from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from tools import search_web
import os

load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

def calculate_confidence(results: list) -> float:
    """
    Calculates confidence score based on source relevance scores.
    Returns a score between 0 and 1.
    """
    if not results:
        return 0.0
    
    scores = [r.get("score", 0) for r in results]
    avg_score = sum(scores) / len(scores)
    return round(avg_score, 2)

def research(question: str) -> dict:
    """
    Main research function:
    1. Searches the web
    2. Synthesizes results with LLM
    3. Returns answer + citations + confidence
    """
    print(f"🔍 Searching for: {question}")
    
    # Step 1 — Search the web
    search_results = search_web(question)
    sources = search_results.get("results", [])
    quick_answer = search_results.get("answer", "")

    # Step 2 — Build context from sources
    context = ""
    for i, source in enumerate(sources):
        context += f"\nSource {i+1}: {source['title']}\n"
        context += f"URL: {source['url']}\n"
        context += f"Content: {source['content']}\n"
        context += "---\n"

    # Step 3 — Ask LLM to synthesize
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research assistant. 
        Synthesize the provided sources into a clear, accurate answer.
        Always cite your sources by referring to them as [Source 1], [Source 2] etc.
        Be factual and only use information from the provided sources."""),
        ("user", """Question: {question}
        
Quick Answer from search: {quick_answer}

Sources:
{context}

Please provide:
1. A comprehensive answer with citations
2. Key findings as bullet points
3. Any limitations or gaps in the available information""")
    ])

    # Step 4 — Get synthesized answer from LLM
    chain = prompt | llm
    response = chain.invoke({
        "question": question,
        "quick_answer": quick_answer,
        "context": context
    })

    # Step 5 — Calculate confidence
    confidence = calculate_confidence(sources)

    return {
        "question": question,
        "answer": response.content,
        "sources": sources,
        "confidence": confidence
    }