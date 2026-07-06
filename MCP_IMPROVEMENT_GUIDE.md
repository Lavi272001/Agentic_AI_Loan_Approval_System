# MCP Servers Score Improvement Guide

**Current Status:** 8/10 (Good) → Target: 9-10/10 (Excellent)

---

## 📊 Current MCP Servers Assessment

### What's Already Implemented ✅
- ✅ 4 MCP Servers (ApplicantDB, RiskRulesDB, DecisionSynthesis, NotificationSystem)
- ✅ 16+ Concrete Tools with actual implementations
- ✅ Database connectivity for data persistence
- ✅ Error handling per tool
- ✅ Structured response formats
- ✅ Type hints on all functions

### Gaps Preventing 9-10 Score ⚠️
1. **Limited Tool Complexity** - Tools are basic; no advanced features
2. **No Tool Chaining** - Tools don't compose/call each other
3. **No Advanced Error Handling** - Missing retry logic, circuit breakers
4. **No Tool Versioning** - No API versioning support
5. **No Tool Discovery** - No service manifest or registry
6. **No Performance Metrics** - No tool execution tracking
7. **Minimal Testing** - No comprehensive tool tests
8. **No Streaming** - All responses are blocking

---

## 🚀 Roadmap to 9-10/10 Score

### Phase 1: Enhanced Tool Features (90 min)
**Target: 8.5/10 → 9/10**

#### 1.1 Add Advanced Error Handling
```python
# Add retry logic to tools
@mcp.tool()
def get_applicant_profile(applicant_id: str, retries: int = 3) -> Dict[str, Any]:
    """Fetches applicant with automatic retry on database failures."""
    for attempt in range(retries):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM applicants WHERE applicant_id = %s", (applicant_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if result:
                return {"success": True, "data": result}
            return {"success": False, "error": "Not found"}
        except Exception as e:
            if attempt == retries - 1:
                return {"success": False, "error": str(e), "retries_exhausted": True}
            time.sleep(2 ** attempt)  # Exponential backoff
```

**Score Impact:** +0.3 → 8.3/10

#### 1.2 Add Input Validation
```python
from pydantic import BaseModel, validator

class ApplicantProfileRequest(BaseModel):
    applicant_id: str
    
    @validator('applicant_id')
    def validate_applicant_id(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Applicant ID must be at least 3 characters')
        return v

@mcp.tool()
def get_applicant_profile(applicant_id: str) -> Dict[str, Any]:
    """Validates and fetches applicant profile."""
    try:
        request = ApplicantProfileRequest(applicant_id=applicant_id)
        # ... rest of logic
    except ValueError as e:
        return {"success": False, "error": str(e), "validation_failed": True}
```

**Score Impact:** +0.2 → 8.5/10

#### 1.3 Add Tool Metadata & Versioning
```python
TOOL_METADATA = {
    "version": "1.0.0",
    "namespace": "ApplicantDB",
    "tools": {
        "get_applicant_profile": {
            "version": "1.0",
            "stability": "stable",
            "deprecation": None,
            "tags": ["profile", "applicant", "core"]
        },
        "query_applicant_history": {
            "version": "1.0",
            "stability": "stable",
            "deprecation": None,
            "tags": ["history", "applicant", "audit"]
        }
    }
}

@mcp.tool()
def get_tool_metadata() -> Dict[str, Any]:
    """Returns tool metadata and versioning information."""
    return TOOL_METADATA
```

**Score Impact:** +0.2 → 8.7/10

---

### Phase 2: Tool Composition & Chaining (120 min)
**Target: 8.7/10 → 9.2/10**

