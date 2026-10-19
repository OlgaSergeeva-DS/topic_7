"""
Домашнее задание: Реализация Хеш-таблицы (HashTable).
"""


# ========== 3. ХЕШ-ФУНКЦИЯ ДЛЯ СТРОК ==========
def simple_hash(string):
    """
    Принимает строку и возвращает её хеш-значение.
    Алгоритм: сумма ASCII-кодов всех символов.
    """
    total = 0
    for char in string:
        total += ord(char)  # ord() возвращает ASCII-код символа
    return total


# ========== 1. КЛАСС HASHTABLE ==========
class HashTable:
    """
    Реализация хеш-таблицы методом цепочек (chaining).
    """

    def __init__(self, size=5):
        self.size = size
        # Создаем список списков (корзин).
        # Каждая корзина — это список для разрешения коллизий.
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        """Внутренняя хеш-функция. Превращает ключ в индекс корзины."""
        # Используем нашу функцию simple_hash и берем остаток от деления на размер
        return simple_hash(key) % self.size

    def insert(self, key, value):
        """Вставляет элемент (или обновляет, если ключ уже есть)."""
        index = self._hash(key)
        bucket = self.table[index]

        # Ищем ключ в корзине
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Обновляем значение
                return

        # Если ключа нет, добавляем новую пару
        bucket.append((key, value))

    def search(self, key):
        """Ищет значение по ключу. Возвращает None, если не найдено."""
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Удаляет элемент по ключу. Возвращает True, если удалено."""
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False

    # ========== 2. МЕТОД RESIZE ==========
    def resize(self):
        """Увеличивает размер таблицы вдвое и перераспределяет элементы."""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]

        # Перехешируем все старые элементы в новую таблицу
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)


# ========== 4. СЛОВАРЬ НА ОСНОВЕ ХЕШ-ФУНКЦИИ ==========
class SimpleDict:
    """Простой словарь, использующий нашу функцию simple_hash."""

    def __init__(self):
        # Используем стандартный словарь Python для хранения пар,
        # но ключом выступает хеш-значение строки (по заданию).
        self._data = {}

    def add(self, key_string):
        """Добавляет строку, вычисляя её хеш."""
        hash_val = simple_hash(key_string)
        self._data[hash_val] = key_string

    def find_by_key(self, key_string):
        """Ищет значение по ключу (исходной строке)."""
        hash_val = simple_hash(key_string)
        return self._data.get(hash_val, "Не найдено")


# ========== ТЕСТИРОВАНИЕ ==========
if __name__ == "__main__":
    print("=== 1. Тест HashTable ===")
    ht = HashTable(size=5)
    ht.insert("яблоко", 10)
    ht.insert("банан", 20)
    ht.insert("вишня", 30)

    print(f"Поиск 'банан': {ht.search('банан')}")  # 20
    ht.delete("банан")
    print(f"Поиск 'банан' после удаления: {ht.search('банан')}")  # None

    print("\n=== 2. Тест Resize ===")
    ht2 = HashTable(size=5)
    print(f"Размер до: {ht2.size}")

    # Добавляем 10 элементов
    for i in range(10):
        ht2.insert(f"ключ_{i}", i)

    ht2.resize()
    print(f"Размер после resize: {ht2.size}")
    print(f"Проверка элемента 'ключ_9': {ht2.search('ключ_9')}")

    print("\n=== 3. Тест функции simple_hash ===")
    print(f"Хеш строки 'abc': {simple_hash('abc')}")

    print("\n=== 4. Тест SimpleDict ===")
    sd = SimpleDict()
    sd.add("Москва")
    sd.add("Питер")
    print(f"Поиск 'Москва': {sd.find_by_key('Москва')}")
    print(f"Поиск 'Казань': {sd.find_by_key('Казань')}")