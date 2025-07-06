import json

def export(data: dict, format="json") -> str:
    """
    Converts dict into the given format.
    """
    if format == "json":
        return json.dumps(data, indent=2)
    elif format == "csv":
        keys = list(data.keys())
        values = [str(data[k]) for k in keys]
        return f"{','.join(keys)}\n{','.join(values)}"
    else:
        return "Unsupported format"
