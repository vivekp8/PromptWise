from modules.Chat_Session_Management.session_controller import start_session, end_session

def test_start_session():
    session = start_session("test_user")
    assert session["user_id"] == "test_user"
    assert session["status"] == "active"

def test_end_session_invalid_id():
    response = end_session("fake_session_id")
    assert "error" in response
