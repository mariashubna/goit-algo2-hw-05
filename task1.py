from bloom_filter import BloomFilter


def check_password_uniqueness(bloom, passwords):
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password:
            raise ValueError("Input must be a list of strings")

        if bloom.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom.add(password)

    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
