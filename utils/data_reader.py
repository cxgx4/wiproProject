import json
import openpyxl

from config import config


def read_excel_data(file_path=None, sheet_name="TestData"):
    file_path = file_path or config.EXCEL_TESTDATA_FILE
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook[sheet_name] if sheet_name in workbook.sheetnames else workbook.active

    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return []

    headers = [str(h).strip() for h in rows[0]]
    records = []
    for row in rows[1:]:
        if all(cell is None for cell in row):
            continue
        record = {headers[i]: row[i] for i in range(len(headers))}
        records.append(record)
    return records


def read_json_data(file_path=None):
    file_path = file_path or config.JSON_TESTDATA_FILE
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_test_data():
    if config.TESTDATA_SOURCE == "json":
        return read_json_data()
    return read_excel_data()
