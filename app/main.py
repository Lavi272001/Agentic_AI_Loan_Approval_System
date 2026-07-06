# FastAPI Microservice
# Main entry point for the loan approval system API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.orchestrator import app_workflow

app = FastAPI(title="Agentic AI Intelligent Loan Approval System")

class LoanApplicationRequest(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure: int
    existing_liabilities: float
    location: str

@app.post("/api/v1/loan/evaluate")
async def evaluate_application(application: LoanApplicationRequest):
    try:
        # Construct initial state mapping to LangGraph inputs
        initial_state = {
            "applicant_id": application.applicant_id,
            "income": application.income,
            "employment_type": application.employment_type,
            "credit_score": application.credit_score,
            "loan_amount": application.loan_amount,
            "tenure": application.tenure,
            "existing_liabilities": application.existing_liabilities,
            "applicant_profile_data": None,
            "financial_risk_data": None,
            "final_decision": None,
            "compliance_action": None,
            "next_step": ""
        }
        
        # Run graph execution
        final_output = app_workflow.invoke(initial_state)
        return final_output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)