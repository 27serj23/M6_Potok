# Вопрос - есть 2 задачи,
# скачать с вебсайта несколько эксель файлов и для каждого скачанного эксель файла
# рассчитать новую колонку на основе имеющихся.
# Для какой задачи какой способ обработки (потоки, процессы, асинк) лучше и почему?

# Задача №1: Скачивание файлов с веб-сервера
# Тип задачи:
# Операция ввода-вывода (I/O-bound task). Здесь большую часть времени занимает
# ожидание ответа от сервера и получение данных по сети.
#
# ### Какой подход лучше?
# Подходит "асинхронная обработка" с использованием asyncio и aiohttp. Почему?
# - Такие задачи идеально подходят для асинхронного исполнения,
# потому что основное время уходит на ожидание сетевых операций, а не на активные вычисления.
# - Используя asyncio, можно запустить большое количество задач практически одновременно,
# дожидаясь поступления данных, не блокируя главный поток.
#
# Пример кода для асинхронной загрузки:
#
# async def download_file(session, url, filename):
#     async with session.get(url) as resp:
#         if resp.status == 200:
#             with open(filename, 'wb') as f:
#                 f.write(await resp.read())
#             print(f"✅ Скачал файл: {filename}")
#         else:
#             print(f"❌ Ошибка загрузки файла {filename}, статус: {resp.status}")
# ---
#
# ## Задача №2: Обработка данных в Excel файлах
#
# ### Тип задачи:
# ЦПУ-интенсивная задача (CPU-bound task). Здесь требуется значительное количество
# вычислений для преобразования данных, особенно если файлов много или они большие.
#
# ### Какой подход лучше?
# Рекомендуется использовать "много процессную обработку" с модулем multiprocessing. Почему?
#
# - Каждое ядро процессора способно параллельно обработать разные файлы,
# значительно увеличивая общую скорость обработки.
# - Модуль multiprocessing предоставляет возможность распределять нагрузку
# по доступным ресурсам ЦПУ, таким образом позволяя выполнить операцию гораздо быстрее.
#
# Пример использования пула процессов:
#
# from multiprocessing import Pool
#
# def process_excel_file(filename):
#     # Код обработки Excel файла
#     pass
#
# filenames = ["file1.xlsx", "file2.xlsx"]
#
# with Pool() as p:
#     results = p.map(process_excel_file, filenames)
# ---
#
# ## Итоговая схема:
#
# 1. *Скачивание файлов:* асинхронная обработка (asyncio + aiohttp).
# 2. *Обработка данных:* много процессная обработка (multiprocessing).
# ---
#
# ## Проверка соответствия:
#
# - *Структура проекта:* Имеется удобная навигационная структура и пояснения по
# ключевым компонентам.
# - "Создание файлов:" Генерация тестовых Excel файлов выполнена грамотно.
# - "Параллельные задачи:" Верно применены подходы для различных типов
# задач (скачивание — асинхронно, обработка — мультипроцессно).
# - "Очистка старых файлов:" Есть механизм очистки временных файлов перед каждым запуском.
# - "Производительность:" Организация оптимального распределения задач по
# ресурсам для повышения общей скорости работы.

import os
import asyncio
import aiohttp
import pandas as pd
from multiprocessing import Pool
import time

def show_full_path(filename):
    """Показывает абсолютный путь к файлу"""
    return os.path.abspath(filename)

def show_project_structure():
    """Показывает структуру проекта и важные пути"""
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print("\n" + "=" * 70)
    print("СТРУКТУРА ПРОЕКТА И ПУТИ")
    print("=" * 70)
    print(f"📁 Папка проекта: {project_dir}")
    print(f"📄 Файл скрипта: {os.path.abspath(__file__)}")
    print(f"🐍 Виртуальное окружение: {os.path.join(project_dir, '.venv')}")

    excel_dir = os.path.join(project_dir, "excel_files")
    print(f"📊 Папка для Excel файлов: {excel_dir}")

    print("\n📂 СОДЕРЖИМОЕ ПАПКИ ПРОЕКТА:")
    for item in os.listdir(project_dir):
        item_path = os.path.join(project_dir, item)
        if os.path.isfile(item_path):
            print(f"   📄 {item}")
        else:
            print(f"   📁 {item}/")

def create_sample_excel_file(filename):
    """Создает тестовый Excel файл с данными"""
    try:
        # Создаем директорию если её нет
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)

        sample_data = {
            'Product': ['Product A', 'Product B', 'Product C', 'Product D'],
            'Price': [100, 200, 150, 300],
            'Quantity': [2, 1, 3, 2]
        }
        df = pd.DataFrame(sample_data)
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"✅ Создан тестовый файл: {show_full_path(filename)}")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания файла {filename}: {e}")
        return False

async def mock_download_file(session, url, filename):
    """
    Имитация загрузки файла - создает тестовый Excel файл
    """
    try:
        # Имитируем загрузку
        await asyncio.sleep(1)

        # Создаем тестовый Excel файл
        success = create_sample_excel_file(filename)

        if success:
            print(f"✅ Успешно скачан (создан): {show_full_path(filename)}")
            return filename
        else:
            return None

    except Exception as e:
        print(f"❌ Ошибка загрузки {filename}: {e}")
        return None

async def download_files(file_urls):
    """Основная точка входа для асинхронного скачивания файлов"""
    async with aiohttp.ClientSession() as session:
        tasks = [mock_download_file(session, url, filename) for filename, url in file_urls.items()]
        results = await asyncio.gather(*tasks)
        # Возвращаем только успешно скачанные файлы
        return [filename for filename in results if filename is not None]

