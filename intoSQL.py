import pandas as pd
import sqlite3
import winsound

date = '2023-05-24' # дата в имени файлов  --- ввести вручную!!!!

# Создаем соединение с базой данных SQLite
conn = sqlite3.connect('C:/SQLite/firstDB/stsDB.db')

fileG = (f'C:/wHesron/sts/2G/2G_countersCS({date}.xlsx')
fileU1 = (f'C:/wHesron/sts/3G/3G_counters1({date}.xlsx')
fileU2 = (f'C:/wHesron/sts/3G/3G_counters2({date}.xlsx')
fileU3 = (f'C:/wHesron/sts/3G/3G_NodeB_thr_all({date}.xlsx') # добавил _all
fileL = (f'C:/wHesron/sts/4G/4G_counters_all({date}.xlsx') # добавил _all

dfG = pd.read_excel(fileG, header=7)
dfU1 = pd.read_excel(fileU1, header=7, na_values='NIL')
dfU2 = pd.read_excel(fileU2, header=7, na_values='NIL')
dfU3 = pd.read_excel(fileU3, header=7, na_values='NIL')
dfL = pd.read_excel(fileL, header=7, na_values='NIL')
print('эксели считаны')


# Записываем данные в базу данных SQLite с помощью библиотеки SQLite3
dfG.to_sql('GSMsts', conn, if_exists='append', index=False)
dfU1.to_sql('UMTS_1v2', conn, if_exists='append', index=False)
dfU2.to_sql('UMTS_2_v2', conn, if_exists='append', index=False)
dfU3.to_sql('NodeBsts', conn, if_exists='append', index=False)
dfL.to_sql('LTEsts', conn, if_exists='append', index=False)
print('в БД записано')
# Закрываем соединение с базой данных SQLite
conn.close()


winsound.Beep(2500, 1000)
winsound.Beep(2700, 1000)
print('готово')