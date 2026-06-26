from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from tools import search_web
import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

def calculate_confidence(results: list) -> float:
    if not results:
        return 0.0
    scores = [r.get("score", 0) for r in results]
    avg_score = sum(scores) / len(scores)
    return round(avg_score, 2)

def research(question: str, num_sources: int = 5) -> dict:
    print(f"🔍 Searching for: {question}")

    # Step 1 — Search the web
    search_results = search_web(question, num_sources)
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

    # Step 4 — Get synthesized answer
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