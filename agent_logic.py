import os
from pypdf import PdfReader
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import json

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_claims(text):
    # LLM ko function ke andar initialize kiya taaki key pehle se na maange
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    prompt = f"""
    You are an assistant checking a document. Look at this text and find all specific claims that have stats, dates, or numbers.
    Ignore generic sentences. 
    
    Return the output ONLY as a JSON list of objects, where each object has:
    "claim": "the fact or stat found"
    "context": "the sentence around it"
    
    Text:
    {text}
    """
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)

def verify_claim(claim_text, context):
    # Dono tools ko function ke andar dala, jab run hoga tabhi key use hogi
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    search_tool = TavilySearchResults(max_results=3)
    
    try:
        search_results = search_tool.invoke({"query": claim_text})
    except Exception as e:
        search_results = f"Search failed: {str(e)}"
    
    prompt = f"""
    Compare this claim with the live web search results from the current year 2026.
    
    Claim: {claim_text}
    Context: {context}
    
    Search Results:
    {search_results}
    
    Give a final verdict in this exact JSON format:
    {{
        "status": "Verified" or "Inaccurate" or "False",
        "real_facts": "A short summary of what is actually true based on search results."
    }}
    """
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return json.loads(content)