#### 2.1 Add Tool Composition
```python
# In DecisionSynthesis server
@mcp.tool()
def synthesize_decision_with_history(
    applicant_id: str,
    current_profile: Dict[str, Any],
    financials: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Synthesizes decision with historical context.
    Chains with ApplicantDB to get history.
    """
    try:
        # Get historical data
        history_result = query_applicant_history(applicant_id)
        
        if not history_result.get("success"):
            return {"success": False, "error": "Cannot fetch history"}
        
        historical_decisions = history_result.get("applications", [])
        
        # Analyze patterns
        rejection_pattern = sum(1 for app in historical_decisions 
                               if app.get("credit_score", 0) < 650)
        
        # Synthesize with history awareness
        decision = synthesize_decision(current_profile, {}, financials)
        decision["historical_context"] = {
            "previous_applications": len(historical_decisions),
            "rejection_pattern": rejection_pattern,
            "trend": "improving" if historical_decisions and 
                    historical_decisions[0]["credit_score"] > current_profile["credit_score"]
                    else "declining"
        }
        
        return decision
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Score Impact:** +0.3 → 9/10

#### 2.2 Add Tool Pipeline Execution
```python
# New tool that executes a pipeline of tools
@mcp.tool()
def execute_full_evaluation_pipeline(applicant_id: str) -> Dict[str, Any]:
    """
    Executes complete evaluation pipeline:
    1. Get applicant profile
    2. Evaluate risk rules
    3. Synthesize decision
    4. Log decision
    """
    try:
        # Step 1: Get profile
        profile_result = get_applicant_profile(applicant_id)
        if not profile_result.get("success"):
            return {"success": False, "error": "Profile fetch failed", "step": 1}
        
        profile = profile_result["data"]
        
        # Step 2: Evaluate risks
        risk_result = evaluate_risk_rules(profile, {"dti": profile.get("existing_liabilities", 0) / profile.get("income", 1)})
        if not risk_result.get("success"):
            return {"success": False, "error": "Risk evaluation failed", "step": 2}
        
        # Step 3: Synthesize decision
        decision_result = synthesize_decision(profile, risk_result, {})
        if not decision_result.get("success"):
            return {"success": False, "error": "Decision synthesis failed", "step": 3}
        
        # Step 4: Log decision
        log_result = log_decision(
            f"CASE-{applicant_id}",
            decision_result,
            applicant_id
        )
        
        return {
            "success": True,
            "pipeline": "complete",
            "profile": profile_result,
            "risk_assessment": risk_result,
            "decision": decision_result,
            "audit_log": log_result
        }
    except Exception as e:
        return {"success": False, "error": str(e), "pipeline": "failed"}
```

**Score Impact:** +0.2 → 9.2/10

---

### Phase 3: Performance Tracking & Monitoring (90 min)
**Target: 9.2/10 → 9.5/10**

#### 3.1 Add Tool Metrics
```python
import time
from functools import wraps

TOOL_METRICS = {
    "execution_times": {},
    "error_counts": {},
    "success_counts": {}
}

