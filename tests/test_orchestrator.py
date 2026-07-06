import pytest
from app.orchestrator import (
    applicant_profile_node,
    financial_risk_node,
    loan_decision_node,
    compliance_node,
    app_workflow
)


class TestApplicantProfileNode:
    """Test applicant profile assessment"""

    def test_high_income_stability(self, sample_state):
        """High income should indicate high stability"""
        result = applicant_profile_node(sample_state)
        assert result["applicant_profile_data"]["income_stability_score"] in ["High", "Medium"]

    def test_low_income_stability(self, rejected_state):
        """Low income should indicate low stability"""
        result = applicant_profile_node(rejected_state)
        assert result["applicant_profile_data"]["income_stability_score"] == "Low"

    def test_full_time_employment(self, sample_state):
        """Full-time employment should be low risk"""
        result = applicant_profile_node(sample_state)
        assert result["applicant_profile_data"]["employment_risk"] == "Low"

    def test_unemployed_employment(self, rejected_state):
        """Unemployed should be high risk"""
        result = applicant_profile_node(rejected_state)
        assert result["applicant_profile_data"]["employment_risk"] == "High"

    def test_application_completeness(self, sample_state):
        """All required fields present"""
        result = applicant_profile_node(sample_state)
        assert result["applicant_profile_data"]["application_completeness_flags"] == True

    def test_age_verification(self, sample_state):
        """Age should be verified"""
        result = applicant_profile_node(sample_state)
        assert result["applicant_profile_data"]["age_verification"] == True

    def test_profile_data_structure(self, sample_state):
        """Profile data should have all required fields"""
        result = applicant_profile_node(sample_state)
        profile = result["applicant_profile_data"]
        assert "income_stability_score" in profile
        assert "employment_risk" in profile
        assert "credit_history_summary" in profile
        assert "application_completeness_flags" in profile


class TestFinancialRiskNode:
    """Test financial risk analysis"""

    def test_healthy_dti_ratio(self, approved_state):
        """Good DTI ratio should indicate low risk"""
        result = financial_risk_node(approved_state)
        dti = result["financial_risk_data"]["debt_to_income_ratio"]
        assert dti <= 0.45, f"DTI {dti} exceeds 0.45 threshold"

    def test_high_dti_ratio(self, rejected_state):
        """High DTI ratio should indicate high risk"""
        result = financial_risk_node(rejected_state)
        dti = result["financial_risk_data"]["debt_to_income_ratio"]
        assert dti > 0.50, f"DTI {dti} should be > 0.50"

    def test_credit_score_risk_excellent(self, approved_state):
        """Excellent credit score"""
        result = financial_risk_node(approved_state)
        assert result["financial_risk_data"]["credit_score_risk_level"] == "Low"

    def test_credit_score_risk_poor(self, rejected_state):
        """Poor credit score"""
        result = financial_risk_node(rejected_state)
        assert result["financial_risk_data"]["credit_score_risk_level"] == "High"

    def test_loan_to_income_ratio(self, sample_state):
        """Loan should not exceed recommended multiple of income"""
        result = financial_risk_node(sample_state)
        ratio = sample_state["loan_amount"] / sample_state["income"]
        assert ratio <= 1.0, f"Loan to income ratio {ratio} exceeds 1.0"

    def test_financial_data_structure(self, sample_state):
        """Financial risk data should have all required fields"""
        result = financial_risk_node(sample_state)
        risk = result["financial_risk_data"]
        assert "debt_to_income_ratio" in risk
        assert "credit_score_risk_level" in risk
        assert "loan_risk_assessment" in risk
        assert "anomaly_detection_flags" in risk


