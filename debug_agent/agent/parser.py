import json
from debug_agent.agent.schema import FixResponse

def parse_llm_output(response: str):
    try:
        data = json.loads(response)
        return FixResponse(**data)
    except Exception as e:
        return None