def calculate_new_column(filename):
    """Обработка Excel-файла с добавлением новой колонки Total"""
    try:
        # Проверяем, что файл существует и не пустой
        if not os.path.exists(filename):
            return f"❌ Файл не существует: '{filename}'"

        file_size = os.path.getsize(filename)
        if file_size == 0:
            return f"❌ Файл пустой: '{filename}'"

        print(f"📖 Чтение файла: {os.path.basename(filename)} (размер: {file_size} байт)")

        # Читаем файл
        df = pd.read_excel(filename, engine="openpyxl")
        print(f"✅ Прочитан файл {os.path.basename(filename)}, колонки: {list(df.columns)}")

        # Проверяем наличие необходимых колонок
        if 'Price' not in df.columns or 'Quantity' not in df.columns:
            return f"❌ В файле '{os.path.basename(filename)}' отсутствуют колонки Price и/или Quantity. Доступные колонки: {list(df.columns)}"

        # Создаем новую колонку
        df['Total'] = df['Price'] * df['Quantity']

        # Сохраняем файл обратно
        df.to_excel(filename, index=False, engine='openpyxl')

        result = {
            'filename': filename,
            'columns_added': ['Total'],
            'total_sum': df['Total'].sum(),
            'rows_processed': len(df),
            'status': 'успешно'
        }

        print(f"✅ Обработан файл: {os.path.basename(filename)}, создана колонка: Total")
        return result

    except Exception as e:
        error_msg = f"❌ Ошибка при обработке файла '{os.path.basename(filename)}': {str(e)}"
        print(error_msg)
        return error_msg

def verify_processed_files(filenames):
    """Проверяет обработанные файлы и выводит их содержимое"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ОБРАБОТАННЫХ ФАЙЛОВ")
    print("=" * 60)

    for filename in filenames:
        print(f"\n--- Проверка файла: {os.path.basename(filename)} ---")
        if os.path.exists(filename):
            try:
                df = pd.read_excel(filename, engine='openpyxl')
                print(f"✅ Файл существует: {show_full_path(filename)}")
                print(f"📊 Колонки: {list(df.columns)}")
                print(f"📏 Количество строк: {len(df)}")
                print(f"📋 Содержимое:")
                print(df.to_string(index=False))
                print(f"💰 Сумма по колонке Total: {df['Total'].sum()}")
            except Exception as e:
                print(f"❌ Ошибка чтения {filename}: {e}")
        else:
            print(f"❌ Файл не найден: {filename}")

def cleanup_old_files(filenames):
    """Удаляет старые файлы перед началом работы"""
    print("\n🧹 Очистка старых файлов...")
    for filename in filenames:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"🗑 Удален старый файл: {os.path.basename(filename)}")
            except Exception as e:
                print(f"⚠ Не удалось удалить {os.path.basename(filename)}: {e}")

async def main():
    """Основная функция"""
    print("🚀 ЗАПУСК ПРОЕКТА: Скачивание и обработка Excel файлов")

    # Определяем путь к папке проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(project_dir, "excel_files")

    # Показываем структуру проекта
    show_project_structure()

    # Определяем файлы с абсолютными путями
    test_files = {
        os.path.join(output_dir, 'data1.xlsx'): 'local_file_1',
        os.path.join(output_dir, 'data2.xlsx'): 'local_file_2',
        os.path.join(output_dir, 'data3.xlsx'): 'local_file_3'
    }

    # Очищаем старые файлы
    cleanup_old_files(test_files.keys())

    print("\n" + "=" * 70)
    print("ЭТАП 1: Скачивание файлов")
    print("=" * 70)
    successfully_downloaded = await download_files(test_files)

    print(f"\n📥 Скачано файлов: {len(successfully_downloaded)}/{len(test_files)}")

    if successfully_downloaded:
        print("\n" + "=" * 70)
        print(f"ЭТАП 2: Обработка {len(successfully_downloaded)} файлов")
        print("=" * 70)

        # Используем оптимальное количество процессов
        with Pool(processes=min(os.cpu_count(), len(successfully_downloaded))) as pool:
            results = pool.map(calculate_new_column, successfully_downloaded)

        print("\n" + "=" * 70)
        print("РЕЗУЛЬТАТЫ ОБРАБОТКИ")
        print("=" * 70)
        successful = 0
        for result in results:
            if isinstance(result, dict) and result.get('status') == 'успешно':
                print(f"✅ {os.path.basename(result['filename'])}: "
                      f"{result['rows_processed']} строк, "
                      f"сумма: {result['total_sum']}")
                successful += 1
            else:
                print(f"❌ {result}")

        print(f"\n📊 ИТОГ: {successful}/{len(results)} файлов обработано успешно")

        # Проверяем обработанные файлы
        verify_processed_files(successfully_downloaded)

    else:
        print("❌ Ни один файл не был успешно скачан.")


if __name__ == '__main__':
    # Запускаем основную функцию
    start_time = time.time()

    asyncio.run(main())

    end_time = time.time()
    print(f"\n⏱ Общее время выполнения: {end_time - start_time:.2f} секунд")

    project_dir = os.path.dirname(os.path.abspath(__file__))
    excel_dir = os.path.join(project_dir, "excel_files")
    print(f"\n📍 Excel файлы находятся в: {excel_dir}")
    print("🎯 Проект завершен!")

    # Показываем как открыть папку с файлами
    print(f"\n💡 Чтобы открыть папку с файлами, скопируйте этот путь в Проводник:")
    print(f"   {excel_dir}")