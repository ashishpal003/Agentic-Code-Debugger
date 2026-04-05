def build_prompt(context, previous_attempts, error):

    return f"""
You are an expert Python debugging agent using ReAct reasoning.

THINK step-by-step:
1. Identify root cause
2. Identify correct file
3. Suggest minimal fix

---

ERROR:
{error}

SNIPPETS:
{context["snippets"]}

PREVIOUS ATTEMPTS:
{previous_attempts}

---

Return JSON:
{{
  "reason": "...",
  "file": "...",
  "fixed_code": "..."
}}
"""