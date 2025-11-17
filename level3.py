# Уровень 3.
# Напишите функцию, get_html(link), которая принимает один аргумент - название веб страницы.
# Функция должна получать текст веб страницы с помощью библиотеки requests.
#
# def get_html(link):
#
#   pass
#
# Запустите 5 потоков с данной функцией и разными именами в качестве аргументов.
# Сравните время работы параллельного и последовательного запуска с помощью библиотеки time.
# Это задание на самостоятельность, где понадобится установка request.
"""
Реализация функции для загрузки HTML-контента веб-страниц с использованием библиотеки requests.
Оценивается разница во времени выполнения последовательных и параллельных запросов.
"""
import requests  # Библиотека для отправки HTTP-запросов
import time  # Модуль для измерения времени выполнения
import threading  # Модуль для работы с потоками

def get_html(link):
    """
    Функция для загрузки HTML-контента страницы по-указанному URL.
    Args:
        link (str): URL страницы, которую необходимо загрузить.
    Returns:
        str: HTML-код страницы или сообщение об ошибке.
    """
    try:
        # Отправляем GET-запрос с таймаутом 5 секунд
        response = requests.get(link, timeout=5)
        # Возвращаем HTML-код страницы
        return response.text
    except requests.RequestException as e:
        # Если возникла ошибка, возвращаем соответствующее сообщение
        return f"Ошибка при загрузке {link}: {e}"

def run_sequential(links):
    """
    Функция для последовательной загрузки страниц.
    Args:
        links (list of str): Список URL, которые нужно загрузить.
    Returns:
        list of str: Список HTML-кодов страниц или сообщений об ошибках.
    """
    results = []
    for link in links:
        # Последовательно обрабатываем каждый URL
        result = get_html(link)
        results.append(result)
    return results

def run_parallel(links):
    """
    Функция для параллельной загрузки страниц с использованием потоков.
    Args:
        links (list of str): Список URL, которые нужно загрузить.
    Returns:
        list of str: Список HTML-кодов страниц или сообщений об ошибках.
    """
    threads = []
    results = []

    def worker(link):
        # Рабочая функция, сохраняющая результат в глобальном списке
        results.append(get_html(link))

    # Создание и запуск потоков
    for link in links:
        thread = threading.Thread(target=worker, args=(link,))
        threads.append(thread)
        thread.start()

    # Ожидание завершения всех потоков
    for t in threads:
        t.join()

    return results

if __name__ == "__main__":
    # Тестовые ссылки для проверки функционала
    test_links = [
        "https://www.python.org",
        "https://docs.python.org/3/",
        "https://github.com/python/cpython",
        "https://google.com",
        "https://en.wikipedia.org/wiki/Python_(programming_language)"
    ]

    # Последовательная загрузка
    print("Запуск последовательной загрузки...")
    start_time_seq = time.time()
    sequential_results = run_sequential(test_links)
    seq_duration = time.time() - start_time_seq
    print(f"Время последовательной загрузки: {seq_duration:.2f} сек.")

    # Параллельная загрузка
    print("\nЗапуск параллельной загрузки...")
    start_time_par = time.time()
    parallel_results = run_parallel(test_links)
    par_duration = time.time() - start_time_par
    print(f"Время параллельной загрузки: {par_duration:.2f} сек.")

    # Оцениваем прирост производительности
    if par_duration > 0:
        speedup = seq_duration / par_duration
        improvement_percentage = ((seq_duration - par_duration) / seq_duration) * 100
        print(f"\nУскорение: {speedup:.2f}x")
        print(f"Параллельная версия быстрее на {improvement_percentage:.1f}%")
    else:
        print("\nВремя параллельной загрузки слишком мало для вычисления ускорения")

    # Контроль количества полученных ответов
    print(f"\nПолучено страниц последовательно: {len(sequential_results)}")
    print(f"Получено страниц параллельно: {len(parallel_results)}")