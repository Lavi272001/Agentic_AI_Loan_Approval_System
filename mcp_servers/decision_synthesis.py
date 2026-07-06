# MCP Server for Decision Synthesis
# Synthesizes loan approval decisions based on risk assessment
from fastmcp import FastMCP
from typing import Dict, Any, List

mcp = FastMCP("DecisionSynthesis")

@mcp.tool()
def synthesize_decision(profile: Dict[str, Any], risk_assessment: Dict[str, Any],
                       financial_data: Dict[str, Any]) -> Dict[str, Any]:
    """Synthesizes final loan decision from multiple data sources."""
    try:
        credit_score = profile.get("credit_score", 0)
        dti_ratio = financial_data.get("debt_to_income_ratio", 1.0)
        risk_score = risk_assessment.get("risk_score", 50)

        # Decision logic
        if credit_score >= 700 and dti_ratio <= 0.45 and risk_score >= 70:
            classification = "Approved"
            confidence = "High"
            final_risk_score = risk_score
        elif credit_score >= 650 and dti_ratio <= 0.50 and risk_score >= 50:
            classification = "Requires Manual Review"
            confidence = "Medium"
            final_risk_score = risk_score - 10
        else:
            classification = "Rejected"
            confidence = "High"
            final_risk_score = risk_score

        return {
            "success": True,
            "classification": classification,
            "risk_score": final_risk_score,
            "confidence_level": confidence,
            "key_factors": _extract_key_factors(profile, financial_data, risk_assessment),
            "explanation": _generate_explanation(classification, credit_score, dti_ratio),
            "review_required": classification == "Requires Manual Review"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def generate_explanation(decision: str, factors: List[str],
                        credit_score: int) -> Dict[str, Any]:
    """Generates detailed explanation for the decision."""
    try:
        explanation_map = {
            "Approved": f"Applicant meets core credit criteria with a score of {credit_score}. Strong financial position supports loan approval.",
            "Requires Manual Review": f"Applicant score {credit_score} warrants manual review due to borderline risk factors.",
            "Rejected": f"Applicant score {credit_score} does not meet minimum lending criteria."
        }

        return {
            "success": True,
            "decision": decision,
            "explanation": explanation_map.get(decision, "Unable to generate explanation"),
            "key_factors": factors,
            "credit_score": credit_score,
            "requires_reviewer_attention": decision != "Approved"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def score_risk(profile: Dict[str, Any], financials: Dict[str, Any]) -> Dict[str, Any]:
    """Calculates comprehensive risk score."""
    try:
        score = 100

        # Credit score component (40 points)
        credit = profile.get("credit_score", 0)
        if credit >= 750:
            score -= 0
        elif credit >= 700:
            score -= 5
        elif credit >= 650:
            score -= 15
        else:
            score -= 25

        # DTI component (30 points)
        dti = financials.get("debt_to_income_ratio", 0)
        if dti <= 0.30:
            score -= 0
        elif dti <= 0.45:
            score -= 10
        elif dti <= 0.50:
            score -= 20
        else:
            score -= 30

        # Income stability (20 points)
        income = profile.get("income", 0)
        employment = profile.get("employment_type", "")
        if income > 100000 and employment == "Full-Time":
            score -= 0
        elif income > 50000:
            score -= 5
        elif income > 0:
            score -= 15
        else:
            score -= 20

        # Loan amount reasonableness (10 points)
        loan_ratio = financials.get("loan_to_income", 2.0)
        if loan_ratio <= 2.0:
            score -= 0
        elif loan_ratio <= 3.0:
            score -= 5
        else:
            score -= 10

        return {
            "success": True,
            "risk_score": max(0, score),
            "risk_level": _determine_risk_level(score),
            "components": {
                "credit_score_component": credit,
                "dti_component": dti,
                "income_component": income,
                "loan_ratio_component": loan_ratio
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def _extract_key_factors(profile: Dict[str, Any], financials: Dict[str, Any],
                         risk_assessment: Dict[str, Any]) -> List[str]:
    """Extract key factors contributing to decision"""
    factors = []

    if profile.get("credit_score", 0) >= 700:
        factors.append("High Credit Score")

    if profile.get("employment_type") == "Full-Time":
        factors.append("Stable Employment")

    if financials.get("debt_to_income_ratio", 1) <= 0.45:
        factors.append("Healthy DTI Ratio")

    if risk_assessment.get("rules_passed"):
        factors.append("Passes Risk Assessment")

    return factors if factors else ["Standard Assessment"]

def _generate_explanation(classification: str, credit_score: int, dti_ratio: float) -> str:
    """Generate plain English explanation"""
    return f"Decision: {classification}. Credit Score: {credit_score}, DTI Ratio: {dti_ratio:.2f}"

def _determine_risk_level(score: int) -> str:
    """Determine risk level from score"""
    if score >= 80:
        return "LOW"
    elif score >= 60:
        return "MEDIUM"
    elif score >= 40:
        return "HIGH"
    else:
        return "CRITICAL"

if __name__ == "__main__":
    mcp.run()