from hyperLogLog import HyperLogLog
import time
import json


# Читання log-файлу
def get_data_from_json(filepath):
    get_data = []
    with open(filepath, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                IP_address = data.get("remote_addr", "")
                if IP_address.count(".") == 3:
                    get_data.append(IP_address)
            except json.JSONDecodeError:
                print("Error")
    return get_data


# Викликаємо метод set для підрахунку унікальних IP-адрес
def count_exact_unique_ips(IPs):
    return len(set(IPs))


# Викликаємо HyperLogLog для наближеного підрахунку унікальних IP-адрес
def count_approx_unique_ips(IPs):
    hll = HyperLogLog(p=14)
    print("p=14, теоретична похибка ±0.8%, приблизне споживання пам'яті ~16 KB")
    for IP in IPs:
        hll.add(IP)
    return hll.count()


# Ф-я вимірювання часу виконання функції
def measure_execution_time(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start


def main():
    log_file = "lms-stage-access.log"

    # Отримуємо дані з файлу
    IPs = get_data_from_json(log_file)

    # Вимірюємо час
    set_result, set_time = measure_execution_time(count_exact_unique_ips, IPs)
    approx_result, approx_time = measure_execution_time(count_approx_unique_ips, IPs)

    print("\nРезультати порівняння:")

    print("---------------------------------------------------------------")
    print(f"{'':<25}{'|':<3}{'Метод set':<15}{'|':<3}{'HyperLogLog':<20}")
    print("---------------------------------------------------------------")
    print(
        f"{'Унікальні елементи':<25}{'|':<3}{set_result:<15}{'|':<3}{round(approx_result, 1):<20}"
    )
    print("---------------------------------------------------------------")
    print(
        f"{'Час виконання (сек.)':<25}{'|':<3}{round(set_time, 3):<15}{'|':<3}{round(approx_time, 3):<20}"
    )
    print("---------------------------------------------------------------")


if __name__ == "__main__":
    main()
