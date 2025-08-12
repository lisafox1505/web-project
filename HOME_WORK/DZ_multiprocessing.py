import datetime
import threading
import time

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def find_primes_single_thread(start, end):
    primes_list = []
    for n in range(start, end):
        if is_prime(n):
            primes_list.append(n)
    return primes_list
start_time = time.perf_counter()
print(f"Список простих чисел з одним потоком: {find_primes_single_thread(1, 2000)}")
end_time = time.perf_counter()
print(f"Процесс з одним потоком виконувався {end_time - start_time}")
print(35 * "-")


primes_result = []
lock = threading.Lock()
def find_primes_multi_thread(start, end, num_thread):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Початок роботи потока {num_thread}")
    primes_list = []
    for n in range(start, end):
        if is_prime(n):
            primes_list.append(n)
    with lock:
        primes_result.extend(primes_list)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Кінець роботи потока {num_thread}")

start_time = time.perf_counter()
thread1 = threading.Thread(target=find_primes_multi_thread, args=(1, 1000, 1))
thread2 = threading.Thread(target=find_primes_multi_thread, args=(1001, 2000, 2))
thread1.start()
thread2.start()
thread1.join()
thread2.join()
end_time = time.perf_counter()

print(f"Список простих чисел з двома потоками: {primes_result}")
print(f"Процесс з двома потоками виконувався: {end_time - start_time} сек.")

# Для такої задачі, як пошук простих чисел, багатопоточність не
# прискорює роботу програми. В цьому випадку программа працює
# швидше, коли працює з одним потоком.