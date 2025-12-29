# tests/test_exporter.py

import pytest
from modules.Export_Integration_System import exporter


def test_export_json():
    data = {"name": "Vivek", "role": "Engineer"}
    result = exporter.export_data(data, format="json")
    assert '"name": "Vivek"' in result
    assert '"role": "Engineer"' in result


def test_export_csv():
    data = {"name": "Vivek", "role": "Engineer"}
    result = exporter.export_data(data, format="csv")
    assert "name,role" in result
    assert "Vivek,Engineer" in result


def test_export_invalid_format():
    data = {"name": "Vivek"}
    with pytest.raises(ValueError) as excinfo:
        exporter.export_data(data, format="xml")
    assert "Unsupported format" in str(excinfo.value)


def test_supported_formats_constant():
    assert "json" in exporter.SUPPORTED_FORMATS
    assert "csv" in exporter.SUPPORTED_FORMATS
