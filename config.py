"""Файл конфигурации программы.

Константы, значения которых нужно изменять именно здесь. А вот имена менять нежелательно! """

PATH_DIR_WITH_CIF_FILES = 'Mouse/'
"""Путь к папке с исходными файлами .cif"""

FILE_NAME_AFTER_PRIMARY_EXPORT = PATH_DIR_WITH_CIF_FILES.replace('/', '')+'_data.csv'  # Название: исходная папка + _data.csv
"""Имя файла с результатами первичного экспорта."""

HEADERS_CSV = ['gene_name','plddt']
"""Список с заголовками для .csv файла."""

HEADERS_IN_RESULT_FILE = ['gene1', 'gene2', 'gene1_plddt', 'gene2_plddt']
"""Список с заголовками для файла с результатами сравнения."""

FILE_NAME_GENES_NAMES = 'BIOGRID-ORGANISM-Mus_musculus-4.4.224.tab3.txt'
"""Имя исходного .txt файла с названиями Gene и Interactor B"""

FILE_NAME_RESULT_DATA = PATH_DIR_WITH_CIF_FILES.replace('/', '')+'_result.csv'  # Название: исходная папка + _result.csv
"""Имя файла с результатами сравнения генов."""

DICT_WORK_MODES = {
    '1' : f'Экспорт файлов .cif из папки {PATH_DIR_WITH_CIF_FILES} в первичный файл {FILE_NAME_AFTER_PRIMARY_EXPORT}',
    '2' : f'Поиск совпадений генов в файле .txt и запись результатов в файл {FILE_NAME_RESULT_DATA}',
    '12' : f'Выполнить оба режима работы друг за другом.',
}
"""Словарь с описаниями режимов работы программы."""