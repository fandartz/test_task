import os

def find_csv_files(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".csv"): # Ищем файлы с окончанием .csv
            files.append(file)
 
    return files

def convert_file_data(data):
    # Создаем список для хранения сотрудников
    employees = []
    for cur_data in data:
        # Разбиваем данные на строки
        rows = cur_data.split('\n')

        # Получаем первую строку (названия колонок)
        columns = rows[0].split(',')

        # Обрабатываем каждую строку с данными о сотрудниках (с 1, т.к 0 у нас колонки)
        for row in rows[1:]:
            if not row:
                continue  # Пропускаем пустые строки если есить
            
            # Разбиваем строку на значения
            values = row.split(',')
            
            # Создаем читаемого сотрудника
            employee = {
                columns[0]: values[0],
                columns[1]: values[1],
                columns[2]: values[2],
                columns[3]: values[3],
                columns[4]: values[4],
                columns[5]: values[5]
            }
            
            employees.append(employee) #Добавляем сотрудника
    return employees

def generate_report(data):
    departments = {} # LДобавляем отделы

    for employee in data:
        dept = employee['department'].lower() # Получаем название отдела
        
        # Ищем поле с зарплатой
        rate_key = None
        for key in ['hourly_rate', 'rate', 'salary']: # Добавить поле при необходимости
            if key in employee:
                rate_key = key
                break
        
        if not rate_key:
            continue
            
        # Создаем запись сотрудника и считаем его выплату
        emp_data = {
            'name': employee['name'].split()[0].lower(),
            'email': employee['email'].split()[0].lower(),
            'hours': int(employee['hours_worked']),
            'rate': float(employee[rate_key]),
            'payout': int(employee['hours_worked']) * int(employee[rate_key])
        }
        
        # Добавляем к отделу
        if dept not in departments:
            departments[dept] = []
        
        departments[dept].append(emp_data)

    # Формируем отчет
    report = []
    report.append("---------------| name | email | hours | rate | payout |")
    for dept, employees in departments.items():
        report.append(dept.upper())
        
        for emp in employees:
            report.append(
                f"---------------| {emp['name']} | {emp['email']} | {emp['hours']} | {emp['rate']} | ${emp['payout']} |"
            )
        
        report.append("\n")  # Пустая строка между отделами

    return '\n'.join(report).strip()