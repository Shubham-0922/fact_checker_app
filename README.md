# Automated Fact-Checking Web App

This repository contains a modular AI Agent designed to parse PDF documents, automatically extract precise factual claims (such as statistics, dates, or numerical metrics), and cross-verify them against live internet data using real-time web search. 

The project is structured to ensure clean code readability, modularity, and straightforward execution.

## Live Deployment
The application is fully deployed and accessible here:
[INSERT YOUR STREAMLIT LIVE LINK HERE]

## How It Works
1. **Text Extraction:** The application reads raw text from uploaded PDF files using PyPDF.
2. **Claims Identification:** Using LangChain orchestration, the text is processed by the LLM to filter out generic sentences and isolate testable factual claims.
3. **Live Verification:** Each extracted claim is processed individually and verified against real-time web results via the Tavily Search API.
4. **Final Reporting:** The final verdict is structured into a clean Streamlit interface, classifying claims as Verified, Inaccurate, or False along with the live web source details.

## Project Structure
The repository consists of three core files:
- `app.py`: The frontend UI and user input handling built with Streamlit.
- `agent_logic.py`: The backend logic handling text parsing, prompt execution, and search tool calls.
- `requirements.txt`: The underlying dependencies required to provision the environment.

## Local Setup & Installation

To run this application locally, please follow these steps:

Install the necessary dependencies:
python -m pip install -r requirements.txt

Run the Streamlit server:
python -m streamlit run app.py

Security & API Compliance
In accordance with security best practices, no API keys are hardcoded into this repository. Users are required to input their own OpenAI and Tavily API credentials securely via the Streamlit sidebar at runtime. These keys exist only within the temporary browser session and are never stored.

