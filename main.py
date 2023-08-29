"""Основной модуль проекта для определения корреляции количества взаимодействия между белками и их стабильностью"""

import Bio  # pip3 install biopython
from Bio.PDB.MMCIF2Dict import MMCIF2Dict

import csv
from csv import DictWriter  # Для записи словаря в .csv файл
import logging  # Для логирования
from pathlib import Path  # Для работы с путями файлов
from sys import getsizeof  # Чтобы посмотреть размер словаря в памяти компьютера
from time import time  # Если хочется посмотреть время выполнения программы
from time import sleep
import winsound


# Импортируем настройки (значения констант) из файла конфигурации программы
from config import DICT_WORK_MODES, PATH_DIR_WITH_CIF_FILES, HEADERS_CSV, HEADERS_IN_RESULT_FILE,\
    FILE_NAME_AFTER_PRIMARY_EXPORT, FILE_NAME_GENES_NAMES, FILE_NAME_RESULT_DATA

logger = logging.getLogger(__name__)


def export_cif_to_csv():
    """Читает из папки файлы .cif и сохраняет данные в файле .csv Название гена, Значение plddt."""
    number_of_cif_file = 1
    pathlist = Path(PATH_DIR_WITH_CIF_FILES).glob('*.cif')
    dict_from_cif = {}
    """ Словарь, содержит только два ключа _ma_target_ref_db_details.gene_name и _ma_qa_metric_global.metric_value"""
    
    for path in pathlist:  # перебираем пути к файлам (объекты path)
        path_in_str = str(path) # преобразуем объект path в строку
        logger.debug(f'Работаем с файлом {path_in_str.split("/")[-1]}')

        # Читаем файл cif
        with open(path_in_str, 'r') as file_cif:
            dict_from_cif.clear()
            dict_from_cif = MMCIF2Dict(file_cif)  # Проанализируем файл mmCIF и получим словарь
            # Оставим в словаре только два нужных ключа со значениями 
            gene_name_value = dict_from_cif['_ma_target_ref_db_details.gene_name'][0]  # [0] элемент. т.к. MMCIF2Dict
            plddt_value = dict_from_cif['_ma_qa_metric_global.metric_value'][0]  #  выше вернул словарь со списками
            # Очищаем словарь и записываем туда только нужные значения (это быстро - примерно 0.000369 сек) 
            dict_from_cif.clear()  
            dict_from_cif[HEADERS_CSV[0]] = gene_name_value  # Ключи берем из списка с заголовками, т.к. они 
            dict_from_cif[HEADERS_CSV[1]] = plddt_value  # должны совпадать при использовании потом метода DictWriter
            logger.debug(f'{dict_from_cif}')
            print(f'Обработано {number_of_cif_file} .cif файлов.')
            file_cif.close()  # Закрываем файл.cif
        
        # Записываем файл csv
        with open(FILE_NAME_AFTER_PRIMARY_EXPORT, 'a', newline='') as file_csv:
            # Передаем объект файл.csv в функцию Dictwriter() в результат получаем объект DictWriter
            dictwriter_object = DictWriter(file_csv, fieldnames=HEADERS_CSV, delimiter=',')
            # Записываем в файл.csv данные из словаря, передавая словарь в функцию writerow()
            dictwriter_object.writerow(dict_from_cif)
            file_csv.close()  # Закрываем файл.csv
        number_of_cif_file += 1


