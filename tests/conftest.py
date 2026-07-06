import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_state():
    """Sample loan application state"""
    return {
        "applicant_id": "APP-TEST-001",
        "age": 34,
        "income": 95000,
        "employment_type": "Full-Time",
        "credit_score": 720,
        "loan_amount": 25000,
        "tenure": 36,
        "existing_liabilities": 1200,
        "location": "New York",
        "applicant_profile_data": None,
        "financial_risk_data": None,
        "final_decision": None,
        "compliance_action": None,
        "next_step": ""
    }

@pytest.fixture
def approved_state():
    """Pre-approved applicant state"""
    return {
        "applicant_id": "APP-APPROVED-001",
        "age": 42,
        "income": 150000,
        "employment_type": "Full-Time",
        "credit_score": 780,
        "loan_amount": 50000,
        "tenure": 60,
        "existing_liabilities": 2000,
        "location": "San Francisco",
        "applicant_profile_data": None,
        "financial_risk_data": None,
        "final_decision": None,
        "compliance_action": None,
        "next_step": ""
    }

@pytest.fixture
def rejected_state():
    """Applicant likely to be rejected"""
    return {
        "applicant_id": "APP-REJECTED-001",
        "age": 28,
        "income": 30000,
        "employment_type": "Unemployed",
        "credit_score": 550,
        "loan_amount": 100000,
        "tenure": 60,
        "existing_liabilities": 25000,
        "location": "Chicago",
        "applicant_profile_data": None,
        "financial_risk_data": None,
        "final_decision": None,
        "compliance_action": None,
        "next_step": ""
    }
