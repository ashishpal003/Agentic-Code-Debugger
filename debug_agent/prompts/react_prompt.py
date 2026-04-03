def build_prompt(context, previous_attempts, error):

    return f"""
You are an expert Python debugging agent.

GOAL:
Fix the error with MINIMAL change.

RULES:
- Only fix the root cause
- Do NOT modify unrelated code
- Return FULL corrected file
- File must exist in provided context

---

ERROR TRACEBACK:
{error}

---

CODE SNIPPETS (focus here first):
{context["snippets"]}

---

FULL FILES (fallback only):
{context["code"]}

---

PREVIOUS ATTEMPTS:
{previous_attempts}

---

Return ONLY valid JSON:

{{
  "reason": "root cause explanation",
  "file": "filename.py",
  "fixed_code": "full corrected file content"
}}
"""