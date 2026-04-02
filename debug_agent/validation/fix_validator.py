def validate_fix(old_error: str, run_result: dict) -> str:
    """
    Compare previous error vs new result
    """

    # Success case
    if run_result.get("success"):
        return "success"
    
    new_error = run_result.get("stderr", "") or run_result.get("error", "")

    # Same error
    if new_error == old_error:
        return "no_change"
    
    # Different error (possible improvement)
    if new_error and new_error != old_error:
        return "improved"
    
    return "failed"