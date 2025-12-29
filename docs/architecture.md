# Project Architecture

## Folder Structure

- `modules/`  
  Contains all core logic, organized by domain:
  - `Chat_Session_Management/`
  - `Prompt_Engine/`
  - `Security_Access_Control/`
  - `Integration_System/`

- `tests/`  
  Contains unit tests for each module, named as `test_<module>.py`.

- `htmlcov/`  
  Auto-generated coverage report from `pytest --cov`.

- `run_coverage.py`  
  Script to enforce 100% coverage.

- `README.md`  
  Project overview and usage instructions.

## Design Principles

- Modular and maintainable
- Explicit test coverage
- CI/CD ready
- Public impact via coverage badge and docs