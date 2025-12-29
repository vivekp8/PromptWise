from fastapi.responses import FileResponse
import os


def get_favicon_path(base_dir: str, prefers_dark: bool) -> FileResponse:
    filename = "favicon-dark.ico" if prefers_dark else "favicon-light.ico"
    icon_path = os.path.join(base_dir, "PromptWise", "static", filename)

    if not os.path.isfile(icon_path):
        icon_path = os.path.join(base_dir, "PromptWise", "static", "favicon.ico")

    return FileResponse(icon_path)
