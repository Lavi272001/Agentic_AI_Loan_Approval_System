# MCP Server for Risk Rules Database
# Manages risk assessment rules and criteria
from fastmcp import FastMCP
from typing import Dict, Any

mcp = FastMCP("RiskRulesDB")

# Risk thresholds and rules
RISK_RULES = {
    "credit_score_excellent": 750,
    "credit_score_good": 700,
    "credit_score_fair": 650,
    "credit_score_poor": 600,
    "max_dti_ratio": 0.5,
    "max_debt_to_income_ratio": 0.45,
    "min_employment_years": 1,
    "employment_stability_threshold": 2,
    "max_loan_to_income": 3.0,
}

@mcp.tool()
def evaluate_risk_rules(profile: Dict[str, Any], financials: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates applicant against risk assessment rules."""
    try:
        score = 100
        violations = []

        # Credit score evaluation
        if profile.get("credit_score", 0) < RISK_RULES["credit_score_poor"]:
            violations.append("Credit score below poor threshold")
            score -= 30
        elif profile.get("credit_score", 0) < RISK_RULES["credit_score_fair"]:
            violations.append("Credit score in fair range")
            score -= 15
        elif profile.get("credit_score", 0) < RISK_RULES["credit_score_good"]:
            violations.append("Credit score in good range")
            score -= 5

        # DTI ratio evaluation
        dti = financials.get("debt_to_income_ratio", 0)
        if dti > RISK_RULES["max_dti_ratio"]:
            violations.append(f"DTI ratio {dti:.2f} exceeds maximum {RISK_RULES['max_dti_ratio']}")
            score -= 25

        # Income verification
        if profile.get("income", 0) <= 0:
            violations.append("No valid income reported")
            score -= 40

        return {
            "success": True,
            "risk_score": max(0, score),
            "risk_level": _determine_risk_level(score),
            "violations": violations,
            "rules_passed": len(violations) == 0,
            "details": {
                "credit_score": profile.get("credit_score", 0),
                "dti_ratio": dti,
                "income": profile.get("income", 0)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_threshold(rule_name: str) -> Dict[str, Any]:
    """Retrieves specific risk rule threshold."""
    if rule_name in RISK_RULES:
        return {
            "success": True,
            "rule_name": rule_name,
            "threshold": RISK_RULES[rule_name],
            "description": _get_rule_description(rule_name)
        }
    return {"success": False, "error": f"Rule '{rule_name}' not found"}

@mcp.tool()
def apply_custom_rules(data: Dict[str, Any], custom_rules: Dict[str, Any] = None) -> Dict[str, Any]:
    """Applies custom rules to applicant data."""
    try:
        rules = RISK_RULES.copy()
        if custom_rules:
            rules.update(custom_rules)

        results = []
        for rule_name, threshold in rules.items():
            result = {
                "rule": rule_name,
                "threshold": threshold,
                "status": "applied"
            }
            results.append(result)

        return {
            "success": True,
            "total_rules": len(results),
            "results": results,
            "custom_rules_applied": bool(custom_rules)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

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

def _get_rule_description(rule_name: str) -> str:
    """Get human-readable description of a rule"""
    descriptions = {
        "credit_score_excellent": "Excellent credit score threshold",
        "credit_score_good": "Good credit score threshold",
        "max_dti_ratio": "Maximum debt-to-income ratio allowed",
        "max_loan_to_income": "Maximum loan amount relative to annual income"
    }
    return descriptions.get(rule_name, "Risk rule")

if __name__ == "__main__":
    mcp.run()