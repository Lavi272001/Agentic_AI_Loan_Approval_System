# Streamlit Chatbot UI
# User interface for the loan approval system

import streamlit as st
import requests

st.set_page_config(page_title="Agentic Loan Assistant", layout="wide")
st.title("🏦 Agentic AI Intelligent Loan Approval System")

# Form Inputs
with st.sidebar:
    st.header("📋 Applicant Form Details")
    app_id = st.text_input("Applicant ID", value="APP-9982")
    age = st.number_input("Age", min_value=18, max_value=100, value=34)
    income = st.number_input("Annual Income ($)", value=95000)
    emp_type = st.selectbox("Employment Type", ["Full-Time", "Part-Time", "Self-Employed", "Unemployed"])
    credit_score = st.slider("Credit Score", 300, 850, 720)
    loan_amt = st.number_input("Requested Loan Amount ($)", value=25000)
    tenure = st.number_input("Tenure (Months)", value=36)
    liabilities = st.number_input("Existing Monthly Liabilities ($)", value=1200)
    location = st.text_input("Location", value="New York, USA")

if st.button("🚀 Evaluate Loan Application"):
    payload = {
        "applicant_id": app_id,
        "age": age,
        "income": income,
        "employment_type": emp_type,
        "credit_score": credit_score,
        "loan_amount": loan_amt,
        "tenure": tenure,
        "existing_liabilities": liabilities,
        "location": location
    }
    
    with st.spinner("Multi-Agent Coordination Engine actively analyzing..."):
        try:
            response = requests.post("http://localhost:8000/api/v1/loan/evaluate", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                # Main Status Display
                decision = data['final_decision']['classification']
                if decision == "Approved":
                    st.success(f"🎉 Result: {decision}")
                elif decision == "Requires Manual Review":
                    st.warning(f"⚠️ Result: {decision}")
                else:
                    st.error(f"❌ Result: {decision}")
                
                # Agent Audit Trail Breakdowns
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🕵️‍♂️ Applicant Profile Agent Metrics")
                    st.json(data['applicant_profile_data'])
                    
                    st.subheader("📊 Financial Risk Agent Metrics")
                    st.json(data['financial_risk_data'])
                    
                with col2:
                    st.subheader("🧠 Decision Agent Synthesis")
                    st.json(data['final_decision'])
                    
                    st.subheader("🛡️ Compliance & Actions Audit")
                    st.json(data['compliance_action'])
            else:
                st.error("Error communicating with backend microservice.")
        except Exception as e:
            st.error(f"Failed to fetch evaluation: {e}")

