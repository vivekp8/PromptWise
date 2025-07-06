from modules.Export_Integration_System.exporter import export

def test_export_json():
    data = { "x": 1, "y": 2 }
    output = export(data, format="json")
    assert output.startswith("{")

def test_export_csv():
    data = { "name": "vivek", "role": "developer" }
    output = export(data, format="csv")
    assert "name,role" in output
