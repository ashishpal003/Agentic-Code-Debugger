from typing import Dict

def apply_patch(file_path: str, new_code: str) -> Dict:
    """
    Replace file content with new code
    """

    try:
        with open(file_path, "w") as f:
            f.write(new_code)

        return {
            "success": True,
            "file": file_path
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }