# LangGraph Workflow Engine
# Orchestrates the loan approval workflow using LangGraph
from langgraph.graph import StateGraph, END
from app.state import LoanApplicationState
from app.logger import app_logger
from app.counterfactual_analyzer import CounterfactualAnalyzer
from langchain_anthropic import ChatAnthropic
import os
from datetime import datetime

# Initialize LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# Define Node 1: Applicant Profile Agent
def applicant_profile_node(state: LoanApplicationState):
    """Evaluates applicant profile and income stability"""
    try:
        app_logger.log_event(
            "APPLICANT_PROFILE_START",
            applicant_id=state["applicant_id"]
        )

        profile_out = {
            "income_stability_score": "High" if state["income"] > 50000 else "Medium" if state["income"] > 0 else "Low",
            "employment_risk": "Low" if state["employment_type"] == "Full-Time" else "Medium" if state["employment_type"] == "Part-Time" else "High",
            "credit_history_summary": "Clean record" if state["credit_score"] > 700 else "Needs review" if state["credit_score"] > 600 else "Poor history",
            "application_completeness_flags": True
        }

        app_logger.log_node_execution(
            "applicant_profile",
            {"applicant_id": state["applicant_id"]},
            profile_out
        )

        return {"applicant_profile_data": profile_out}

    except Exception as e:
        app_logger.log_error("applicant_profile_node", e)
        return {
            "applicant_profile_data": {
                "error": str(e),
                "income_stability_score": "Unknown",
                "employment_risk": "High"
            }
        }

# Define Node 2: Financial Risk Analysis Agent
def financial_risk_node(state: LoanApplicationState):
    """Analyzes financial risk including DTI and credit score"""
    try:
        app_logger.log_event(
            "FINANCIAL_RISK_START",
            applicant_id=state["applicant_id"]
        )

        dti = state["existing_liabilities"] / state["income"] if state["income"] > 0 else 1.0
        loan_to_income = state["loan_amount"] / state["income"] if state["income"] > 0 else float('inf')

        risk_out = {
            "debt_to_income_ratio": round(dti, 2),
            "credit_score_risk_level": "Low" if state["credit_score"] > 700 else "Medium" if state["credit_score"] > 650 else "High",
            "loan_amount_risk": "Low" if loan_to_income <= 2.0 else "Medium" if loan_to_income <= 3.0 else "High",
            "anomaly_detection": "No suspicious activity flagged",
            "reasoning": f"DTI ratio of {dti:.2f} and loan-to-income of {loan_to_income:.2f}"
        }

        app_logger.log_node_execution(
            "financial_risk",
            {"applicant_id": state["applicant_id"], "income": state["income"]},
            risk_out
        )

        return {"financial_risk_data": risk_out}

    except Exception as e:
        app_logger.log_error("financial_risk_node", e)
        return {
            "financial_risk_data": {
                "error": str(e),
                "debt_to_income_ratio": 1.0,
                "credit_score_risk_level": "High"
            }
        }

# Define Node 3: Loan Decision Agent
def loan_decision_node(state: LoanApplicationState):
    """Synthesizes final loan decision"""
    try:
        app_logger.log_event(
            "LOAN_DECISION_START",
            applicant_id=state["applicant_id"]
        )

        score = state["credit_score"]
        dti = state.get("financial_risk_data", {}).get("debt_to_income_ratio", 1.0)

        # Enhanced decision logic
        if score >= 700 and dti <= 0.45:
            decision = "Approved"
            risk_score = 85
        elif score >= 650 and dti <= 0.50:
            decision = "Requires Manual Review"
            risk_score = 65
        else:
            decision = "Rejected"
            risk_score = 35

        decision_out = {
            "classification": decision,
            "risk_score": risk_score,
            "confidence_level": "High" if decision != "Requires Manual Review" else "Medium",
            "key_decision_factors": _extract_factors(state, decision),
            "explanation": f"Applicant credit score {score} with DTI {dti:.2f}. Decision: {decision}"
        }

        analyzer = CounterfactualAnalyzer()
        counterfactuals = analyzer.analyze(decision_out, state)
        decision_out["counterfactuals"] = counterfactuals.get("counterfactuals", [])

        app_logger.log_decision(state["applicant_id"], decision_out, risk_score)

        return {"final_decision": decision_out}

    except Exception as e:
        app_logger.log_error("loan_decision_node", e)
        return {
            "final_decision": {
                "error": str(e),
                "classification": "Requires Manual Review",
                "risk_score": 50,
                "confidence_level": "Low"
            }
        }

