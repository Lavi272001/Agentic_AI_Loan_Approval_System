# MCP Server for Applicant Database
# Handles applicant profile management and queries
from fastmcp import FastMCP
import mysql.connector
from typing import Dict, Any, Optional

mcp = FastMCP("ApplicantDB")

def get_db_connection():
    """Create database connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tek@12345",
        database="loan_approval_db"
    )

@mcp.tool()
def get_applicant_profile(applicant_id: str) -> Dict[str, Any]:
    """Fetches applicant profile including income, employment, and credit information."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM applicants WHERE applicant_id = %s", (applicant_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return {
                "success": True,
                "applicant_id": result["applicant_id"],
                "age": result["age"],
                "income": float(result["income"]),
                "employment_type": result["employment_type"],
                "credit_score": result["credit_score"],
                "loan_amount": float(result["loan_amount"]),
                "existing_liabilities": float(result["existing_liabilities"]),
                "location": result["location"]
            }
        return {"success": False, "error": f"Applicant {applicant_id} not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def query_applicant_history(applicant_id: str) -> Dict[str, Any]:
    """Retrieves historical applications for an applicant."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT applicant_id, credit_score, income, employment_type, timestamp
            FROM applicants
            WHERE applicant_id = %s
            ORDER BY timestamp DESC
        """, (applicant_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return {
            "success": True,
            "applicant_id": applicant_id,
            "application_count": len(results),
            "applications": results
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
def validate_applicant_id(applicant_id: str) -> Dict[str, Any]:
    """Validates whether an applicant ID exists in the system."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM applicants WHERE applicant_id = %s", (applicant_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        return {
            "success": True,
            "applicant_id": applicant_id,
            "exists": count > 0,
            "message": f"Applicant {applicant_id} {'found' if count > 0 else 'not found'}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run()