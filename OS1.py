import win32api
import os
import json
import zipfile
import win32file
import xml.etree.ElementTree as ET
from xml.dom import minidom
import time

class DiskManager:
    DRIVE_TYPES = {
        0: "Unknown",
        1: "No Root Directory",
        2: "Removable Disk",
        3: "Fixed",
        4: "Network Drive",
        5: "Compact Disc",
        6: "RAM Disk",
    }

    def __init__(self):
        self.menu()

    def delete_file_if_exists(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Файл '{file_name}' успешно удален.")
        else:
            print(f"Файл '{file_name}' не найден. Пожалуйста, убедитесь, что файл существует в текущем каталоге.")

    def task1(self):
        drive_list = self.get_drive_list()
        drives_data = {}
        for drive in drive_list:
            drive_info = self.get_drive_info(drive)
            drives_data[drive] = drive_info
        self.display_drive_info(drives_data)

    def get_drive_list(self):
        drive_list = win32api.GetLogicalDriveStrings()
        drive_list = drive_list.split("\x00")[:-1]
        return drive_list

    def get_drive_info(self, drive):
        drive_type = win32file.GetDriveType(drive)
        drive_size = win32file.GetDiskFreeSpace(drive)
        drive_volume = win32file.GetVolumePathName(drive)
        drive_info = {
            'type': self.DRIVE_TYPES.get(drive_type, 'Unknown'),
            'size': round((drive_size[0] * drive_size[1] * drive_size[3]) / (1024 * 1024 * 1024), 1),
            'free_size': round(drive_size[0] * drive_size[1] * drive_size[2] / (1024 * 1024 * 1024), 1),
            'volume_label': drive_volume if drive_volume != drive else "Don't have volume label"
        }
        return drive_info

    def display_drive_info(self, drives_data):
        for disk, info in drives_data.items():
            s = f'''
            Название: {disk}
            Тип: {info['type']}
            Пространство: {info['size']} GiB
            Свободное пространство: {info['free_size']} GiB
            Метка: {info['volume_label']}
            '''
            print(s)

    def task2(self):
        file_name = "task2.txt"
        with open(file_name, "w+") as file:
            text = input("Введите текст: ")
            file.write(text)
        
        with open(file_name, "r") as file:
            file_contents = file.read()
            print("\nТекст из файла:", file_contents)
        
        otvet = input("\nХотите ли удалить файл? 1-Да/2-Нет: ")
        if otvet == "1":
            self.delete_file_if_exists(file_name)
            print("\nПереход в главное меню\n")
        else:
            print("\nПереход в главное меню\n")

    def task3(self):
        data1 = {
            "Фильм: 'Бегущий по лезвию 2049' ": {
                "Режисер": "Дени Вильнёв",
                "Страна, где велась съемка": "Будапешт",
                "Главный герой": "Райан Гослин"
            }
        }

        json_file_name = "task3.json" 

        with open("task3.json", "w+") as write_file:
            json.dump(data1, write_file)
        with open("task3.json", "r") as read_file:
            data1 = json.load(read_file)
            print(data1)

        name = input("Введите имя критика: ")
        ocenka = int(input("Введите оценку фильма: "))
        janr = input("Введите жанр фильма: ")
        data2 = {
            "Критик": {
                "Имя": name,
                "Оценка": ocenka,
                "Жанр": janr
            }
        }

        with open("task3.json", "a+") as write_file:
            json.dump(data2, write_file)
            print("\nЗаписанные данные в JSON файл:")
        with open("task3.json", "r") as read_file:
            zap = json.loads(json.dumps([data1, data2]))
            print(zap)
        otvet = input("Хотите ли удалить JSON файл? 1-Да/2-Нет: ")
        if otvet == "1":
            self.delete_file_if_exists(json_file_name)
            print("\nПереход в главное меню\n")
        else:
            print("\nПереход в главное меню\n")

    def task4(self):
        xml_file_name = "task4.xml"
        root = minidom.Document()

        xml = root.createElement('root')
        root.appendChild(xml)

        product_child = root.createElement('Person')
        product_child.setAttribute('Firstname', input("Введите имя: "))
        product_child.setAttribute('Lastname', input("Введите фамилию: "))
        product_child.setAttribute('Age', input("Введите возраст: "))
        product_child.setAttribute('Gender', input("Введите пол: "))

        xml.appendChild(product_child)

        xml_str = root.toprettyxml(indent="\t")

        with open("task4.xml", "w+", encoding="utf-8") as f:
            f.write(xml_str)
        tree = ET.parse(xml_file_name)
        root = tree.getroot()
        print(root)
        print(root[0].attrib)
        otvet = input("Хотите ли удалить XML файл? 1-Да/2-Нет: ")
        if otvet == "1":
            self.delete_file_if_exists(xml_file_name)
            print("\nПереход в главное меню\n")
        else:
            print("\nПереход в главное меню\n")
    
    def task5(self):
        file_name = input("Введите название файла, которого хотите добавить: ")
        if os.path.exists(file_name):
            arch = zipfile.ZipFile("task5.zip", "a")
            arch.write(file_name)
            os.remove(file_name)
            print()
            arch.printdir()
            arch.close()
            otvet = input("\nРазархиваровать файл? 1-Да/2-Нет: ")
            if otvet == "1":
                arch = zipfile.ZipFile("task5.zip", "a")
                arch.extractall()
                arch.close()
                arch = zipfile.ZipFile("task5.zip", "w")
                arch.close()
                stats = os.stat(file_name)
                print("Имя файла:", file_name)
                print("Размер файла:", stats.st_size)
                file_time = os.path.getctime(file_name)
                print("Дата создания файла:", time.ctime(file_time))
                otvet = input("\nХотите ли удалить Zip архив и файл? 1-Да/2-Нет: ")
                if otvet == "1":
                    self.delete_file_if_exists("task5.zip")
                    self.delete_file_if_exists(file_name)
                    print("\nПереход в главное меню\n")
                else:
                    print("\nПереход в главное меню\n")
            else:
                print("Переход в главное меню")
        else:
            print(f"Файл '{file_name}' не найден. Пожалуйста, убедитесь, что файл существует в текущем каталоге.")

    def menu(self):
        while True:
            print("Введите цифру, чтобы:")
            print("1. Вывести информацию о дисках")
            print("2. Работа с файлами")
            print("3. Работа с форматом JSON")
            print("4. Работа с форматом XML")
            print("5. Создание zip архива")
            print("Другой вариант, для выхода из программы")
            choice = input("Ваш выбор: ")
            if choice == "1":
                self.task1()
            elif choice == "2":
                self.task2()
            elif choice == "3":
                self.task3()
            elif choice == "4":
                self.task4()
            elif choice == "5":
                self.task5()
            else:
                print("Выход из программы")
                break

if __name__ == "__main__":
    DiskManager()