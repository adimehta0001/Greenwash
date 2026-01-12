import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
import time
st.set_page_config(page_title="Greenwash Hunter", page_icon="🍃", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #00ffa3; color: black; border-radius: 5px; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)
st.sidebar.title("🍃 Greenwash Hunter")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
uploaded_file = st.sidebar.file_uploader("Upload Report (PDF)", type="pdf")
model_name = "models/gemini-pro" 
if api_key:
    try:
        genai.configure(api_key=api_key)

        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)

        if available_models:
            model_name = st.sidebar.selectbox("Select Brain", available_models, index=0)
            st.sidebar.success(f"Locked on: {model_name}")
        else:
            st.sidebar.error("No models found. Check API permissions.")
            
    except Exception as e:
        st.sidebar.error(f"API Error: {e}")

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    max_pages = min(len(reader.pages), 4) 
    for i in range(max_pages):
        text += reader.pages[i].extract_text()
    return text

def search_web(query):
    search = DuckDuckGoSearchRun()
    try:
        time.sleep(1)
        return search.run(f"{query} scandal lawsuit fine")
    except:
        return "No public dirt found."

if uploaded_file and api_key:

    model = genai.GenerativeModel(model_name)

    if st.button("RUN AUDIT"):

        with st.spinner("📂 Reading Document..."):
            raw_text = extract_text(uploaded_file)
 
        with st.status("🔍 Extracting Claims...", expanded=True):
            prompt_extract = f"""
            Extract the Company Name and 3 sustainability claims.
            Format:
            Company: [Name]
            Claim 1: [Text]
            Claim 2: [Text]
            Claim 3: [Text]
            
            TEXT: {raw_text[:3000]}
            """
            
            try:
                res = model.generate_content(prompt_extract).text
                
                company = "Target"
                claims = []
                for line in res.split('\n'):
                    if "Company:" in line: company = line.split(":")[1].strip()
                    if "Claim" in line: claims.append(line.split(":")[1].strip())
                
                if not claims: claims = ["Net Zero", "Ethical Sourcing", "Waste Reduction"]
                
                st.write(f"**Target:** {company}")
                st.write(f"**Claims:** {claims}")
                
            except Exception as e:
                st.error(f"Extraction Error: {e}")
                st.stop()

        evidence = {}
        with st.status("🕵️‍♂️ Investigating...", expanded=True):
            progress = st.progress(0)
            for i, claim in enumerate(claims):
                st.write(f"Checking: {claim}")
                evidence[claim] = search_web(f"{company} {claim}")
                progress.progress((i+1)/len(claims))

        st.divider()
        st.subheader("⚖️ Final Verdict")
        with st.spinner("Compiling Report..."):
            prompt_verdict = f"""
            Compare Claims vs Evidence.
            Company: {company}
            Claims: {claims}
            Evidence: {evidence}
            
            OUTPUT:
            1. Table comparing Promise vs Reality.
            2. Verdict: GREENWASHING or PASSED.
            """
            try:
                final_report = model.generate_content(prompt_verdict).text
                st.markdown(final_report)
            except Exception as e:
                st.error(f"Verdict Error: {e}")