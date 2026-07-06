# MCP Server for Notification System
# Handles sending notifications about loan decisions
from fastmcp import FastMCP
from typing import Dict, Any
from datetime import datetime
import json

mcp = FastMCP("NotificationSystem")

# In-memory audit log (in production, use database)
AUDIT_LOG = []

@mcp.tool()
def send_notification(applicant_id: str, decision: str, recipient_email: str = None) -> Dict[str, Any]:
    """Sends notification about loan decision to applicant."""
    try:
        timestamp = datetime.utcnow().isoformat()

        notification = {
            "applicant_id": applicant_id,
            "decision": decision,
            "recipient": recipient_email or f"{applicant_id}@applicant.local",
            "timestamp": timestamp,
            "status": "sent"
        }

        # Log the notification
        AUDIT_LOG.append(notification)

        # Generate notification message
        messages = {
            "Approved": "Congratulations! Your loan application has been approved.",
            "Requires Manual Review": "Your loan application is under manual review. We will contact you soon.",
            "Rejected": "Your loan application has been reviewed. Please contact us for more information."
        }

        return {
            "success": True,
            "notification_id": f"NOTIF-{applicant_id}-{len(AUDIT_LOG)}",
            "applicant_id": applicant_id,
            "decision": decision,
            "message": messages.get(decision, "Application update"),
            "recipient": recipient_email or f"{applicant_id}@applicant.local",
            "sent_at": timestamp,
            "status": "sent"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def log_decision(case_id: str, decision: Dict[str, Any], applicant_id: str) -> Dict[str, Any]:
    """Logs loan decision to audit trail."""
    try:
        timestamp = datetime.utcnow().isoformat()

        audit_entry = {
            "case_id": case_id,
            "applicant_id": applicant_id,
            "decision": decision.get("classification", "Unknown"),
            "risk_score": decision.get("risk_score", 0),
            "confidence_level": decision.get("confidence_level", "Unknown"),
            "timestamp": timestamp,
            "logged_at": timestamp,
            "decision_factors": decision.get("key_decision_factors", []),
            "explanation": decision.get("explanation", "")
        }

        AUDIT_LOG.append(audit_entry)

        return {
            "success": True,
            "case_id": case_id,
            "log_entry_id": f"LOG-{len(AUDIT_LOG)}",
            "applicant_id": applicant_id,
            "decision_logged": True,
            "timestamp": timestamp,
            "log_status": "recorded"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def get_audit_trail(applicant_id: str = None, case_id: str = None) -> Dict[str, Any]:
    """Retrieves audit trail for an applicant or case."""
    try:
        filtered_logs = AUDIT_LOG

        if applicant_id:
            filtered_logs = [log for log in filtered_logs if log.get("applicant_id") == applicant_id]

        if case_id:
            filtered_logs = [log for log in filtered_logs if log.get("case_id") == case_id]

        # Sort by timestamp (most recent first)
        filtered_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return {
            "success": True,
            "applicant_id": applicant_id,
            "case_id": case_id,
            "total_entries": len(filtered_logs),
            "audit_trail": filtered_logs,
            "earliest_entry": filtered_logs[-1].get("timestamp") if filtered_logs else None,
            "latest_entry": filtered_logs[0].get("timestamp") if filtered_logs else None
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def send_compliance_report(case_id: str, decision: str, compliance_notes: str = None) -> Dict[str, Any]:
    """Generates and sends compliance report."""
    try:
        timestamp = datetime.utcnow().isoformat()

        report = {
            "case_id": case_id,
            "decision": decision,
            "compliance_status": "compliant",
            "report_timestamp": timestamp,
            "compliance_notes": compliance_notes or "Application meets regulatory baseline requirements",
            "regulatory_checks": {
                "fair_lending": "passed",
                "data_privacy": "passed",
                "audit_trail": "recorded"
            }
        }

        return {
            "success": True,
            "case_id": case_id,
            "report_id": f"COMP-{case_id}",
            "compliance_status": "compliant",
            "timestamp": timestamp,
            "report": report
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()