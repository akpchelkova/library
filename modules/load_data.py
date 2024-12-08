import json
import pandas as pd

def load_books(file_path):
    """
    Загружает базу книг из JSON или CSV файла.
    :param file_path: Путь к файлу.
    :return: DataFrame с книгами.
    """
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Неподдерживаемый формат файла. Используйте JSON или CSV.")
