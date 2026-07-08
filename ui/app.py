# Streamlit Loan Approval UI - Enhanced with Beautiful Styling
# Advanced user interface for the Agentic AI Loan Approval System

import streamlit as st
import requests
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="🏦 Agentic Loan Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com',
        'Report a bug': None,
        'About': "# Agentic AI Loan Approval System\nPowered by Multi-Agent AI"
    }
)

# Custom CSS Styling for Enhanced Colors and Design
st.markdown("""
<style>
/* Main theme colors */
:root {
    --primary-blue: #0066CC;
    --success-green: #00AA44;
    --warning-orange: #FF8800;
    --danger-red: #DD3333;
    --light-bg: #F0F4F8;
}

/* Streamlit main container background */
.main {
    background: linear-gradient(135deg, #f0f4f8 0%, #e8eef7 100%);
}

/* Header styling */
.stTitle {
    color: #0066CC !important;
    text-shadow: 0 2px 4px rgba(0,102,204,0.1);
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* Metric cards styling */
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    border-left: 4px solid #0066CC;
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,102,204,0.1);
    transition: all 0.3s ease;
}

.metric-card:hover {
    box-shadow: 0 4px 12px rgba(0,102,204,0.2);
    transform: translateY(-2px);
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 12px 30px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0,102,204,0.3);
}

.stButton > button:hover {
    box-shadow: 0 6px 16px rgba(0,102,204,0.4);
    transform: translateY(-2px);
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
}

/* Success message styling */
.stSuccess {
    background-color: #E8F5E9 !important;
    border-left: 4px solid #00AA44 !important;
    border-radius: 8px;
}

/* Warning message styling */
.stWarning {
    background-color: #FFF3E0 !important;
    border-left: 4px solid #FF8800 !important;
    border-radius: 8px;
}

/* Error message styling */
.stError {
    background-color: #FFEBEE !important;
    border-left: 4px solid #DD3333 !important;
    border-radius: 8px;
}

/* Expander styling */
.streamlit-expanderHeader {
    background-color: #F0F4F8 !important;
    border-radius: 8px;
    border-left: 4px solid #0066CC;
}

/* Card styling for metrics */
.card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-top: 3px solid #0066CC;
}

/* JSON display styling */
.json-container {
    background-color: #F5F5F5;
    border-radius: 8px;
    padding: 15px;
    border-left: 4px solid #0066CC;
}

/* Subheader styling */
.stSubheader {
    color: #0066CC !important;
    font-weight: 600;
    border-bottom: 2px solid #E0E8F0;
    padding-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header Section
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.markdown("## 🏦")
with col_title:
    st.markdown("# Agentic AI Intelligent Loan Approval System")
    st.markdown("*Powered by Multi-Agent AI Architecture with Real-Time Decision Analysis*")

st.markdown("---")

# Key Information Boxes at Top
info_col1, info_col2, info_col3, info_col4 = st.columns(4)

with info_col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                padding: 20px; border-radius: 12px; border-left: 4px solid #0066CC; text-align: center;">
        <h3 style="color: #0066CC; margin: 0;">⚡ Fast</h3>
        <p style="color: #666; margin: 5px 0 0 0; font-size: 14px;">Real-time Analysis</p>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                padding: 20px; border-radius: 12px; border-left: 4px solid #00AA44; text-align: center;">
        <h3 style="color: #00AA44; margin: 0;">✅ Accurate</h3>
        <p style="color: #666; margin: 5px 0 0 0; font-size: 14px;">AI-Powered Decisions</p>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
                padding: 20px; border-radius: 12px; border-left: 4px solid #FF8800; text-align: center;">
        <h3 style="color: #FF8800; margin: 0;">📊 Detailed</h3>
        <p style="color: #666; margin: 5px 0 0 0; font-size: 14px;">Comprehensive Analysis</p>
    </div>
    """, unsafe_allow_html=True)

with info_col4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
                padding: 20px; border-radius: 12px; border-left: 4px solid #9C27B0; text-align: center;">
        <h3 style="color: #9C27B0; margin: 0;">🔒 Secure</h3>
        <p style="color: #666; margin: 5px 0 0 0; font-size: 14px;">Compliant & Safe</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar Form with Enhanced Styling
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #0066CC;">📋 Applicant Information</h2>
        <p style="color: #666; font-size: 14px;">Enter applicant details for analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Personal Information Section
    st.markdown("### 👤 Personal Information")
    app_id = st.text_input("Applicant ID", value="APP-9982",
                           help="Unique identifier for the applicant")
    age = st.number_input("Age (Years)", min_value=18, max_value=100, value=34,
                         help="Applicant's age")
    location = st.text_input("Location", value="New York, USA",
                            help="Geographic location")

    # Employment Information Section
    st.markdown("### 💼 Employment Information")
    emp_type = st.selectbox("Employment Type",
                           ["Full-Time", "Part-Time", "Self-Employed", "Unemployed"],
                           help="Type of employment")
    income = st.number_input("Annual Income ($)", value=95000, min_value=0,
                            help="Total annual income")

    # Financial Information Section
    st.markdown("### 💰 Financial Information")
    credit_score = st.slider("Credit Score", 300, 850, 720,
                            help="Credit score range (300-850)")
    liabilities = st.number_input("Monthly Liabilities ($)", value=1200, min_value=0,
                                 help="Existing monthly debt obligations")

    # Loan Information Section
    st.markdown("### 🏷️ Loan Information")
    loan_amt = st.number_input("Requested Loan Amount ($)", value=25000, min_value=1000,
                              help="Amount of loan requested")
    tenure = st.number_input("Tenure (Months)", value=36, min_value=6, max_value=360,
                            help="Loan repayment period")

st.markdown("---")

