from typing import Dict, Any, List


class CounterfactualAnalyzer:
    """Generates counterfactual explanations for loan decisions"""

    def analyze(self, decision: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate what-if scenarios for the decision"""

        counterfactuals = []

        credit_score = profile.get("credit_score", 0)
        income = profile.get("income", 1)
        existing_liabilities = profile.get("existing_liabilities", 0)

        # Credit score counterfactual
        if credit_score < 700:
            gap = 700 - credit_score
            counterfactuals.append({
                "scenario": "If credit score were 700",
                "change": f"+{gap} points",
                "impact": "Would likely qualify for approval or lower risk category",
                "difficulty": "High",
                "timeline": "24+ months of perfect payment history"
            })

        # DTI counterfactual
        dti = existing_liabilities / income if income > 0 else 1.0
        if dti > 0.45:
            target_dti = 0.45
            target_liabilities = income * target_dti
            reduction = existing_liabilities - target_liabilities

            counterfactuals.append({
                "scenario": "If debt were lower",
                "change": f"-${reduction:.0f} liabilities",
                "impact": "Would improve DTI ratio to acceptable level",
                "difficulty": "Medium",
                "timeline": "6-12 months of debt paydown"
            })

        # Income counterfactual
        if dti > 0.50:
            income_needed = existing_liabilities / 0.45
            increase = income_needed - income
            counterfactuals.append({
                "scenario": "If income were higher",
                "change": f"+${increase:.0f}/year",
                "impact": "Would significantly improve debt-to-income ratio",
                "difficulty": "Medium",
                "timeline": "Career advancement or additional employment"
            })

        # Employment counterfactual
        employment_type = profile.get("employment_type", "")
        if employment_type == "Unemployed":
            counterfactuals.append({
                "scenario": "If employed full-time",
                "change": "Employment status change",
                "impact": "Would significantly improve income stability score",
                "difficulty": "Medium",
                "timeline": "Job placement required"
            })

        return {
            "current_decision": decision.get("classification"),
            "confidence": decision.get("confidence_level"),
            "counterfactuals": counterfactuals,
            "actionable_improvements": [
                c for c in counterfactuals
                if c["difficulty"] in ["Low", "Medium"]
            ]
        }
