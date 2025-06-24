import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="Chat2Data", layout="wide")

st.title("💬 Chat2Data")
st.markdown("Ask questions to your dataset using natural language. Powered by Gemini + SQLite.")

if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False
if "history" not in st.session_state:
    st.session_state.history = []

prompt = ["""
You are an expert in converting English questions to SQL query!
The SQL database has a table called economicdata with the following columns:
[country_name], [year], [Inflation (CPI %)], [GDP (Current USD)], [GDP per Capita (Current USD)], 
[Unemployment Rate (%)], [Interest Rate (Real, %)], [Inflation (GDP Deflator, %)], [GDP Growth (% Annual)], 
[Current Account Balance (% GDP)], [Government Expense (% of GDP)], [Government Revenue (% of GDP)], 
[Tax Revenue (% of GDP)], [Gross National Income (USD)], [Public Debt (% of GDP)]

When writing the SQL query, ensure:
- Column names with spaces are enclosed in square brackets [ ]
- The SQL code should not have ``` in beginning or end
- Do not include the word 'sql' in the output
"""]


@st.dialog("Enter Your Gemini API Key")
def api_key_dialog():
    api_input = st.text_input("Gemini API Key", type="password")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("Submit"):
            if api_input.startswith("AIza"):
                st.session_state.api_key = api_input
                st.session_state.show_dialog = False
                st.rerun()
            else:
                st.error("Invalid API Key. It must start with 'AIza'")
    with col2:
        if st.button("Cancel"):
            st.session_state.show_dialog = False

if not st.session_state.api_key:
    st.warning("Please click the button below to enter your Gemini API key.")
    if st.button("🔐 Enter Gemini API Key"):
        st.session_state.show_dialog = True

if st.session_state.show_dialog:
    api_key_dialog()

if st.session_state.api_key:
    genai.configure(api_key=st.session_state.api_key)

    @st.cache_resource
    def load_model():
        return genai.GenerativeModel('models/gemini-2.5-flash-lite-preview-06-17')

    model = load_model()

    def get_gemini_response(question, prompt):
        try:
            response = model.generate_content([prompt[0], question])
            return response.text.strip()
        except Exception as e:
            st.error(f"Gemini Error: {str(e)}")
            return None

    def read_sql_query(sql, db):
        try:
            conn = sqlite3.connect(db)
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return df, None
        except Exception as e:
            return None, str(e)

    question = st.text_input("🧠 Ask your question:")

    if st.button("Run Query") and question:
        with st.spinner("Generating SQL query with Gemini..."):
            sql_query = get_gemini_response(question, prompt)

            if sql_query:
                st.code(sql_query, language='sql')
                df, error = read_sql_query(sql_query, "globaleconomicdata.db")

                if error:
                    st.error(f"SQL Error: {error}")
                elif df.empty:
                    st.warning("Query ran successfully but returned no results.")
                else:
                    st.success("Query executed successfully!")
                    st.dataframe(df, use_container_width=True)
                    st.session_state.history.append({
                        "question": question,
                        "sql": sql_query,
                        "result": df.copy()
                    })

    with st.sidebar:
        st.subheader("📜 Query History")
        if not st.session_state.history:
            st.info("No successful queries yet.")
        else:
            for i, entry in enumerate(st.session_state.history[::-1]):
                label = f"{len(st.session_state.history)-i}. {entry['question'][:40]}..."
                if st.button(label, key=f"history_{i}"):
                    st.subheader("🧠 Previous Question")
                    st.text(entry["question"])
                    st.subheader("📝 SQL Query")
                    st.code(entry["sql"], language='sql')
                    st.subheader("📊 Result")
                    st.dataframe(entry["result"], use_container_width=True)