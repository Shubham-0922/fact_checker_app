import streamlit as st
import os
from agent_logic import extract_text_from_pdf, extract_claims, verify_claim

st.set_page_config(page_title="Fact Checker App", page_icon="🔍")

st.title("🔍 Automated Fact-Checking Web App")
st.write("Upload a PDF to extract key claims and verify them against live web data.")

# Sidebar for API Keys
st.sidebar.header("Setup API Keys")
openai_key = st.sidebar.text_input("Enter OpenAI Key", type="password")
tavily_key = st.sidebar.text_input("Enter Tavily Key", type="password")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    if not openai_key or not tavily_key:
        st.error("Please enter both API keys in the sidebar first!")
    else:
        # Set environment variables dynamically
        os.environ["OPENAI_API_KEY"] = openai_key
        os.environ["TAVILY_API_KEY"] = tavily_key
        
        st.success("File uploaded! Starting the verification process...")
        
        # Step 1: Extract Claims
        with st.spinner("Extracting claims from PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            claims = extract_claims(pdf_text)
            st.write(f"Found {len(claims)} factual claims to check.")
            
        # Step 2: Process and Verify each claim
        if claims:
            results = []
            progress = st.progress(0)
            
            for index, item in enumerate(claims):
                with st.spinner(f"Checking claim {index+1}/{len(claims)}..."):
                    verdict = verify_claim(item['claim'], item['context'])
                    results.append({
                        "claim": item['claim'],
                        "status": verdict.get('status', 'False'),
                        "real_facts": verdict.get('real_facts', 'No details available')
                    })
                # Update progress bar
                progress.progress((index + 1) / len(claims))
                
            # Step 3: Show results
            st.markdown("### 📊 Verification Report")
            
            for res in results:
                # Simple color logic based on status
                if res['status'] == 'Verified':
                    status_text = f"🟢 Verified"
                elif res['status'] == 'Inaccurate':
                    status_text = f"🟡 Inaccurate"
                else:
                    status_text = f"🔴 False"
                    
                # Display in a clean expander box
                with st.expander(f"{status_text} | {res['claim'][:80]}..."):
                    st.write(f"**Original Claim:** {res['claim']}")
                    st.write(f"**Verdict:** {res['status']}")
                    st.write(f"**Live Web Source Info:** {res['real_facts']}")