import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import winsound
import gzip

''' код для вытаскивания из xml статистических файлов информации соответствия counterID-measInfoID (номер счётчика - номер подзадачи). 
в разных версиях софта могут быть разные соответствия и наборы счётчиков, работает для всех трёх технологий
'''

# Директория с XML-файлами
directory = 'C:/temp/try2/'

# Пространство имен
namespace = {'ns': 'http://latest/nmc-omc/cmNrm.doc#measCollec'}

# Создание пустого словаря для данных
big_dict = {'counter': 'measInfoId'}
small_dict = {}

# разархивация файлов *.gz
for filename in os.listdir(directory):
    if filename.endswith('.gz'):
        filepath = os.path.join(directory, filename)
        output_filepath = os.path.join(directory, filename[:-3])  # Удаление расширения .gz

        with gzip.open(filepath, 'rb') as f_in:
            with open(output_filepath, 'wb') as f_out:
                f_out.write(f_in.read())

# Перебор файлов в директории
for filename in os.listdir(directory):
    if filename.endswith('.xml'):
        # Полный путь к файлу
        filepath = os.path.join(directory, filename)

        # Парсинг XML-файла
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Получение всех элементов measInfo (измерительная задача FunctionSubSet Name,
        # содержащая в себе счётчики, например KPI Measurement <per Cell>)
        for measInfo in root.findall('.//ns:measInfo', namespace):
            # Получение значения measInfoId
            measInfoId = measInfo.get('measInfoId')
            measTypes = measInfo.find('ns:measTypes', namespace).text.strip().split()
            for counter in measTypes:
                small_dict = {counter: measInfoId}
                big_dict.update(small_dict)

with open('C:/temp/try2/output.txt', 'w') as file:
    for key, value in big_dict.items():
        file.write(f'{key}: {value}\n')

