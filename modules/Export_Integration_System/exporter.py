import json
import csv
import io

SUPPORTED_FORMATS = ["json", "csv"]


def export_data(data: dict, format: str) -> str:
    """
    Exports data to the specified format.

    Args:
        data (dict): The data to export.
        format (str): The format to export to ("json" or "csv").

    Returns:
        str: The exported data as a string.
    """
    if format == "json":
        return json.dumps(data, indent=2)
    elif format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
        return output.getvalue()
    else:
        raise ValueError(f"Unsupported format: {format}")


# ✅ Alias for compatibility with test_runner.py
export = export_data
