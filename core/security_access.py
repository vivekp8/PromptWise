def get_user_role(user_id):
    """
    Simulates fetching a user's role from a database.
    """
    role_map = {
        1: "admin",
        2: "editor",
        3: "viewer"
    }
    return role_map.get(user_id, "guest")