def track_tool_performance(tool_name: str):
    """Decorator to track tool performance metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Track success
                if tool_name not in TOOL_METRICS["success_counts"]:
                    TOOL_METRICS["success_counts"][tool_name] = 0
                TOOL_METRICS["success_counts"][tool_name] += 1
                
                # Track timing
                if tool_name not in TOOL_METRICS["execution_times"]:
                    TOOL_METRICS["execution_times"][tool_name] = []
                TOOL_METRICS["execution_times"][tool_name].append(execution_time)
                
                result["_performance"] = {
                    "execution_time_ms": round(execution_time * 1000, 2),
                    "tool_name": tool_name
                }
                
                return result
            except Exception as e:
                # Track error
                if tool_name not in TOOL_METRICS["error_counts"]:
                    TOOL_METRICS["error_counts"][tool_name] = 0
                TOOL_METRICS["error_counts"][tool_name] += 1
                
                raise
        return wrapper
    return decorator

@mcp.tool()
@track_tool_performance("get_applicant_profile")
def get_applicant_profile(applicant_id: str) -> Dict[str, Any]:
    """Fetches applicant profile with performance tracking."""
    # ... existing logic
```

#### 3.2 Add Metrics Reporting Tool
```python
@mcp.tool()
def get_tool_metrics() -> Dict[str, Any]:
    """Returns performance metrics for all tools."""
    metrics_summary = {
        "total_successes": sum(TOOL_METRICS["success_counts"].values()),
        "total_errors": sum(TOOL_METRICS["error_counts"].values()),
        "tools": {}
    }
    
    for tool_name, execution_times in TOOL_METRICS["execution_times"].items():
        metrics_summary["tools"][tool_name] = {
            "execution_count": len(execution_times),
            "avg_time_ms": round(sum(execution_times) / len(execution_times) * 1000, 2),
            "min_time_ms": round(min(execution_times) * 1000, 2),
            "max_time_ms": round(max(execution_times) * 1000, 2),
            "success_count": TOOL_METRICS["success_counts"].get(tool_name, 0),
            "error_count": TOOL_METRICS["error_counts"].get(tool_name, 0)
        }
    
    return metrics_summary
```

**Score Impact:** +0.2 → 9.4/10

---

### Phase 4: Advanced Features (120 min)
**Target: 9.4/10 → 9.8/10**

#### 4.1 Add Caching Layer
```python
from functools import lru_cache
import hashlib

CACHE_TTL = 300  # 5 minutes

@mcp.tool()
def get_applicant_profile_cached(applicant_id: str, use_cache: bool = True) -> Dict[str, Any]:
    """Fetches applicant profile with optional caching."""
    
    if use_cache:
        cache_key = hashlib.md5(applicant_id.encode()).hexdigest()
        if cache_key in PROFILE_CACHE:
            cached_data, timestamp = PROFILE_CACHE[cache_key]
            if time.time() - timestamp < CACHE_TTL:
                return {
                    "success": True,
                    "data": cached_data,
                    "cached": True,
                    "cache_age_ms": round((time.time() - timestamp) * 1000)
                }
    
    # Fetch fresh data
    result = get_applicant_profile(applicant_id)
    
    if result.get("success") and use_cache:
        cache_key = hashlib.md5(applicant_id.encode()).hexdigest()
        PROFILE_CACHE[cache_key] = (result["data"], time.time())
        result["cached"] = False
    
    return result
```

**Score Impact:** +0.2 → 9.6/10

#### 4.2 Add Batch Operations
```python
@mcp.tool()
def get_applicant_profiles_batch(applicant_ids: List[str]) -> Dict[str, Any]:
    """Fetches multiple applicant profiles in batch."""
    try:
        results = []
        errors = []
        
        for applicant_id in applicant_ids:
            try:
                result = get_applicant_profile_cached(applicant_id)
                results.append({
                    "applicant_id": applicant_id,
                    "status": "success",
                    "data": result.get("data")
                })
            except Exception as e:
                errors.append({
                    "applicant_id": applicant_id,
                    "error": str(e)
                })
        
        return {
            "success": len(errors) == 0,
            "total": len(applicant_ids),
            "successful": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
```

**Score Impact:** +0.2 → 9.8/10

---

### Phase 5: Testing & Documentation (90 min)
**Target: 9.8/10 → 10/10**

#### 5.1 Add Comprehensive Tool Tests
```python
# File: mcp_servers/test_tools.py

import unittest
from mcp_servers.applicant_db import (
    get_applicant_profile,
    query_applicant_history,
    validate_applicant_id
)

class TestApplicantDBTools(unittest.TestCase):
    
    def test_get_applicant_profile_success(self):
        """Test successful profile retrieval"""
        result = get_applicant_profile("APP-1001")
        self.assertTrue(result["success"])
        self.assertIn("data", result)
        self.assertEqual(result["data"]["applicant_id"], "APP-1001")
    
    def test_get_applicant_profile_not_found(self):
        """Test profile retrieval for non-existent applicant"""
        result = get_applicant_profile("APP-INVALID")
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_validate_applicant_id_valid(self):
        """Test validation of valid applicant ID"""
        result = validate_applicant_id("APP-1001")
        self.assertTrue(result["success"])
        self.assertTrue(result["exists"])
    
    def test_validate_applicant_id_invalid(self):
        """Test validation of invalid applicant ID"""
        result = validate_applicant_id("")
        self.assertFalse(result["success"])
    
    def test_get_applicant_history(self):
        """Test historical application retrieval"""
        result = query_applicant_history("APP-1001")
        self.assertTrue(result["success"])
        self.assertGreater(result["application_count"], 0)

class TestRiskRulesDBTools(unittest.TestCase):
    
    def test_evaluate_risk_rules_approved(self):
        """Test risk evaluation for approved applicant"""
        profile = {"credit_score": 750, "income": 100000}
        financials = {"debt_to_income_ratio": 0.30}
        result = evaluate_risk_rules(profile, financials)
        self.assertTrue(result["success"])
        self.assertGreater(result["risk_score"], 70)
    
    def test_evaluate_risk_rules_rejected(self):
        """Test risk evaluation for rejected applicant"""
        profile = {"credit_score": 500, "income": 0}
        financials = {"debt_to_income_ratio": 1.0}
        result = evaluate_risk_rules(profile, financials)
        self.assertTrue(result["success"])
        self.assertLess(result["risk_score"], 50)

if __name__ == '__main__':
    unittest.main()
```

#### 5.2 Add OpenAPI/Swagger Documentation
```python
# Add to each MCP server

TOOL_DOCUMENTATION = {
    "ApplicantDB": {
        "description": "Manages applicant profile data",
        "version": "1.0.0",
        "tools": {
            "get_applicant_profile": {
                "description": "Fetches applicant profile by ID",
                "parameters": {
                    "applicant_id": {
                        "type": "string",
                        "description": "Unique applicant identifier",
                        "example": "APP-1001"
                    }
                },
                "returns": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "data": {"type": "object"},
                        "error": {"type": "string"}
                    }
                }
            }
        }
    }
}

@mcp.tool()
def get_mcp_documentation() -> Dict[str, Any]:
    """Returns comprehensive OpenAPI-style documentation for all tools."""
    return TOOL_DOCUMENTATION
```

**Score Impact:** +0.2 → 10/10

---

## 📈 Implementation Timeline

| Phase | Focus | Time | Score Impact | Total |
|-------|-------|------|--------------|-------|
| **Phase 1** | Error handling, validation, metadata | 90 min | +0.7 | 8.7/10 |
| **Phase 2** | Tool composition, chaining, pipelines | 120 min | +0.5 | 9.2/10 |
| **Phase 3** | Performance tracking, metrics | 90 min | +0.3 | 9.5/10 |
| **Phase 4** | Advanced features (caching, batch) | 120 min | +0.3 | 9.8/10 |
| **Phase 5** | Testing, documentation | 90 min | +0.2 | 10/10 |
| **TOTAL** | **Complete MCP System** | **510 min (8.5h)** | **+2.0** | **10/10** |

---

## 🎯 Quick Wins (30 min each)

If you don't have 8+ hours, here are quick wins:

### Quick Win #1: Add Retry Logic (30 min)
- Wrap DB calls with exponential backoff
- Score Impact: +0.2 → 8.2/10

### Quick Win #2: Add Input Validation (30 min)
- Use Pydantic models for all tool inputs
- Score Impact: +0.2 → 8.4/10

### Quick Win #3: Add Tool Metadata (30 min)
- Create tool registry with versions
- Score Impact: +0.2 → 8.6/10

### Quick Win #4: Add Performance Tracking (30 min)
- Decorator to track execution times
- Score Impact: +0.2 → 8.8/10

**Total Time: 2 hours → Score: 8/10 → 8.8/10**

---

## ✅ Checklist to 10/10

- [ ] Add retry logic to all tools
- [ ] Add input validation with Pydantic
- [ ] Add tool metadata and versioning
- [ ] Implement tool composition/chaining
- [ ] Add tool pipeline execution
- [ ] Add performance metrics tracking
- [ ] Add metrics reporting tool
- [ ] Implement caching layer
- [ ] Add batch operations
- [ ] Write unit tests for all tools
- [ ] Add OpenAPI documentation
- [ ] Document tool examples
- [ ] Add error recovery examples
- [ ] Document best practices

---

## 📊 Score Progression

```
Current:  8/10 (Good)
          ████████░░

After Phase 1: 8.7/10 (Good+)
               ████████░░

After Phase 2: 9.2/10 (Excellent)
               █████████░

After Phase 3: 9.5/10 (Excellent+)
               █████████░

After Phase 4: 9.8/10 (Near Perfect)
               █████████░

After Phase 5: 10/10 (Perfect)
               ██████████
```

---

## 💡 Implementation Tips

1. **Start with Quick Wins** - Get to 8.8/10 in 2 hours
2. **Focus on Tool Composition** - This is the biggest score lever
3. **Test as You Go** - Add tests alongside features
4. **Document Thoroughly** - Examples beat documentation
5. **Measure Performance** - Data drives decisions

---

## 🚀 Next Steps

1. Pick a phase based on your time availability
2. Implement the changes
3. Update orchestrator to use new features
4. Test end-to-end
5. Update evaluation documentation
6. Celebrate! 🎉

**Good luck improving to 10/10!**