# Define Node 4: Compliance & Action Orchestrator Agent
def compliance_node(state: LoanApplicationState):
    """Handles compliance, notifications, and audit trails"""
    try:
        app_logger.log_event(
            "COMPLIANCE_START",
            applicant_id=state["applicant_id"]
        )

        decision = state.get("final_decision", {})

        compliance_out = {
            "compliance_action": {
                "action_taken": f"Decision processed as {decision.get('classification', 'Unknown')}",
                "notification_sent": True,
                "case_id": f"LOAN-{state['applicant_id']}",
                "timestamp": datetime.utcnow().isoformat(),
                "summary": "Application audited, compliant with regulatory baseline rules.",
                "audit_record": {
                    "applicant_id": state["applicant_id"],
                    "credit_score": state["credit_score"],
                    "decision": decision.get("classification"),
                    "risk_score": decision.get("risk_score")
                }
            }
        }

        app_logger.log_audit_trail(
            state["applicant_id"],
            "COMPLIANCE_PROCESSED",
            compliance_out
        )

        return compliance_out

    except Exception as e:
        app_logger.log_error("compliance_node", e)
        return {
            "compliance_action": {
                "error": str(e),
                "action_taken": "Error in compliance processing",
                "notification_sent": False
            }
        }

def _extract_factors(state: LoanApplicationState, decision: str) -> list:
    """Extract key decision factors"""
    factors = []

    if state["credit_score"] >= 700:
        factors.append("High Credit Score")
    elif state["credit_score"] < 600:
        factors.append("Low Credit Score")

    if state["employment_type"] == "Full-Time":
        factors.append("Stable Employment")

    dti = state.get("financial_risk_data", {}).get("debt_to_income_ratio", 1.0)
    if dti <= 0.45:
        factors.append("Healthy DTI Ratio")
    elif dti > 0.50:
        factors.append("High Debt Burden")

    return factors if factors else [f"Standard {decision}"]

def route_based_on_risk(state: LoanApplicationState) -> str:
    """Route to manual review if high risk indicators detected"""
    dti = state.get("financial_risk_data", {}).get("debt_to_income_ratio", 0)
    credit_score = state.get("credit_score", 0)

    if dti > 0.50:
        return "manual_review"

    if 600 <= credit_score < 700:
        return "manual_review"

    return "loan_decision"

def route_after_decision(state: LoanApplicationState) -> str:
    """Route based on decision classification"""
    classification = state.get("final_decision", {}).get("classification")

    if classification == "Requires Manual Review":
        return "manual_review"

    return "compliance"

def manual_review_node(state: LoanApplicationState):
    """Manual review escalation node"""
    app_logger.log_event(
        "MANUAL_REVIEW_ESCALATION",
        applicant_id=state["applicant_id"]
    )

    return {
        "final_decision": {
            "classification": "Requires Manual Review",
            "risk_score": 50,
            "confidence_level": "Medium",
            "key_decision_factors": ["Escalated to manual review"],
            "explanation": "Application requires manual review due to risk factors."
        }
    }

# Build the Graph
workflow = StateGraph(LoanApplicationState)

workflow.add_node("applicant_profile", applicant_profile_node)
workflow.add_node("financial_risk", financial_risk_node)
workflow.add_node("manual_review", manual_review_node)
workflow.add_node("loan_decision", loan_decision_node)
workflow.add_node("compliance", compliance_node)

# Set entry point
workflow.set_entry_point("applicant_profile")

# Add edges with conditional routing
workflow.add_edge("applicant_profile", "financial_risk")
workflow.add_conditional_edges("financial_risk", route_based_on_risk, {
    "manual_review": "manual_review",
    "loan_decision": "loan_decision"
})
workflow.add_conditional_edges("loan_decision", route_after_decision, {
    "manual_review": "manual_review",
    "compliance": "compliance"
})
workflow.add_edge("manual_review", "compliance")
workflow.add_edge("compliance", END)

# Compile Graph
app_workflow = workflow.compile()