# Main Evaluation Button with Enhanced Styling
col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
with col_btn2:
    evaluate_button = st.button("🚀 Evaluate Application", use_container_width=True,
                               key="eval_btn")

# Processing and Results Section
if evaluate_button:
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

    # Processing Indicator
    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.spinner("🔄 Multi-Agent Engine Analyzing Application..."):
        try:
            status_text.write("📡 Sending to backend analysis engine...")
            progress_bar.progress(25)

            response = requests.post("http://localhost:8000/api/v1/loan/evaluate", json=payload)
            progress_bar.progress(50)

            if response.status_code == 200:
                data = response.json()
                progress_bar.progress(75)

                # Decision Display with Color Coding
                decision = data['final_decision']['classification']
                risk_score = data['final_decision'].get('risk_score', 50)
                confidence = data['final_decision'].get('confidence_level', 'Medium')

                progress_bar.progress(100)
                status_text.success("✅ Analysis Complete!")

                # Main Decision Card
                st.markdown("---")
                if decision == "Approved":
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                                padding: 30px; border-radius: 12px; text-align: center;
                                border: 2px solid #00AA44; box-shadow: 0 4px 12px rgba(0,170,68,0.2);">
                        <h1 style="color: #00AA44; margin: 0;">✅ APPROVED</h1>
                        <p style="color: #333; font-size: 18px; margin: 10px 0;">Application meets all approval criteria</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif decision == "Requires Manual Review":
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
                                padding: 30px; border-radius: 12px; text-align: center;
                                border: 2px solid #FF8800; box-shadow: 0 4px 12px rgba(255,136,0,0.2);">
                        <h1 style="color: #FF8800; margin: 0;">⚠️ MANUAL REVIEW REQUIRED</h1>
                        <p style="color: #333; font-size: 18px; margin: 10px 0;">Application requires additional review</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
                                padding: 30px; border-radius: 12px; text-align: center;
                                border: 2px solid #DD3333; box-shadow: 0 4px 12px rgba(221,51,51,0.2);">
                        <h1 style="color: #DD3333; margin: 0;">❌ DECLINED</h1>
                        <p style="color: #333; font-size: 18px; margin: 10px 0;">Application does not meet approval criteria</p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Key Metrics Dashboard
                st.markdown("### 📊 Decision Metrics Dashboard")
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                with metric_col1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                                padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #0066CC;">
                        <p style="color: #666; font-size: 12px; margin: 0;">Risk Score</p>
                        <h2 style="color: #0066CC; margin: 5px 0 0 0;">{risk_score}/100</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with metric_col2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                                padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #00AA44;">
                        <p style="color: #666; font-size: 12px; margin: 0;">Confidence Level</p>
                        <h2 style="color: #00AA44; margin: 5px 0 0 0;">{confidence}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                dti = (data['financial_risk_data'].get('debt_to_income_ratio', 0))
                with metric_col3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
                                padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #FF8800;">
                        <p style="color: #666; font-size: 12px; margin: 0;">Debt-to-Income</p>
                        <h2 style="color: #FF8800; margin: 5px 0 0 0;">{dti:.2%}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                with metric_col4:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
                                padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #9C27B0;">
                        <p style="color: #666; font-size: 12px; margin: 0;">Credit Score</p>
                        <h2 style="color: #9C27B0; margin: 5px 0 0 0;">{credit_score}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # Detailed Analysis Tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "👤 Applicant Profile",
                    "📊 Financial Analysis",
                    "🧠 Decision Reasoning",
                    "🔄 Counterfactuals",
                    "🛡️ Compliance"
                ])

                with tab1:
                    st.markdown("### Applicant Profile Analysis")
                    st.json(data['applicant_profile_data'])

                with tab2:
                    st.markdown("### Financial Risk Assessment")
                    st.json(data['financial_risk_data'])

                with tab3:
                    st.markdown("### Decision Analysis")
                    decision_data = data['final_decision'].copy()
                    # Remove counterfactuals for cleaner display
                    counterfactuals = decision_data.pop('counterfactuals', [])
                    st.json(decision_data)

                with tab4:
                    st.markdown("### What-If Scenarios (Counterfactual Analysis)")
                    counterfactuals = data['final_decision'].get('counterfactuals', [])
                    if counterfactuals:
                        for i, cf in enumerate(counterfactuals, 1):
                            with st.expander(f"📌 Scenario {i}: {cf.get('scenario', 'Unknown')}"):
                                col_cf1, col_cf2 = st.columns(2)
                                with col_cf1:
                                    st.write(f"**Change:** {cf.get('change', 'N/A')}")
                                    st.write(f"**Timeline:** {cf.get('timeline', 'N/A')}")
                                with col_cf2:
                                    st.write(f"**Impact:** {cf.get('impact', 'N/A')}")
                                    st.write(f"**Difficulty:** {cf.get('difficulty', 'N/A')}")
                    else:
                        st.info("No counterfactual scenarios available for this decision.")

                with tab5:
                    st.markdown("### Compliance & Audit Trail")
                    st.json(data['compliance_action'])

                st.markdown("---")
                st.success("✅ Evaluation completed successfully!")

            else:
                st.error(f"❌ Backend Error: {response.status_code}")
                st.write("Failed to get response from the backend service.")

        except requests.exceptions.ConnectionError:
            st.error("❌ Connection Error: Cannot reach backend at localhost:8000")
            st.info("💡 Please ensure the FastAPI backend is running on http://localhost:8000")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666; font-size: 12px;">
    <p>🏦 <strong>Agentic AI Loan Approval System</strong></p>
    <p>Powered by Multi-Agent Architecture | Real-time Decision Engine | Explainable AI</p>
    <p>© 2026 - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
