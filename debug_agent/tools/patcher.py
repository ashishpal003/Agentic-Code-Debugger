from typing import Dict

def apply_patch(file_path: str, new_code: str) -> Dict:
    """
    Replace entire file content with updated code.

    Args:
        file_path (str): Target file path
        new_code (str): Updated file content

    Returns:
        Dict: Patch result
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
            "file": file_path,
            "error": str(e)
        }