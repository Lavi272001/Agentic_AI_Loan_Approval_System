# MCP Server for Decision Synthesis
# Synthesizes loan approval decisions based on risk assessment
from fastmcp import FastMCP

mcp = FastMCP("ApplicantDB")

@mcp.tool()
def get_applicant_profile(applicant_id: str) -> dict:
    """Fetches employment type, income, and basic credit background for an applicant."""
    # Mock data - in production, query your actual database here
    return {
        "applicant_id": applicant_id,
        "income": 95000,
        "employment_type": "Full-Time",
        "years_employed": 4,
        "credit_score": 720
    }

if __name__ == "__main__":
    mcp.run()