class TestLoanDecisionNode:
    """Test loan decision logic"""

    def test_approved_high_credit_low_dti(self, approved_state):
        """High credit score + low DTI = Approved"""
        state_with_risk = financial_risk_node(approved_state)
        result = loan_decision_node(state_with_risk)
        assert result["final_decision"]["classification"] == "Approved"

    def test_rejected_low_credit_high_dti(self, rejected_state):
        """Low credit score + high DTI = Rejected"""
        state_with_risk = financial_risk_node(rejected_state)
        result = loan_decision_node(state_with_risk)
        assert result["final_decision"]["classification"] == "Rejected"

    def test_decision_has_confidence(self, sample_state):
        """Decision includes confidence level"""
        state_with_risk = financial_risk_node(sample_state)
        result = loan_decision_node(state_with_risk)
        assert result["final_decision"]["confidence_level"] in ["High", "Medium", "Low"]

    def test_decision_has_factors(self, sample_state):
        """Decision includes key factors"""
        state_with_risk = financial_risk_node(sample_state)
        result = loan_decision_node(state_with_risk)
        factors = result["final_decision"]["key_decision_factors"]
        assert len(factors) > 0, "Decision should have key factors"

    def test_decision_has_explanation(self, sample_state):
        """Decision includes explanation"""
        state_with_risk = financial_risk_node(sample_state)
        result = loan_decision_node(state_with_risk)
        explanation = result["final_decision"]["explanation"]
        assert len(explanation) > 0, "Decision should have explanation"

    def test_risk_score_in_range(self, sample_state):
        """Risk score should be between 0-100"""
        state_with_risk = financial_risk_node(sample_state)
        result = loan_decision_node(state_with_risk)
        risk_score = result["final_decision"]["risk_score"]
        assert 0 <= risk_score <= 100, f"Risk score {risk_score} out of range"

    def test_decision_data_structure(self, sample_state):
        """Decision data should have all required fields"""
        state_with_risk = financial_risk_node(sample_state)
        result = loan_decision_node(state_with_risk)
        decision = result["final_decision"]
        assert "classification" in decision
        assert "risk_score" in decision
        assert "confidence_level" in decision
        assert "key_decision_factors" in decision
        assert "explanation" in decision


class TestComplianceNode:
    """Test compliance and audit trail"""

    def test_compliance_creates_case_id(self, sample_state):
        """Compliance creates case ID"""
        state_with_decision = {
            **sample_state,
            "final_decision": {"classification": "Approved"}
        }
        result = compliance_node(state_with_decision)
        assert "case_id" in result["compliance_action"]
        assert result["compliance_action"]["case_id"].startswith("LOAN-")

    def test_compliance_sends_notification(self, sample_state):
        """Compliance marks notification as sent"""
        state_with_decision = {
            **sample_state,
            "final_decision": {"classification": "Approved"}
        }
        result = compliance_node(state_with_decision)
        assert result["compliance_action"]["notification_sent"] == True

    def test_compliance_has_timestamp(self, sample_state):
        """Compliance records timestamp"""
        state_with_decision = {
            **sample_state,
            "final_decision": {"classification": "Approved"}
        }
        result = compliance_node(state_with_decision)
        assert "timestamp" in result["compliance_action"]

    def test_compliance_action_structure(self, sample_state):
        """Compliance action should have all required fields"""
        state_with_decision = {
            **sample_state,
            "final_decision": {"classification": "Approved"}
        }
        result = compliance_node(state_with_decision)
        action = result["compliance_action"]
        assert "action_taken" in action
        assert "notification_sent" in action
        assert "case_id" in action
        assert "timestamp" in action


class TestEndToEndWorkflow:
    """Test complete workflow execution"""

    def test_workflow_execution_success(self, sample_state):
        """Complete workflow should execute without error"""
        result = app_workflow.invoke(sample_state)
        assert result is not None
        assert "final_decision" in result
        assert "compliance_action" in result

    def test_workflow_produces_decision(self, sample_state):
        """Workflow should produce a decision"""
        result = app_workflow.invoke(sample_state)
        decision = result["final_decision"]["classification"]
        assert decision in ["Approved", "Rejected", "Requires Manual Review"]

    def test_workflow_produces_audit_trail(self, sample_state):
        """Workflow should produce audit trail"""
        result = app_workflow.invoke(sample_state)
        assert result["compliance_action"]["case_id"].startswith("LOAN-")

    def test_approved_workflow(self, approved_state):
        """Workflow with approved applicant"""
        result = app_workflow.invoke(approved_state)
        decision = result["final_decision"]["classification"]
        assert decision == "Approved"

    def test_rejected_workflow(self, rejected_state):
        """Workflow with rejected applicant"""
        result = app_workflow.invoke(rejected_state)
        decision = result["final_decision"]["classification"]
        assert decision == "Rejected"

    def test_workflow_state_propagation(self, sample_state):
        """State should propagate through entire workflow"""
        result = app_workflow.invoke(sample_state)
        assert result["applicant_id"] == sample_state["applicant_id"]
        assert result["income"] == sample_state["income"]
        assert result["credit_score"] == sample_state["credit_score"]

    def test_workflow_data_enrichment(self, sample_state):
        """Workflow should enrich input state with analysis results"""
        result = app_workflow.invoke(sample_state)
        assert result.get("applicant_profile_data") is not None
        assert result.get("financial_risk_data") is not None
        assert result.get("final_decision") is not None
        assert result.get("compliance_action") is not None
