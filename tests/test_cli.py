import subprocess


def test_cli_create():
    result = subprocess.run(
        ["python", "cli.py", "--create", "vivek"], capture_output=True, text=True
    )
    assert "✅ Session created: vivek_session" in result.stdout


def test_cli_get():
    subprocess.run(["python", "cli.py", "--create", "vivek"])
    result = subprocess.run(
        ["python", "cli.py", "--get", "vivek_session"], capture_output=True, text=True
    )
    assert "🔍 Session found:" in result.stdout


def test_cli_end():
    subprocess.run(["python", "cli.py", "--create", "vivek"])
    result = subprocess.run(
        ["python", "cli.py", "--end", "vivek_session"], capture_output=True, text=True
    )
    assert "🛑 Session ended:" in result.stdout
