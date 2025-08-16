def generate_prompt(role):
    if role == "admin":
        return "Access granted. Full privileges enabled."
    elif role == "viewer":
        return "Read-only access."
    else:
        return "No access."