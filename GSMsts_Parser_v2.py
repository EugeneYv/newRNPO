import os
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime

# Директория с XML-файлами
directory = 'C:/temp/try/'

# Пространство имен
namespace = {'ns': 'http://latest/nmc-omc/cmNrm.doc#measCollec'}

# Список measInfoId
measInfoId_list = ['1275071435', '1275071427']

1275071435_conversion = {
'1278087421':	'CELL.KPI.SD.SUCC',
'1278087432':	'CELL.KPI.TCH.ASS.SUCC.TRAF',
'1278087436':	'CELL.KPI.TCH.HO.SUCC.TRAF',
'1278087427':	'CELL.KPI.TCH.SUCC.SIG',
'1278087452':	'CELL.KPI.TCH.ASS.SUCC.TRAF.TCHH',
'1278087454':	'CELL.KPI.TCH.HO.SUCC.TRAF.TCHH',
'1278087450':	'CELL.KPI.TCH.SUCC.SIG.TCHH',
'1278087453':	'CELL.KPI.TCH.ASS.SUCC.TRAF.TCHF',
'1278087455':	'CELL.KPI.TCH.HO.SUCC.TRAF.TCHF',
'1278087451':	'CELL.KPI.TCH.SUCC.SIG.TCHF',
'1278087437':	'CELL.KPI.TCH.HO.DROPS.TRAF',
'1278087417':	'CELL.KPI.IMM.ASS.REQ',
'1278087418':	'CELL.KPI.IMM.ASS.CMD',
'1278087419':	'CELL.KPI.SD.REQ',
'1278087420':	'CELL.KPI.SD.CONGEST',
'1278087422':	'CELL.KPI.SD.TRAF.ERL',
'1278087423':	'CELL.KPI.SD.AVAIL.NUM',
'1278087424':	'CELL.KPI.SD.CFG.NUM',
'1278087425':	'CELL.KPI.TCH.REQ.SIG',
'1278087426':	'CELL.KPI.TCH.CONG.SIG',
'1278087428':	'CELL.KPI.TCH.DROPS.SIG',
'1278087429':	'CELL.KPI.TCH.TRAF.ERL.SIG',
'1278087430':	'CELL.KPI.TCH.ASS.REQ.TRAF',
'1278087431':	'CELL.KPI.TCH.ASS.CONG.TRAF',
'1278087433':	'CELL.KPI.TCH.STATIC.DROPS.TRAF',
'1278087434':	'CELL.KPI.TCH.HO.REQ.TRAF',
'1278087435':	'CELL.KPI.TCH.HO.CONGEST.TRAF',
'1278087438':	'CELL.KPI.TCH.TRAF.ERL.TRAF',
'1278087439':	'CELL.KPI.TCH.AVAIL.NUM',
'1278087440':	'CELL.KPI.TCH.CFG.NUM',
'1278087441':	'CELL.KPI.DUBAND.HO.REQ',
'1278087442':	'CELL.KPI.DUBAND.HO.SUCC',
'1278087443':	'CELL.TCH.OVERFLOW.RATE',
'1278087444':	'CELL.TCH.SEIZ.SUCC.RATE',
'1278087445':	'CELL.KPI.TCHH.TRAF.ERL',
'1278087446':	'CELL.TRX.CFG.AVAIL.RATE',
'1278087447':	'CELL.KPI.TCH.SUCC',
'1278087448':	'CELL.KPI.TCH.CONGESTION.RATE',
'1278087449':	'CELL.KPI.DUBAND.HO.FAIL',
}

# Создание словаря для хранения данных по measInfoId
meas_info_dict = {measInfoId: [] for measInfoId in measInfoId_list}

# Перебор файлов в директории
for filename in os.listdir(directory):
    if filename.endswith('.xml'):
        # Полный путь к файлу
        filepath = os.path.join(directory, filename)

        # Парсинг XML-файла
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Получение значения beginTime
        begin_time = root.find('.//ns:measCollec', namespace).get('beginTime')
        begin_time = datetime.fromisoformat(begin_time).strftime('%Y-%m-%d %H:%M:%S')

        # Перебор measInfoId
        for measInfoId in measInfoId_list:
            # Получение элемента measInfo с определенным measInfoId
            measInfo = root.find(".//ns:measInfo[@measInfoId='{}']".format(measInfoId), namespace)

            # Если measInfo найден, получение значения из элемента measTypes
            if measInfo is not None:
                measTypes = measInfo.find('ns:measTypes', namespace).text.strip().split()

                # Получение всех элементов measValue внутри выбранного measInfo
                for measValue in measInfo.findall('ns:measValue', namespace):
                    # Извлечение значений из элементов measObjLdn и measResults
                    measObjLdn = measValue.get('measObjLdn')
                    measResults = measValue.find('ns:measResults', namespace).text

                    # Разделение значения measResults по пробелу и создание списка значений
                    measResults_list = measResults.split()

                    # Создание словаря для хранения данных текущей записи
                    record = {'begin_time': begin_time, 'measObjLdn': measObjLdn}

                    # Добавление значений из measResults_list в словарь с использованием значений из measTypes в качестве ключей
                    for i, value in enumerate(measResults_list):
                        if i < len(measTypes):
                            record[measTypes[i]] = value

                    # Добавление словаря в список данных для текущего measInfoId
                    meas_info_dict[measInfoId].append(record)

# Создание DataFrame для каждого measInfoId
df_dict = {measInfoId: pd.DataFrame(data) for measInfoId, data in meas_info_dict.items()}

# Сохранение в Excel
with pd.ExcelWriter(os.path.join(directory, 'output.xlsx'), engine='openpyxl') as writer:
    for measInfoId, df in df_dict.items():
        df.to_excel(writer, sheet_name=measInfoId)
