from utils import *
import os

def main():
    os.makedirs("data", exist_ok=True) # Создаём папку для отчётов
    txt_files = find_csv_files("data") # Получаем файлы csv из папки
    if txt_files:
        file_data = []
        for file in txt_files: # Считываем все файлы csv
            with open(f"data/{file}", "r") as csv_file:
                file_data.append(csv_file.read())
        
        data = convert_file_data(file_data) # Конвертируем file_data в удобный формат

        print(generate_report(data)) # Формируем отчёт
    else:
        print("Добавьте отчёты в папку data")


if __name__ == "__main__":
    main()