# LangGraph Shared State
# Defines the shared state structure for the workflow
from typing import TypedDict, Optional, Dict, Any

class LoanApplicationState(TypedDict):
    # Inputs
    applicant_id: str
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure: int
    existing_liabilities: float
    
    # Agent Outputs
    applicant_profile_data: Optional[Dict[str, Any]]
    financial_risk_data: Optional[Dict[str, Any]]
    final_decision: Optional[Dict[str, Any]]
    compliance_action: Optional[Dict[str, Any]]
    
    # Internal routing control
    next_step: str