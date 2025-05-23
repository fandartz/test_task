import pytest
import os
from utils import find_csv_files, convert_file_data, generate_report

@pytest.fixture
def sample_csv_directory(tmp_path):
    # Создаем временную директорию с тестовыми файлами
    d = tmp_path / "test_data"
    d.mkdir()
    (d / "test1.csv").write_text("")
    (d / "test2.csv").write_text("")
    (d / "test.txt").write_text("")
    return d

def test_find_csv_files(sample_csv_directory):
    files = find_csv_files(sample_csv_directory)
    assert len(files) == 2
    assert all(f.endswith('.csv') for f in files)

def test_convert_file_data():
    test_data = [
        "name,email,department,hours_worked,hourly_rate,position\n"
        "Иван Иванов,ivan@company.com,IT,40,100,Developer\n"
        "Петр Петров,petr@company.com,HR,35,90,Manager"
    ]
    
    result = convert_file_data(test_data)
    assert len(result) == 2
    assert result[0]['name'] == 'Иван Иванов'
    assert result[0]['department'] == 'IT'
    assert result[1]['email'] == 'petr@company.com'
    assert result[1]['hours_worked'] == '35'

def test_convert_file_data_empty():
    result = convert_file_data([""])
    assert len(result) == 0

def test_convert_file_data_invalid_format():
    test_data = ["name,email\nИван,ivan@company.com,IT"]  # Неправильное количество колонок
    result = convert_file_data(test_data)
    assert len(result) == 0

def test_generate_report():
    test_data = [
        {
            'name': 'Иван Иванов',
            'email': 'ivan@company.com',
            'department': 'IT',
            'hours_worked': '40',
            'hourly_rate': '100',
            'position': 'Developer'
        }
    ]
    
    report = generate_report(test_data)
    assert 'IT' in report
    assert 'иван' in report.lower()
    assert 'ivan@company.com' in report.lower()
    assert '$4000' in report  # 40 часов * 100 ставка

def test_generate_report_multiple_departments():
    test_data = [
        {
            'name': 'Иван Иванов',
            'email': 'ivan@company.com',
            'department': 'IT',
            'hours_worked': '40',
            'hourly_rate': '100',
            'position': 'Developer'
        },
        {
            'name': 'Петр Петров',
            'email': 'petr@company.com',
            'department': 'HR',
            'hours_worked': '35',
            'hourly_rate': '90',
            'position': 'Manager'
        }
    ]
    
    report = generate_report(test_data)
    assert 'IT' in report
    assert 'HR' in report
    assert '$4000' in report  # Для Ивана
    assert '$3150' in report  # Для Петра 