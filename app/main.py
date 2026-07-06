# FastAPI Microservice
# Main entry point for the loan approval system API
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from app.orchestrator import app_workflow
from app.logger import app_logger
import uuid
from datetime import datetime

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

class ErrorResponse(BaseModel):
    error: str
    correlation_id: str
    timestamp: str

@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    """Add correlation ID to all requests for tracking"""
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    app_logger.set_correlation_id(correlation_id)
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Loan Approval System"
    }

@app.post("/api/v1/loan/evaluate")
async def evaluate_application(application: LoanApplicationRequest):
    """Evaluate loan application through multi-agent workflow"""
    try:
        app_logger.log_event(
            "LOAN_APPLICATION_RECEIVED",
            applicant_id=application.applicant_id,
            income=application.income,
            credit_score=application.credit_score
        )

        # Validate input
        if application.income < 0 or application.loan_amount < 0:
            app_logger.log_event(
                "VALIDATION_ERROR",
                level="ERROR",
                applicant_id=application.applicant_id,
                error="Negative income or loan amount"
            )
            raise ValueError("Income and loan amount must be non-negative")

        # Construct initial state
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

        app_logger.log_workflow_start(application.applicant_id, initial_state)

        # Run workflow with error handling
        try:
            final_output = app_workflow.invoke(initial_state)
        except Exception as workflow_error:
            app_logger.log_error("app_workflow.invoke", workflow_error)
            # Return partial results with error noted
            final_output = {
                **initial_state,
                "error": str(workflow_error),
                "workflow_status": "failed"
            }

        app_logger.log_event(
            "LOAN_APPLICATION_COMPLETED",
            applicant_id=application.applicant_id,
            decision=final_output.get("final_decision", {}).get("classification", "Unknown")
        )

        return final_output

    except ValidationError as ve:
        app_logger.log_event(
            "VALIDATION_ERROR",
            level="ERROR",
            error=str(ve)
        )
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid request data", "details": str(ve)}
        )

    except ValueError as ve:
        app_logger.log_event(
            "VALUE_ERROR",
            level="ERROR",
            error=str(ve)
        )
        raise HTTPException(
            status_code=400,
            detail={"error": str(ve)}
        )

    except Exception as e:
        app_logger.log_event(
            "UNEXPECTED_ERROR",
            level="ERROR",
            error_type=type(e).__name__,
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "message": str(e),
                "correlation_id": app_logger.correlation_id
            }
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    app_logger.log_event(
        "HTTP_EXCEPTION",
        level="ERROR",
        status_code=exc.status_code,
        detail=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "correlation_id": app_logger.correlation_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)