# Хэш-значения:
# 1115dd800feaacefdf481f1f9070374a2a81e27880f187396db67958b207cbad - zyzzx
# 3a7bd3e2360a3d29eea436fcfb7e44c735d117c42d1c1835420b6b9942dd4f1b - apple
# 74e1bb62f8dabb8125a58852b63bdf6eaef667cb56ac7f7cdba6d7305c50a22f - mmmmm

import hashlib
import threading
import time
import sys

class Bruteforcer:
    def __init__(self, hashes, hasher, threads_count):
        self.results = []
        self.hashes = hashes
        self.hasher = hasher
        self.threads_count = threads_count

    def bruteforce(self):
        print("START")
        words_count = 11881376
        words_per_thread_count = words_count // self.threads_count

        indexes = [i * words_per_thread_count for i in range(self.threads_count)]
        indexes.append(words_count)

        threads = []

        for i in range(self.threads_count):
            start_index = indexes[i] + 1
            end_index = indexes[i + 1]
            thread = threading.Thread(target=self.force, args=(start_index, end_index))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def force(self, start_index, end_index): 
        for i in range(start_index, end_index): # Перебор комбинаций в заданном диапазоне
            current_word = self.get_combination_by_position(i) # Получение текущей комбинации
            current_word_hash = self.hasher.hash(current_word)
            if current_word_hash in self.hashes:
                with results_lock:
                    self.results.append(f"{current_word_hash} = {current_word}")

    def get_combination_by_position(self, position):
        alphabet_size = 26 # Размер алфавита (в данном случае, латинские буквы)
        word = ['a'] * 5  # Инициализация массива для хранения комбинации

        position -= 1

        for i in range(4, -1, -1):
            remainder = position % alphabet_size
            word[i] = chr(ord('a') + remainder)
            position //= alphabet_size

        return ''.join(word)

class Sha256Hasher:
    def hash(self, text):
        sha256 = hashlib.sha256()
        sha256.update(text.encode('ascii'))
        return sha256.hexdigest()

if __name__ == '__main__':
    while True:
        results_lock = threading.Lock()
        target_hashes = input("Введите хэш-значение: ").split(',') 
        threads_count = int(input("Введите количество потоков: ")) 

        hasher = Sha256Hasher()
        bruteforcer = Bruteforcer(target_hashes, hasher, threads_count)
        
        start_time = time.time() #время начала брутфорса
        bruteforcer.bruteforce()
        end_time = time.time() #время окончания брутфорса

        for result in bruteforcer.results:
            print(result)
        
        elapsed_time = end_time - start_time
        print(f"Затраченное время на подбор: {elapsed_time:.2f} секунд")
        
        choice = input("Хотите продолжить? (да/нет): ")
        if choice.lower() != 'да':
            sys.exit(0)