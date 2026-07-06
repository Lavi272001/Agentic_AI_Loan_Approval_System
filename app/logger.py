# Production Logging System
# Provides structured logging with correlation IDs for audit trails

import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
import uuid

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.correlation_id = None
        self.setup_logging()

    def setup_logging(self):
        """Configure logging with structured format"""
        handler = logging.FileHandler("loan_approval.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Also add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def set_correlation_id(self, correlation_id: str = None):
        """Set correlation ID for request tracking"""
        self.correlation_id = correlation_id or str(uuid.uuid4())

    def log_event(self, event_type: str, level: str = "INFO", **context):
        """Log structured event with context"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "correlation_id": self.correlation_id,
            "event_type": event_type,
            "context": context
        }

        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(json.dumps(log_entry))

    def log_workflow_start(self, applicant_id: str, state: Dict[str, Any]):
        """Log workflow initiation"""
        self.log_event(
            "WORKFLOW_START",
            applicant_id=applicant_id,
            fields=list(state.keys())
        )

    def log_node_execution(self, node_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """Log agent node execution"""
        self.log_event(
            "NODE_EXECUTION",
            node=node_name,
            input_keys=list(inputs.keys()),
            output_keys=list(outputs.keys())
        )

    def log_decision(self, applicant_id: str, decision: Dict[str, Any], risk_score: float):
        """Log final loan decision"""
        self.log_event(
            "DECISION_LOGGED",
            applicant_id=applicant_id,
            classification=decision.get("classification"),
            risk_score=risk_score,
            confidence=decision.get("confidence_level")
        )

    def log_error(self, node_name: str, error: Exception):
        """Log node error"""
        self.log_event(
            "ERROR",
            level="ERROR",
            node=node_name,
            error_type=type(error).__name__,
            error_message=str(error)
        )

    def log_audit_trail(self, applicant_id: str, action: str, details: Dict[str, Any]):
        """Log audit trail event"""
        self.log_event(
            "AUDIT_TRAIL",
            applicant_id=applicant_id,
            action=action,
            details=details
        )

# Global logger instance
app_logger = StructuredLogger("LoanApprovalSystem")
