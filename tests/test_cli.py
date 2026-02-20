import subprocess
import sys
import re


def test_cli_create():
    result = subprocess.run(
        [sys.executable, "cli.py", "--create", "vivek"], capture_output=True, text=True
    )
    assert "[OK] Session created:" in result.stdout


def test_cli_get():
    create_result = subprocess.run(
        [sys.executable, "cli.py", "--create", "vivek"], capture_output=True, text=True
    )
    match = re.search(r"\[OK\] Session created: ([\w-]+)", create_result.stdout)
    assert match is not None
    session_id = match.group(1)

    result = subprocess.run(
        [sys.executable, "cli.py", "--get", session_id], capture_output=True, text=True
    )
    assert "[INFO] Session found:" in result.stdout


def test_cli_end():
    create_result = subprocess.run(
        [sys.executable, "cli.py", "--create", "vivek"], capture_output=True, text=True
    )
    match = re.search(r"\[OK\] Session created: ([\w-]+)", create_result.stdout)
    assert match is not None
    session_id = match.group(1)

    result = subprocess.run(
        [sys.executable, "cli.py", "--end", session_id], capture_output=True, text=True
    )
    assert "[STOP] Session ended:" in result.stdout