def get_gene_matches():
    """По совпадениям названий генов записывает соответствующее значение plddt в результирующий файл."""

    # Читаем файл .csv в словарь
    dict_gene_plddt = {}
    with open(FILE_NAME_AFTER_PRIMARY_EXPORT, 'r') as file_csv:  # gene_and_plddt
        # Создаем объект DictReader, указываем символ-разделитель ","
        reader = csv.reader(file_csv, delimiter = ",")
        for row in reader:  # Итерируемся по строкам файла
            dict_gene_plddt[row[0]] = row[1]  # Записываем значения в словарь
        print(dict_gene_plddt)
        file_csv.close()  # Закрываем файл.csv
    logger.info(f'Словарь из файла {FILE_NAME_AFTER_PRIMARY_EXPORT} занимает в памяти {round(getsizeof(dict_gene_plddt)/1048.576, 1)} КБ')
    
    # Читаем файл .txt построчно и возвращает результат в виде списка со списками
    list_with_lists_gene1_gene2 = []
    with open(FILE_NAME_GENES_NAMES) as file_txt:
        while line := file_txt.readline():
            cur_line = line.rstrip()
            gene1_gene2 = cur_line.split('\t')[7:9]  # Из большого списка берем только нужные столбцы H, I
            list_with_lists_gene1_gene2.append(gene1_gene2)
        # print(list_with_lists_gene1_gene2)
        file_txt.close()  # Закрываем файл.txt
    logger.info(f'Список из файла {FILE_NAME_GENES_NAMES} занимает в памяти {round(getsizeof(list_with_lists_gene1_gene2)/1048.576, 1)} КБ')

    list_with_lists_g1_g2_g1plddt_g2plddt = []  # Создаем список для хранения результатов
    """Список со списками с результатами сравнения
    [[gene1, gene2, gene1_plddt, gene2_plddt], [gene1, gene2, gene1_plddt, gene2_plddt], ...]""" 
    list_with_lists_g1_g2_g1plddt_g2plddt.append(HEADERS_IN_RESULT_FILE)  # Добавляем строку заголовков

    # Итерируемся по списку с названиями генов, проверяем совпадения
    for gene1_gene2 in list_with_lists_gene1_gene2:
        # print(gene1_gene2)
        g1_g2_g1plddt_g2plddt = ['NA', 'NA', 'NA', 'NA']
        # Если gene_1 есть в словаре {gene : plddt}
        # !!!! Сделать !!!!!!!!!!!!
        if gene1_gene2[0].casefold() in dict_gene_plddt.keys():  # casefold - без учета регистра
            print('!!!!!!!!!!!')
            g1_g2_g1plddt_g2plddt[0] = gene1_gene2[0]  # записываем gene_1
            g1_g2_g1plddt_g2plddt[2] = dict_gene_plddt[gene1_gene2[0].casefold()]  #записываем gene1_plddt
        # Если gene_2 есть в словаре {gene : plddt}
        if gene1_gene2[1].casefold() in dict_gene_plddt.keys():  # casefold - без учета регистра
            print('!!!!!!!!!!!')
            g1_g2_g1plddt_g2plddt[1] = gene1_gene2[1]  # записываем gene_2
            g1_g2_g1plddt_g2plddt[3] = dict_gene_plddt[gene1_gene2[1].casefold()]  #записываем gene2_plddt
        list_with_lists_g1_g2_g1plddt_g2plddt.append(g1_g2_g1plddt_g2plddt)  # Добавляем строку в результирующий список
    # print(list_with_lists_g1_g2_g1plddt_g2plddt)
    logger.info(f'Результирующий список занимает в памяти {round(getsizeof(list_with_lists_g1_g2_g1plddt_g2plddt)/1048.576, 1)} КБ')


    
    #     file_csv.close()  # Закрываем файл.csv


def main():
    """Основная логика программы."""
# try:
    print(f'Выберите режим работы:')
    for key, mode in DICT_WORK_MODES.items():
        print(f'{key} - {mode}')
    selected_work_mode = input(f'Введите цифру: ')
    logger.debug(f'Выбран режим {selected_work_mode} - {DICT_WORK_MODES[selected_work_mode]}')
    if selected_work_mode == '1':
        export_cif_to_csv()
    elif selected_work_mode == '2':
        get_gene_matches()
    elif selected_work_mode == '12':
        export_cif_to_csv()
        get_gene_matches()
    elif selected_work_mode not in DICT_WORK_MODES.keys():
        logger.debug(f'Выбранного режима "{selected_work_mode}" нет в списке {DICT_WORK_MODES}')
        print(f'Ошибка! Выбранного режима "{selected_work_mode}" не существует.'\
            f'Требуется перезагрузить программу.')
# except Exception as exc:
    # logger.critical('КРИТИЧЕСКАЯ ОШИБКА: при выполнении программы. Требуется перезапуск.')


if __name__ == '__main__':
    start_time = time()  # Время старта программы
    # Здесь задана глобальная конфигурация для всех логгеров
    logging.basicConfig(
        handlers=[logging.StreamHandler()],
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Установлены настройки логгера для текущего файла
    # В переменной __name__ хранится имя пакета;
    # Это же имя будет присвоено логгеру.
    # Это имя будет передаваться в логи, в аргумент %(name)
    logger = logging.getLogger(__name__)
    main()

    print('\n\n')
    print('Время работы программы составило: ')
    print("--- %s seconds ---" % round((time() - start_time), 0))
    print('[!] Программа выполнена.')
    winsound.PlaySound('*', winsound.SND_ALIAS)