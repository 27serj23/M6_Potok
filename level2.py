# Уровень 2.
# Сравните время работы параллельного и последовательного запуска с
# помощью библиотеки time.

"""
Демонстрация разницы во времени выполнения последовательных и параллельных операций.
Используется библиотека threading для создания и управления потоками.
"""

import time
from threading import Thread  # Импортируем класс Thread отдельно

def get_thread(thread_number):
    """
    Функция, вызываемая в каждом потоке. Она ждёт одну секунду,
    а затем выводит номер текущего потока.
    :param thread_number: Номер текущего потока
    """
    time.sleep(1)
    print(f"Поток {thread_number}")

if __name__ == "__main__":
    # === ПОСЛЕДОВАТЕЛЬНЫЙ РАЗБОР ===
    start_time_seq = time.time()  # Фиксируем начальное время
    for i in range(5):
        get_thread(i + 1)  # Выполняем последовательно
    seq_duration = time.time() - start_time_seq  # Получаем длительность

    # === ПАРАЛЛЕЛЬНАЯ ОБРАБОТКА ===

    start_time_par = time.time()  # Начинаем отсчёт времени
    threads = [Thread(target=get_thread, args=(i + 1,)) for i in range(5)]  # Создаем потоки
    for t in threads:
        t.start()  # Старт потоки
    for t in threads:
        t.join()  # Ждём завершения всех потоков
    par_duration = time.time() - start_time_par  # Вычисляем общую продолжительность

    # Вывод результатов
    print(f"Время последовательного выполнения: {seq_duration:.2f} сек.")
    print(f"Время параллельного выполнения: {par_duration:.2f} сек.")


