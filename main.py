import sys
import sqlite3

from design_files.design import Ui_MainWindow
from classes import MediaController, linear, correct_sp_dur_for_media, Help
from design_files.styles import LIGHT_THEME, DARK_THEME
from PIL.ImageQt import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, \
    QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel, QFileDialog, QHBoxLayout, \
    QMessageBox
from PyQt6.QtCore import Qt
from classes import Note
import csv
from PyQt6.QtGui import QFontDatabase, QIcon


class TactCalculate(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.name_of_tact_lineEdit.setPlaceholderText('Введите имя такта для сохранения в базу данных')
        self.lineEdit_search_in_bd_tact.setPlaceholderText('Поиск такта по имени')
        self.lineEdit_name_tact_in_bd_tact.setPlaceholderText('Введите имя такта для его открытия или удаления')
        self.lineEdit_name_sovokup_in_db.setPlaceholderText('Введите имя совокупности тактов')
        self.lineEdit_search_in_bd_tact_sovokup.setPlaceholderText('Поиск такта по имени')
        self.lineEdit_add_tact_to_sovocup.setPlaceholderText('Введите имя такта для его добавления в совокупность')
        self.lineEdit_del_tact_index.setPlaceholderText('Введите номер такта для удаления его из совокупности')
        self.lineEdit_search_in_db_sov.setPlaceholderText('Поиск совокупности по имени')
        self.lineEdit_name_sov_del_from_db.setPlaceholderText('Введите имя совокупности тактов для удаления из БД')

        self.stok_tact, self.tact_for_durations, self.tact_for_table = (), [], []
        self.sovokup_sp, self.sovokup_sp_vs = [], []

        self.error_msg = QMessageBox()
        self.error_msg.setWindowTitle("Ошибка")
        self.error_msg.setText('Вы превысили вместимость такта')
        self.error_msg.setIcon(QMessageBox.Icon.Critical)
        self.error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.valid_msg = QMessageBox()
        self.valid_msg.setWindowTitle('Информация')
        self.valid_msg.setText('Такт успешно создан')
        self.valid_msg.setIcon(QMessageBox.Icon.Information)
        self.valid_msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.btn_add_tact_to_db.clicked.connect(self.add_tact_to_db_func)
        self.btn_create_stok_tact.clicked.connect(self.create_stok_tact_func)
        self.btn_note_tochka.clicked.connect(self.btn_tochka_func)
        self.btn_note_delete_one_tact.clicked.connect(self.delete_one_tact_func)
        self.btn_clear_all_tact.clicked.connect(self.clear_all_tact_func)
        self.layout_for_created_tact.setContentsMargins(10, 0, 10, 10)
        self.btn_save_tact_as_csv.clicked.connect(self.save_tact_as_csv_func)
        self.open_tact_from_csv.clicked.connect(self.open_tact_from_csv_func)
        self.btn_pokaz_bd_tact.clicked.connect(self.btn_pokaz_bd_tact_func)
        self.lineEdit_search_in_bd_tact.textChanged.connect(self.text_changed_lineEdit_search_in_bd_tact)
        self.btn_open_tact_from_bd.clicked.connect(self.open_tact_from_bd_func)
        self.btn_delete_tact_from_bd.clicked.connect(self.delete_tact_from_bd_func)
        self.table_bd_tact.itemActivated.connect(self.table_bd_tact_activated)
        self.btn_pokas_tact_db_for_sovokup.clicked.connect(self.pokaz_tact_db_for_sovokup_func)
        self.lineEdit_search_in_bd_tact_sovokup.textChanged.connect(
            self.lineEdit_search_in_bd_tact_sovokup_text_changed)
        self.btn_add_tact_to_sovocup.clicked.connect(self.add_tact_to_sovocup_func)
        self.buttonGroup.buttonClicked.connect(self.btn_note_tact_create_clicked)
        self.btn_del_tact_from_sovocup.clicked.connect(self.del_tact_from_sovocup_func)
        self.tablet_tact_db_for_sovokup.itemActivated.connect(self.tablet_tact_db_for_sovokup_ativated)
        self.table_created_sovokup.itemActivated.connect(self.table_created_sovokup_activated)
        self.btn_add_sovokup_to_db.clicked.connect(self.add_sovokup_to_db_func)
        self.btn_clear_all_sov.clicked.connect(self.btn_clear_all_sov_func)
        self.btn_pokas_bd_sovokup.clicked.connect(self.pokas_bd_sovokup_func)
        self.lineEdit_search_in_db_sov.textChanged.connect(self.search_in_db_sov_func)
        self.table_db_sov.itemActivated.connect(self.table_db_sov_activated)
        self.table_db_sov.itemClicked.connect(self.table_db_sov_clicked)
        self.btn_open_sov_from_db.clicked.connect(self.open_sov_from_db_func)
        self.table_bd_tact.itemClicked.connect(self.table_bd_tact_one_clicked)
        self.btn_del_sov_from_db.clicked.connect(self.del_sov_from_db_func)
        self.btn_play_stok_tact.clicked.connect(self.play_stok_tact)
        self.btn_stop_play_stok_tact.clicked.connect(self.stop_play_stok_tact)
        self.btn_play_red_tact.clicked.connect(self.play_red_tact)
        self.btn_stop_play_red_tact.clicked.connect(self.stop_play_red_tact)
        self.btn_play_sovokup.clicked.connect(self.play_sovokup)
        self.btn_stop_play_sovokup.clicked.connect(self.stop_play_sovokup)
        self.help_btn.clicked.connect(self.help)
        self.theme_btn.clicked.connect(self.theme_btn_clicked)
        self.tablet_tact_db_for_sovokup.itemClicked.connect(self.tablet_tact_db_for_sovokup_one_clicked)
        self.table_created_sovokup.itemClicked.connect(self.table_created_sovokup_one_clicked)
        self.label_7.setText('Выберите ноту\nДля добавления в такт')

        self.theme = 'LIGHT_THEME'
        self.setStyleSheet(LIGHT_THEME if self.theme == 'LIGHT_THEME' else DARK_THEME)

        self.media_player_stok_tact = MediaController([0])
        self.media_player_red_tact = MediaController([0])
        self.media_player_red_sov = MediaController([0])

        self.help = Help()

        font_id = QFontDatabase.addApplicationFont("_internal/PT Root UI.ttf")

        self.btn_note_1.setIcon(QIcon(Note(1, self.theme).get_note_link()))
        self.btn_note_2.setIcon(QIcon(Note(2, self.theme).get_note_link()))
        self.btn_note_4.setIcon(QIcon(Note(4, self.theme).get_note_link()))
        self.btn_note_8.setIcon(QIcon(Note(8, self.theme).get_note_link()))
        self.btn_note_16.setIcon(QIcon(Note(16, self.theme).get_note_link()))
        self.btn_note_32.setIcon(QIcon(Note(32, self.theme).get_note_link()))
        self.btn_note_64.setIcon(QIcon(Note(64, self.theme).get_note_link()))
        self.btn_note_tochka.setIcon(QIcon(Note('.', self.theme).get_note_link()))

    # Метод для задания стокового такта
    def create_stok_tact_func(self):
        self.stok_tact = (self.spinBox_chisl.value(), int(self.comboBox_znam.currentText()))

        self.media_player_stok_tact.stop()
        self.media_player_stok_tact.durations = [0.0001] + [Note(self.stok_tact[1], self.theme).get_note_duration()] * \
                                                self.stok_tact[0]

        self.tact_for_durations = []  # Контейнер для редактируемого такта
        self.tact_for_table = []  # Контейнер для отображения такта в таблице такта
        self.tact_duration = Note(self.stok_tact[1], self.theme).get_note_duration() * self.stok_tact[0]

        self.re_table_stok_tact()
        self.label_check_to_create_tact.setText('Такт задан, можете его заполнять')
        self.label_your_tact.setText(f'Ваш такт ({self.stok_tact[0]} / {self.stok_tact[1]}):')

        self.re_label_created_tact()
        self.re_table_podskaz_note()
        self.re_table_podskaz_note_tochka()
        self.name_of_tact_lineEdit.clear()

    # Метод для формирования таблицы стокового такта
    def re_table_stok_tact(self):
        self.table_stok_tact.clear()
        self.table_stok_tact.setRowCount(1)
        self.table_stok_tact.setColumnCount(
            self.stok_tact[0])
        self.table_stok_tact.setHorizontalHeaderLabels(
            [str(i) for i in range(1, len(self.stok_tact) + 1)])

        rows = [self.stok_tact[1] for _ in range(self.stok_tact[0])]

        for c, val in enumerate(rows):
            cell_widget = QWidget()
            layout = QHBoxLayout(cell_widget)
            label = QLabel()
            label.setPixmap(QPixmap(Note(val, self.theme).get_note_link()).scaled(20, 20,
                                                                                  aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                                                                  transformMode=Qt.TransformationMode.SmoothTransformation))
            layout.addWidget(label)

            layout.setContentsMargins(0, 5, 0, 0)
            cell_widget.setFixedSize(
                layout.sizeHint())
            self.table_stok_tact.setCellWidget(0, c, cell_widget)

        header = self.table_stok_tact.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setStretchLastSection(True)

        self.table_stok_tact.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_stok_tact.verticalHeader().setStyleSheet(
            "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
        )

    # Метод, вызывающийся при попытке добавить ноту в такт
    def btn_note_tact_create_clicked(self, btn: QPushButton):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            note = Note(int(btn.objectName().split('_')[-1]), self.theme)
            self.created_tact_duration = sum(
                [Note(i, self.theme).get_note_duration() for i in self.tact_for_durations if i])

            if self.created_tact_duration < self.tact_duration:  # Можем редактировать такт
                if self.created_tact_duration + note.get_note_duration() <= self.tact_duration:  # Есть возможность добавить ноту в такт
                    self.tact_for_durations.append(note.get_note())
                    self.tact_for_table.append(note.get_note())

                    self.media_player_red_tact.stop()
                    self.media_player_red_tact.durations = [0.0001] + correct_sp_dur_for_media(self.tact_for_table,
                                                                                               self.theme)

                    self.re_table_podskaz_note()
                    self.re_table_podskaz_note_tochka()
                    if self.created_tact_duration + note.get_note_duration() == self.tact_duration:
                        self.valid_msg.exec()  # Такт валидно заполнен
                else:
                    self.error_msg.exec()  # Превышена вместимость такта
            elif self.created_tact_duration >= self.tact_duration:
                self.error_msg.exec()  # Такт не валиден, превышена вместимость такта

            self.re_label_created_tact()

    # Метод, вызывающийся при попытке добавить точку к ноте в такте
    def btn_tochka_func(self):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            self.created_tact_duration = sum(
                [Note(i, self.theme).get_note_duration() for i in self.tact_for_durations if i])

            if self.created_tact_duration:  # В такте есть ноты
                if self.created_tact_duration < self.tact_duration:  # Такт не заполнен
                    note_t = Note(self.tact_for_durations[-1] * 2, self.theme)
                    if self.created_tact_duration + note_t.get_note_duration() <= self.tact_duration:  # Можем добавить ноту с точкой
                        if self.tact_for_table[-1] != '.':
                            self.tact_for_durations.append(note_t.get_note())
                            self.tact_for_table.append('.')

                            self.media_player_red_tact.stop()
                            self.media_player_red_tact.durations = [0.0001] + correct_sp_dur_for_media(
                                self.tact_for_table, self.theme)

                            self.re_table_podskaz_note()
                            self.re_table_podskaz_note_tochka()

                            if self.created_tact_duration + note_t.get_note_duration() == self.tact_duration:
                                self.valid_msg.exec()  # Такт валидно заполнен
                        else:
                            self.error_msg.setText('Нельзя записать 2 точки подряд')  # Попытка записать 2 точки подряд
                            self.error_msg.exec()
                            self.error_msg.setText('Вы превысили вместимость такта')
                    else:
                        self.error_msg.exec()  # Превышена вместимость такта
                else:
                    self.error_msg.exec()  # Превышена вместимость такта
            else:
                self.error_msg.setText(
                    'Точка не может быть добавлена в пустой такт')  # Попытка добавить точку в пустой такт
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

            self.re_label_created_tact()
            self.re_table_podskaz_note()

    def delete_one_tact_func(self):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            if self.tact_for_durations:
                del self.tact_for_durations[-1]
                del self.tact_for_table[-1]

                self.media_player_red_tact.stop()
                self.media_player_red_tact.durations = [0.0001] + correct_sp_dur_for_media(self.tact_for_table,
                                                                                           self.theme)

                self.re_table_podskaz_note()
                self.re_table_podskaz_note_tochka()
            self.re_label_created_tact()

    def clear_all_tact_func(self):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            self.tact_for_durations.clear()
            self.tact_for_table.clear()
            self.media_player_red_tact.durations = [0]
            self.re_table_podskaz_note()
            self.re_table_podskaz_note_tochka()
            self.re_label_created_tact()

    # Визуализация редактируемого такта (лайаут с лейблами, в которых лежат изображения)
    def re_label_created_tact(self):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            while self.layout_for_created_tact.count() != 1:
                self.layout_for_created_tact.takeAt(1).widget().deleteLater()

            if self.tact_for_table:
                for i in self.tact_for_table:
                    label = QLabel()
                    label.setStyleSheet("margin-top: 5px; margin-bottom: 5px;")
                    pixmap = QPixmap(Note(i, self.theme).get_note_link_label())
                    label.setPixmap(pixmap.scaled(20, 50, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                                  transformMode=Qt.TransformationMode.SmoothTransformation))
                    self.layout_for_created_tact.addWidget(label)

    # Сохранение такта как csv
    def save_tact_as_csv_func(self):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            created_tact_duration = sum([Note(i, self.theme).get_note_duration() for i in self.tact_for_durations if i])
            if created_tact_duration == self.tact_duration:
                filename, _ = QFileDialog.getSaveFileName(
                    parent=None,
                    caption='Сохранить файл с тактом в csv',
                    directory='',
                    filter='CSV Files (*.csv)'
                )

                if filename:
                    data = [['Имя Такта', 'Числитель Размера Такта', 'Знаменатель Размера Такта', 'Такт (числа)',
                             'Такт (с точками)'],
                            [f'{filename.split('/')[-1].split('.')[0]}', f'{self.stok_tact[0]}', f'{self.stok_tact[1]}',
                             f'{self.tact_for_durations}',
                             f'{self.tact_for_table}']]

                    with open(filename, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file, delimiter=',')
                        for row in data:
                            writer.writerow(row)

    # Открытие такта из csv
    def open_tact_from_csv_func(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Выбрать csv файл с тактом', '',
            'CSV Files (*.csv)')[0]

        if filename:
            with open(filename, mode='r', encoding='utf-8') as file:
                name, c, z, tact_int, tact_table = list(csv.reader(file))[1]
                stok_tact_vs = (int(c), int(z))
                tact_for_durations = [int(i.strip()) for i in tact_int[1:-1].split(',')]
                tact_duration_vs = Note(stok_tact_vs[1], self.theme).get_note_duration() * stok_tact_vs[0]
                created_tact_duration = sum(
                    [Note(i, self.theme).get_note_duration() for i in tact_for_durations if i])

                if created_tact_duration == tact_duration_vs:
                    self.name_of_tact_lineEdit.setText(f'{name}')
                    self.stok_tact = (int(c), int(z))

                    self.media_player_stok_tact.stop()
                    self.media_player_stok_tact.durations = [0.0001] + [
                        Note(self.stok_tact[1], self.theme).get_note_duration()] * self.stok_tact[0]

                    self.tact_for_durations = [int(i.strip()) for i in tact_int[1:-1].split(',')]
                    self.tact_for_table = list(
                        map(lambda x: int(x) if x.isdigit() else '.', [i.strip() for i in tact_table[1:-1].split(',')]))
                    self.tact_duration = Note(self.stok_tact[1], self.theme).get_note_duration() * self.stok_tact[0]

                    self.media_player_red_tact.stop()
                    self.media_player_red_tact.durations = [0.0001] + correct_sp_dur_for_media(self.tact_for_table,
                                                                                               self.theme)

                    self.label_check_to_create_tact.setText('Такт задан, можете его заполнять')
                    self.label_your_tact.setText(f'Ваш такт ({self.stok_tact[0]} / {self.stok_tact[1]}):')

                    self.re_table_stok_tact()
                    self.re_label_created_tact()
                    self.re_table_podskaz_note()
                    self.re_table_podskaz_note_tochka()
                else:
                    self.error_msg.setText('Такт некорректен')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')

    # Визуализация подсказок с целыми нотами в виде таблицы
    def re_table_podskaz_note(self):
        created_tact_duration = sum(
            [Note(i, self.theme).get_note_duration() for i in self.tact_for_durations if i])
        missed_tact_duration = self.tact_duration - created_tact_duration

        rows = []
        for i in [1, 2, 4, 8, 16, 32, 64]:
            rows.append([Note(i, self.theme).get_note_link(),
                         str(int(missed_tact_duration / Note(i, self.theme).get_note_duration()))])

        self.table_podskaz_note.clear()  # Очищаем от того, что было, даже если ничего не было
        self.table_podskaz_note.setRowCount(len(rows))  # Задаём количество строчек
        self.table_podskaz_note.setColumnCount(
            len(rows[0]))  # и столбцов (считаем, что в разных строчках одинаковое количество столбцов)
        self.table_podskaz_note.setHorizontalHeaderLabels(['Вид ноты', 'Кол-во нот, которое можно добавить в такт'])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem()
                if not val.isdigit():
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    label = QLabel()
                    label.setPixmap(QPixmap(val).scaled(20, 20, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                                        transformMode=Qt.TransformationMode.SmoothTransformation))
                    layout.addWidget(label)

                    # Без лишних отступов вокруг содержимого
                    layout.setContentsMargins(0, 5, 0, 0)
                    cell_widget.setFixedSize(
                        layout.sizeHint())  # установим размер виджета равным размерам содержимого
                    self.table_podskaz_note.setCellWidget(r, c, cell_widget)
                else:
                    item.setText(val)
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Выравниваем текст по середине по ширине и высоте
                    self.table_podskaz_note.setItem(r, c, item)  # Ставим ячейку в нужное место

        # Умная ширина колонок
        header = self.table_podskaz_note.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.table_podskaz_note.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_podskaz_note.verticalHeader().setStyleSheet(
            "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
        )

    # Визуализация подсказок с нотами с точкой в виде таблицы
    def re_table_podskaz_note_tochka(self):
        created_tact_duration = sum(
            [Note(i, self.theme).get_note_duration() for i in self.tact_for_durations if i])
        missed_tact_duration = self.tact_duration - created_tact_duration

        rows = []
        for i in [1, 2, 4, 8, 16, 32, 64]:
            rows.append([(Note(i, self.theme).get_note_link(), Note('.', self.theme).get_note_link()),
                         str(int(missed_tact_duration / (Note(i, self.theme).get_note_duration() + Note(i * 2,
                                                                                                        self.theme).get_note_duration())))])

        self.table_podskaz_note_tochka.clear()  # Очищаем от того, что было, даже если ничего не было
        self.table_podskaz_note_tochka.setRowCount(len(rows))  # Задаём количество строчек
        self.table_podskaz_note_tochka.setColumnCount(
            len(rows[0]))  # и столбцов (считаем, что в разных строчках одинаковое количество столбцов)
        self.table_podskaz_note_tochka.setHorizontalHeaderLabels(
            ['Вид ноты', 'Кол-во нот, которое можно добавить в такт'])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem()
                if isinstance(val, tuple):
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    for i in val:
                        label = QLabel()
                        label.setPixmap(QPixmap(i).scaled(20, 20, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                                          transformMode=Qt.TransformationMode.SmoothTransformation))
                        layout.addWidget(label)

                        # Без лишних отступов вокруг содержимого
                        layout.setContentsMargins(0, 5, 0, 0)
                        cell_widget.setFixedSize(
                            layout.sizeHint())  # установим размер виджета равным размерам содержимого
                    self.table_podskaz_note_tochka.setCellWidget(r, c, cell_widget)
                else:
                    item.setText(val)
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Выравниваем текст по середине по ширине и высоте
                    self.table_podskaz_note_tochka.setItem(r, c, item)  # Ставим ячейку в нужное место

        # Умная ширина колонок
        header = self.table_podskaz_note_tochka.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.table_podskaz_note_tochka.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_podskaz_note_tochka.verticalHeader().setStyleSheet(
            "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
        )

    # Добавление такта в БД
    def add_tact_to_db_func(self):
        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            created_tact_duration = sum([Note(i, self.theme).get_note_duration() for i in self.tact_for_durations if i])
            if created_tact_duration == self.tact_duration:
                if self.name_of_tact_lineEdit.text():  # Введено имя такта
                    con = sqlite3.connect('_internal/tact_bd.db')
                    cur = con.cursor()
                    result = cur.execute(f"""SELECT id_name_tact FROM id_tact_table
                                WHERE name_tact = '{self.name_of_tact_lineEdit.text()}'""", ()).fetchall()

                    if not result:  # Такт можно добавить в бд
                        cur.execute(
                            F"""INSERT INTO id_tact_table(name_tact) VALUES('{self.name_of_tact_lineEdit.text()}')""")

                        result = cur.execute(f"""SELECT id_name_tact FROM id_tact_table
                                    WHERE name_tact = '{self.name_of_tact_lineEdit.text()}'""", ()).fetchall()

                        values = [
                            result[0][0],
                            self.stok_tact[0],
                            self.stok_tact[1],
                            ','.join(map(str, self.tact_for_durations)),
                            ','.join(map(str, self.tact_for_table))
                        ]

                        cur.execute("""
                            INSERT INTO tact_table(id_name_tact, chisl, znam, tact_sp_durations, tact_sp_t) 
                            VALUES (?, ?, ?, ?, ?)
                        """, values)

                        con.commit()

                        self.sp_all_bd_tact = cur.execute("""SELECT id_tact_table.name_tact, 
                        tact_table.chisl, 
                        tact_table.znam, 
                        tact_table.tact_sp_t, 
                        tact_table.tact_sp_durations FROM tact_table
                        INNER JOIN id_tact_table ON tact_table.id_name_tact = id_tact_table.id_name_tact""").fetchall()

                        self.valid_msg.setText(
                            f'Такт "{self.name_of_tact_lineEdit.text()}" успешно добавлен в базу данных')
                        self.valid_msg.exec()
                        self.valid_msg.setText('Такт успешно создан')

                    else:  # Такт уже есть в БД
                        values = (
                            self.stok_tact[0],
                            self.stok_tact[1],
                            ','.join(map(str, self.tact_for_durations)),
                            ','.join(map(str, self.tact_for_table)),
                            result[0][0]
                        )

                        cur.execute('''
                            UPDATE tact_table
                            SET chisl = ?,
                                znam = ?,
                                tact_sp_durations = ?,
                                tact_sp_t = ?
                            WHERE id_name_tact = ?
                        ''', values)

                        con.commit()

                        self.sp_all_bd_tact = cur.execute("""SELECT id_tact_table.name_tact, 
                        tact_table.chisl, 
                        tact_table.znam, 
                        tact_table.tact_sp_t, 
                        tact_table.tact_sp_durations FROM tact_table
                        INNER JOIN id_tact_table ON tact_table.id_name_tact = id_tact_table.id_name_tact""").fetchall()

                        self.valid_msg.setText(
                            f'Значения такта "{self.name_of_tact_lineEdit.text()}" в базе данных изменены')
                        self.valid_msg.exec()
                        self.valid_msg.setText('Такт успешно создан')

                    con.close()
                else:  # Не введенно имя такта
                    self.error_msg.setText('Имя такта не введено')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')

    # Показать таблицу с тактами из БД по нажатию кнопки
    def btn_pokaz_bd_tact_func(self):
        self.pokaz_tact_db(self.table_bd_tact, self.label_pokaz_bd_tact)

    # Универсальный метод для обновления таблиц с тактами
    def re_table_tact(self, sp_for_table, table):
        table.clear()  # Очищаем от того, что было, даже если ничего не было
        table.setRowCount(len(sp_for_table))  # Задаём количество строчек
        table.setColumnCount(
            len(sp_for_table[0]))  # и столбцов (считаем, что в разных строчках одинаковое количество столбцов)
        table.setHorizontalHeaderLabels(
            ['Имя такта', 'Числ. дроби размера', 'Знам. дроби размера',
             'Такт'])  # В первой строке файла — вертикальные заголовки

        for r, row in enumerate(sp_for_table):
            for c, val in enumerate(row):
                item = QTableWidgetItem()
                if isinstance(val, list):
                    cell_widget = QWidget()
                    layout = QHBoxLayout(cell_widget)
                    for i in val:
                        label = QLabel()
                        label.setPixmap(QPixmap(Note(i, self.theme).get_note_link()).scaled(20, 20,
                                                                                            aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                                                                                            transformMode=Qt.TransformationMode.SmoothTransformation))
                        layout.addWidget(label)

                        layout.setContentsMargins(0, 5, 0, 0)
                        cell_widget.setFixedSize(
                            layout.sizeHint())
                    table.setCellWidget(r, c, cell_widget)
                else:
                    item.setText(val)
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Выравниваем текст по середине по ширине и высоте
                    table.setItem(r, c, item)  # Ставим ячейку в нужное место

        # Умная ширина колонок
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.verticalHeader().setStyleSheet(
            "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
        )

    # Поиск такта в бд по введённой подстроке на этапе работы с бд тактов
    def text_changed_lineEdit_search_in_bd_tact(self, text):
        self.search_in_bd_tact(text, self.label_pokaz_bd_tact, self.table_bd_tact)

    # Открытие такта для редактирования из БД
    def open_tact_from_bd_func(self):
        if self.label_pokaz_bd_tact.text() == 'База данных с тактами:':
            if self.lineEdit_name_tact_in_bd_tact.text():  # Имя такта введено
                data = [i[0] for i in self.sp_all_bd_tact]

                if self.lineEdit_name_tact_in_bd_tact.text() in data:  # Такт есть в БД
                    name, c, z, sp_t, sp_dur = [i for i in
                                                [[j for j in i if self.lineEdit_name_tact_in_bd_tact.text() in i] for i
                                                 in self.sp_all_bd_tact] if i][0]
                    sp_dur = list(map(int, sp_dur.split(',')))
                    sp_t = list(map(lambda x: int(x) if x.isdigit() else x, sp_t.split(',')))
                    self.name_of_tact_lineEdit.setText(name)

                    self.stok_tact = (c, z)

                    self.media_player_stok_tact.stop()
                    self.media_player_stok_tact.durations = [0.0001] + [
                        Note(self.stok_tact[1], self.theme).get_note_duration()] * self.stok_tact[0]

                    self.tact_for_durations = sp_dur
                    self.tact_for_table = sp_t

                    self.media_player_red_tact.stop()
                    self.media_player_red_tact.durations = [0.0001] + correct_sp_dur_for_media(self.tact_for_table,
                                                                                               self.theme)

                    self.tact_duration = Note(self.stok_tact[1], self.theme).get_note_duration() * self.stok_tact[0]

                    self.label_check_to_create_tact.setText('Такт задан, можете его заполнять')
                    self.label_your_tact.setText(f'Ваш такт ({self.stok_tact[0]} / {self.stok_tact[1]}):')

                    self.re_table_stok_tact()
                    self.re_label_created_tact()
                    self.re_table_podskaz_note()
                    self.re_table_podskaz_note_tochka()

                    self.valid_msg.setText(f'Такт "{name}" открыт для редактирования')
                    self.valid_msg.exec()
                    self.valid_msg.setText('Такт успешно создан')
                else:  # Такта нет в БД
                    self.error_msg.setText('Такта с таким именем нет в базе данных')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')
            else:  # Имя такта не введено
                self.error_msg.setText('Имя такта не введено')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    # Удаление такта из базы данных
    def delete_tact_from_bd_func(self):
        if self.label_pokaz_bd_tact.text() == 'База данных с тактами:':
            if self.lineEdit_name_tact_in_bd_tact.text():  # Имя такта введено
                im = [i[0] for i in self.sp_all_bd_tact]
                if self.lineEdit_name_tact_in_bd_tact.text() in im:  # Такт есть в БД
                    con = sqlite3.connect('_internal/tact_bd.db')
                    cur = con.cursor()
                    cur.execute(f"""DELETE FROM tact_table
                    WHERE id_name_tact = (SELECT id_name_tact from id_tact_table
                    WHERE name_tact IN ('{self.lineEdit_name_tact_in_bd_tact.text()}'))""", )

                    cur.execute(f"""DELETE FROM id_tact_table
                    WHERE name_tact IN ('{self.lineEdit_name_tact_in_bd_tact.text()}')""", )

                    con.commit()

                    self.sp_all_bd_tact = cur.execute("""SELECT id_tact_table.name_tact, 
                    tact_table.chisl, 
                    tact_table.znam, 
                    tact_table.tact_sp_t, 
                    tact_table.tact_sp_durations FROM tact_table
                    INNER JOIN id_tact_table ON tact_table.id_name_tact = id_tact_table.id_name_tact""").fetchall()

                    result = cur.execute("""SELECT id_name_tact FROM id_tact_table""").fetchall()

                    if not result:  # БД снесена в-ручную
                        self.label_pokaz_bd_tact.setText('В базе данных отсутствуют записи')
                        self.re_table_tact([['', '', '', []]], self.table_bd_tact)

                    con.close()

                    self.valid_msg.setText(f'Такт "{self.lineEdit_name_tact_in_bd_tact.text()}" удалён из базы данных')
                    self.valid_msg.exec()
                    self.valid_msg.setText('Такт успешно создан')
                else:  # Такта нет в БД
                    self.error_msg.setText('Такта с таким именем нет в базе данных')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')
            else:  # Имя такта не введено
                self.error_msg.setText('Имя такта не введено')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    # Двойное нажатие на таблицу с БД с тактами и добавление нажатого такта в редактор
    def table_bd_tact_activated(self, item):
        if item.column() == 0:
            name, c, z, sp_t, sp_dur = \
                [i for i in [[j for j in i if item.text() in i] for i in self.sp_all_bd_tact] if i][0]
            sp_dur = list(map(int, sp_dur.split(',')))
            sp_t = list(map(lambda x: int(x) if x.isdigit() else x, sp_t.split(',')))
            self.name_of_tact_lineEdit.setText(name)
            self.lineEdit_name_tact_in_bd_tact.setText(name)

            self.stok_tact = (c, z)

            self.media_player_stok_tact.stop()
            self.media_player_stok_tact.durations = [0.0001] + [
                Note(self.stok_tact[1], self.theme).get_note_duration()] * self.stok_tact[0]

            self.tact_for_durations = sp_dur
            self.tact_for_table = sp_t

            self.media_player_red_tact.stop()
            self.media_player_red_tact.durations = [0.0001] + correct_sp_dur_for_media(self.tact_for_table, self.theme)

            self.tact_duration = Note(self.stok_tact[1], self.theme).get_note_duration() * self.stok_tact[0]

            self.label_check_to_create_tact.setText('Такт задан, можете его заполнять')
            self.label_your_tact.setText(f'Ваш такт ({self.stok_tact[0]} / {self.stok_tact[1]}):')

            self.re_table_stok_tact()
            self.re_label_created_tact()
            self.re_table_podskaz_note()
            self.re_table_podskaz_note_tochka()

            self.valid_msg.setText(f'Такт "{name}" открыт для редактирования')
            self.valid_msg.exec()
            self.valid_msg.setText('Такт успешно создан')

    # Единичное нажатие на таблицу с БД с тактами и выбор нажатого такта
    def table_bd_tact_one_clicked(self, item):
        if item.column() == 0:
            self.lineEdit_name_tact_in_bd_tact.setText(item.text())

    # Показать таблицу с тактами из БД при редактировании совокупности тактов по нажатию кнопки
    def pokaz_tact_db_for_sovokup_func(self):
        self.pokaz_tact_db(self.tablet_tact_db_for_sovokup, self.label_tact_db_for_sovokup)

    # Визуализация таблицы с тактами
    def pokaz_tact_db(self, table, label):
        con = sqlite3.connect('_internal/tact_bd.db')
        cur = con.cursor()
        result = cur.execute("""SELECT id_name_tact FROM id_tact_table""").fetchall()

        if not result:  # В БД нет данных
            self.error_msg.setText('В базе данных нет ни одной записи')
            self.error_msg.exec()
            self.error_msg.setText('Вы превысили вместимость такта')
        else:  # В БД есть данные
            label.setText('База данных с тактами:')

            con = sqlite3.connect('_internal/tact_bd.db')
            cur = con.cursor()
            self.sp_all_bd_tact = cur.execute("""SELECT id_tact_table.name_tact, 
            tact_table.chisl, 
            tact_table.znam, 
            tact_table.tact_sp_t, 
            tact_table.tact_sp_durations FROM tact_table
            INNER JOIN id_tact_table ON tact_table.id_name_tact = id_tact_table.id_name_tact""").fetchall()
            con.close()

            self.sp_for_table_bd_tact = [
                list(map(lambda x: str(x), j[:-1])) + [
                    list(map(lambda x: int(x) if x.isdigit() else x, [k for k in j[-1].split(',')]))] for j in
                [i[:-1] for i in self.sp_all_bd_tact]]

            self.re_table_tact(self.sp_for_table_bd_tact, table)
            table.verticalHeader().setStyleSheet(
                "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
            )

        con.close()

    # Поиск такта в бд по введённой подстроке при создании совокупности тактов
    def lineEdit_search_in_bd_tact_sovokup_text_changed(self, text):
        self.search_in_bd_tact(text, self.label_tact_db_for_sovokup, self.tablet_tact_db_for_sovokup)

    # Поиск такта в бд по введённой подстроке
    def search_in_bd_tact(self, text, label, tabel):
        if label.text() == 'База данных с тактами:':
            sp_for_table_vs = []
            for i in self.sp_for_table_bd_tact:
                name, c, z, sp_dur = i
                if text.lower() in name.lower():
                    sp_for_table_vs.append([name, c, z, sp_dur])
            if sp_for_table_vs:
                self.re_table_tact(sp_for_table_vs, tabel)
            else:
                self.re_table_tact([['', '', '', []]], tabel)

    # Добавление такта в совокупность
    def add_tact_to_sovocup_func(self):
        if self.label_tact_db_for_sovokup.text() == 'База данных с тактами:':
            if self.lineEdit_add_tact_to_sovocup.text():  # Введено имя такта для добавления в совокупность
                if self.lineEdit_add_tact_to_sovocup.text() in [i[0] for i in self.sp_all_bd_tact]:  # Такт есть в БД
                    self.sovokup_sp.extend(
                        [list(map(str, i[:-2])) + [list(map(lambda x: int(x) if x.isdigit() else x, i[-2].split(',')))]
                         for i in self.sp_all_bd_tact if i[0] == self.lineEdit_add_tact_to_sovocup.text()])

                    self.media_player_red_sov.stop()
                    self.media_player_red_sov.durations = [0.0001] + correct_sp_dur_for_media(
                        linear([i[3:] for i in self.sovokup_sp]), self.theme)

                    self.re_table_tact(self.sovokup_sp, self.table_created_sovokup)
                else:  # Такта нет в БД
                    self.error_msg.setText(
                        f'Такта с именем "{self.lineEdit_add_tact_to_sovocup.text()}" нет в базе данных')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')
            else:  # Имя такта не введено
                self.error_msg.setText('Имя такта не введено')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    # Удаление такта из совокупности
    def del_tact_from_sovocup_func(self):
        if self.label_tact_db_for_sovokup.text() == 'База данных с тактами:':
            if self.lineEdit_del_tact_index.text():  # Введён индекс такта для удаления из совокупности
                if self.sovokup_sp:  # Наличие редактируемой совокупности
                    if 0 < int(self.lineEdit_del_tact_index.text().strip()) <= len(
                            self.sovokup_sp):  # Такт есть в совокупности
                        del self.sovokup_sp[int(self.lineEdit_del_tact_index.text().strip()) - 1]

                        self.media_player_red_sov.stop()
                        self.media_player_red_sov.durations = [0.0001] + correct_sp_dur_for_media(
                            linear([i[3:] for i in self.sovokup_sp]), self.theme)

                        if self.sovokup_sp:
                            self.re_table_tact(self.sovokup_sp, self.table_created_sovokup)
                        else:
                            self.re_table_tact([['', '', '', []]], self.table_created_sovokup)
                    else:  # Такта нет в совокупности
                        self.error_msg.setText(
                            f'Некорректный номер такта')
                        self.error_msg.exec()
                        self.error_msg.setText('Вы превысили вместимость такта')
                else:  # Отсутствие редактируемой совокупности
                    self.error_msg.setText('Совокупность пуста')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')
            else:  # Индекс такта не введён
                self.error_msg.setText('Номер такта не введён')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    # Добавление такта в совокупность двойным нажатием на такт в таблице тактов
    def tablet_tact_db_for_sovokup_ativated(self, item):
        if item.column() == 0:
            self.sovokup_sp.append([i for i in [
                list(map(str, i[:-2])) + [list(map(lambda x: int(x) if x.isdigit() else x, i[-2].split(',')))] for i in
                self.sp_all_bd_tact] if i[0] == item.text()][0])

            self.media_player_red_sov.stop()
            self.media_player_red_sov.durations = [0.0001] + correct_sp_dur_for_media(
                linear([i[3:] for i in self.sovokup_sp]), self.theme)

            self.re_table_tact(self.sovokup_sp, self.table_created_sovokup)
            self.lineEdit_add_tact_to_sovocup.setText(item.text())

    # Удаление такта из совокупности двойным нажатием на такт в таблице совокупности
    def table_created_sovokup_activated(self, item):
        if item.column() == 0:
            del self.sovokup_sp[item.row()]

            self.media_player_red_sov.stop()
            self.media_player_red_sov.durations = [0.0001] + correct_sp_dur_for_media(
                linear([i[3:] for i in self.sovokup_sp]), self.theme)

            self.lineEdit_del_tact_index.setText(f'{item.row() + 1}')

            if self.sovokup_sp:
                self.re_table_tact(self.sovokup_sp, self.table_created_sovokup)
            else:
                self.re_table_tact([['', '', '', []]], self.table_created_sovokup)

    # Добавление совокупности в БД
    def add_sovokup_to_db_func(self):
        if self.label_tact_db_for_sovokup.text() == 'База данных с тактами:':
            if self.lineEdit_name_sovokup_in_db.text():  # Введено имя совокупности
                if self.sovokup_sp:  # Совокупность существует
                    con = sqlite3.connect('_internal/tact_bd.db')
                    cur = con.cursor()
                    res_prov = cur.execute(f"""SELECT * from sovokup
                    WHERE name_sovokup = '{self.lineEdit_name_sovokup_in_db.text()}'""").fetchall()

                    if not res_prov:  # Добавление новой совокупности
                        data = [self.lineEdit_name_sovokup_in_db.text(),
                                ','.join([i[0] for i in self.sovokup_sp])]

                        cur.execute(f"""INSERT INTO sovokup(name_sovokup, sp_im_tact) 
                        VALUES (?, ?)""", data)

                        self.valid_msg.setText(
                            f'Совокупность тактов "{data[0]}" успешно добавлена в базу данных')
                        self.valid_msg.exec()
                        self.valid_msg.setText('Такт успешно создан')

                        con.commit()
                    else:  # Обновление данных в выбранной совокупности
                        data = [','.join([i[0] for i in self.sovokup_sp]),
                                self.lineEdit_name_sovokup_in_db.text()]

                        cur.execute(f"""UPDATE sovokup
                        SET sp_im_tact = ? 
                        WHERE name_sovokup = ?""", data)

                        self.valid_msg.setText(
                            f'Значения совокупности тактов "{data[1]}" в базе данных изменены')
                        self.valid_msg.exec()
                        self.valid_msg.setText('Такт успешно создан')

                        con.commit()

                    con.close()
                else:  # Совокупность пуста
                    self.error_msg.setText('Нельзя сохранить пустую совокупность')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')
            else:  # Не введено имя совокупности
                self.error_msg.setText('Имя совокупности не введено')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    def btn_clear_all_sov_func(self):
        if self.label_tact_db_for_sovokup.text() == 'База данных с тактами:':
            self.sovokup_sp.clear()

            self.media_player_red_sov.stop()
            self.media_player_red_sov.durations = [0]

            self.re_table_tact([['', '', '', []]], self.table_created_sovokup)

    # Показать БД совокупностей
    def pokas_bd_sovokup_func(self):
        con = sqlite3.connect('_internal/tact_bd.db')
        cur = con.cursor()
        result = cur.execute("""SELECT name_sovokup FROM sovokup""").fetchall()

        if not result:  # В БД нет данных
            self.error_msg.setText('В базе данных нет ни одной записи')
            self.error_msg.exec()
            self.error_msg.setText('Вы превысили вместимость такта')
        else:  # В БД есть данные
            self.label_pokaz_db_sov.setText('База данных совокупностей:')

            con = sqlite3.connect('_internal/tact_bd.db')
            cur = con.cursor()
            self.sp_db_sov = cur.execute("""SELECT * FROM sovokup""").fetchall()
            con.close()

            self.sp_db_sov = [[i[0]] + [[', '.join(i[1].split(','))]] for i in self.sp_db_sov]

            self.re_table_db_sov(self.sp_db_sov)

        con.close()

    # Обновление таблицы БД совокупностей
    def re_table_db_sov(self, sp_for_table):
        self.table_db_sov.clear()  # Очищаем от того, что было, даже если ничего не было
        self.table_db_sov.setRowCount(len(sp_for_table))  # Задаём количество строчек
        self.table_db_sov.setColumnCount(
            len(sp_for_table[0]))  # и столбцов (считаем, что в разных строчках одинаковое количество столбцов)
        self.table_db_sov.setHorizontalHeaderLabels(
            ['Имя совокупности', 'Имена тактов'])  # В первой строке файла — вертикальные заголовки

        for r, row in enumerate(sp_for_table):
            for c, val in enumerate(row):
                item = QTableWidgetItem()  # Объект конкретной ячейки
                if isinstance(val, list):
                    item.setText(val[0])
                else:
                    item.setText(val)
                self.table_db_sov.setItem(r, c, item)  # Ставим ячейку в нужное место

        # Умная ширина колонок
        header = self.table_db_sov.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(True)

        self.table_db_sov.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_db_sov.verticalHeader().setStyleSheet(
            "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
        )

    # Поиск сов. по имени в БД сов.
    def search_in_db_sov_func(self, text):
        if self.label_pokaz_db_sov.text() == 'База данных совокупностей:':
            sp_for_table_vs = []
            for i in self.sp_db_sov:
                name, sp_tacts = i
                if text.lower() in name.lower():
                    sp_for_table_vs.append([name, sp_tacts])
            if sp_for_table_vs:
                self.re_table_db_sov(sp_for_table_vs)
            else:
                self.re_table_db_sov([['', ['']]])

    # Выбор сов-ти двойным нажатием и визуал. таблицы с редактируемой сов-тью
    def table_db_sov_activated(self, item):
        if item.column() == 0:
            con = sqlite3.connect('_internal/tact_bd.db')
            cur = con.cursor()
            sov = cur.execute(f"""SELECT * from sovokup
            WHERE name_sovokup = '{item.text()}'""", ).fetchall()

            self.sovokup_sp_vs, sp_del_tacts = [], []

            for i in sov[0][1].split(','):
                rez = cur.execute(f"""SELECT id_tact_table.name_tact, 
                tact_table.chisl, 
                tact_table.znam, 
                tact_table.tact_sp_t, 
                tact_table.tact_sp_durations from tact_table
                INNER JOIN id_tact_table ON tact_table.id_name_tact = id_tact_table.id_name_tact
                WHERE id_tact_table.name_tact = '{i}'""", ).fetchall()

                if rez:  # Такт есть в БД, добавляем в список для визуал. сов-ти
                    self.sovokup_sp_vs.extend(
                        [list(map(str, i[:-2])) + [list(map(lambda x: int(x) if x.isdigit() else x, i[-2].split(',')))]
                         for i in rez])
                else:  # Такта нет в БД, вывод информации об отсутствующих в БД тактах
                    sp_del_tacts.append(i)

            if not sp_del_tacts:  # Все такты есть в БД
                self.re_table_tact(self.sovokup_sp_vs, self.table_select_sov)
                self.name_sov_red = item.text()
                self.label_red_sov.setText(f'Выбранная совокупность - "{item.text()}"')
            else:  # В БД нет каких-то тактов из выбранной сов-ти
                self.error_msg.setText(
                    f'В базе данных отсутствуют такт(-ы): {', '.join([f'"{i}"' for i in list(set(sp_del_tacts))])}\nНевозможно открыть совокупность')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

                self.sovokup_sp.clear()

                self.media_player_red_sov.stop()
                self.media_player_red_sov.durations = [0]

            self.lineEdit_name_sov_del_from_db.setText(item.text())

            con.close()

    # Открыть сов-ть для редактирования
    def open_sov_from_db_func(self):
        if self.label_pokaz_db_sov.text() == 'База данных совокупностей:':
            if self.label_red_sov.text() != 'Выбранная совокупность':  # Совокупность выбрана
                self.sovokup_sp = self.sovokup_sp_vs

                self.media_player_red_sov.stop()
                self.media_player_red_sov.durations = [0.0001] + correct_sp_dur_for_media(
                    linear([i[3:] for i in self.sovokup_sp]), self.theme)

                self.re_table_tact(self.sovokup_sp, self.table_created_sovokup)
                self.pokaz_tact_db_for_sovokup_func()
                self.lineEdit_name_sovokup_in_db.setText(self.name_sov_red)

                self.valid_msg.setText(f'Совокупность тактов "{self.name_sov_red}" добавлена в редактор')
                self.valid_msg.exec()
                self.valid_msg.setText('Такт успешно создан')
            else:  # Совокупность не выбрана
                self.error_msg.setText('Совокупность тактов не выбрана')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    # Удаление совокупности тактов из БД
    def del_sov_from_db_func(self):
        if self.label_pokaz_db_sov.text() == 'База данных совокупностей:':
            if self.lineEdit_name_sov_del_from_db.text():  # Поле имени для удаления сов-ти заполнено
                con = sqlite3.connect('_internal/tact_bd.db')
                cur = con.cursor()
                rez = cur.execute(f"""SELECT * from sovokup
                WHERE name_sovokup = '{self.lineEdit_name_sov_del_from_db.text()}'""").fetchall()

                if rez:  # Сов-ть есть в Бд
                    cur.execute(f"""DELETE from sovokup
                                    WHERE name_sovokup = '{self.lineEdit_name_sov_del_from_db.text()}'""")
                    con.commit()

                    self.valid_msg.setText(
                        f'Совокупность "{self.lineEdit_name_sov_del_from_db.text()}" успешно удалена из базы данных')
                    self.valid_msg.exec()
                    self.valid_msg.setText('Такт успешно создан')
                else:  # Сов-ти нет в БД
                    self.error_msg.setText(
                        f'Совокупности "{self.lineEdit_name_sov_del_from_db.text()}" нет в базе данных')
                    self.error_msg.exec()
                    self.error_msg.setText('Вы превысили вместимость такта')

                con.close()

            else:  # Поле не заполнено
                self.error_msg.setText(f'Имя совокупности для удаления не введено')
                self.error_msg.exec()
                self.error_msg.setText('Вы превысили вместимость такта')

    # Проигрывание стокового такта
    def play_stok_tact(self):
        self.media_player_stok_tact.reset_and_start()

    # Далее идут методы для проигрывателей
    def stop_play_stok_tact(self):
        self.media_player_stok_tact.stop()

    def play_red_tact(self):
        self.media_player_red_tact.reset_and_start()

    def stop_play_red_tact(self):
        self.media_player_red_tact.stop()

    def play_sovokup(self):
        self.media_player_red_sov.reset_and_start()

    def stop_play_sovokup(self):
        self.media_player_red_sov.stop()

    # Окно помощи
    def help(self):
        self.help.show()

    # Добавление имени совокупности в поле по единичному клину имя такта в таблице совокупностей
    def table_db_sov_clicked(self, item):
        if item.column() == 0:
            self.lineEdit_name_sov_del_from_db.setText(item.text())

    # Смена тем по клику на кнопку
    def theme_btn_clicked(self):
        self.theme = 'DARK_THEME' if self.theme == 'LIGHT_THEME' else 'LIGHT_THEME'
        self.setStyleSheet(LIGHT_THEME if self.theme == 'LIGHT_THEME' else DARK_THEME)
        self.theme_btn.setText('Тёмная тема' if self.theme == 'LIGHT_THEME' else 'Светлая тема')

        self.btn_note_1.setIcon(QIcon(Note(1, self.theme).get_note_link()))
        self.btn_note_2.setIcon(QIcon(Note(2, self.theme).get_note_link()))
        self.btn_note_4.setIcon(QIcon(Note(4, self.theme).get_note_link()))
        self.btn_note_8.setIcon(QIcon(Note(8, self.theme).get_note_link()))
        self.btn_note_16.setIcon(QIcon(Note(16, self.theme).get_note_link()))
        self.btn_note_32.setIcon(QIcon(Note(32, self.theme).get_note_link()))
        self.btn_note_64.setIcon(QIcon(Note(64, self.theme).get_note_link()))
        self.btn_note_tochka.setIcon(QIcon(Note('.', self.theme).get_note_link()))

        tables = [
            self.table_podskaz_note,
            self.table_podskaz_note_tochka,
            self.table_stok_tact,
            self.table_bd_tact,
            self.tablet_tact_db_for_sovokup,
            self.table_created_sovokup,
            self.table_db_sov,
            self.table_select_sov
        ]

        for table in tables:
            if table and table.verticalHeader():
                # Устанавливаем новый стиль вертикальных заголовков
                table.verticalHeader().setStyleSheet(
                    "background-color: #4A4D50;" if self.theme == 'DARK_THEME' else "background-color: #ededed;"
                )

        if self.label_check_to_create_tact.text() == 'Такт задан, можете его заполнять':
            self.re_label_created_tact()
        if self.stok_tact:
            self.re_table_podskaz_note()
            self.re_table_podskaz_note_tochka()
            self.re_table_stok_tact()
        if self.label_pokaz_bd_tact.text() == 'База данных с тактами:':
            self.pokaz_tact_db(self.table_bd_tact, self.label_pokaz_bd_tact)
        if self.label_tact_db_for_sovokup.text() == 'База данных с тактами:':
            self.re_table_tact(self.sp_for_table_bd_tact, self.tablet_tact_db_for_sovokup)
        if self.sovokup_sp:
            self.re_table_tact(self.sovokup_sp, self.table_created_sovokup)
        if self.label_pokaz_db_sov.text() == 'База данных совокупностей:':
            self.re_table_db_sov(self.sp_db_sov)
        if self.sovokup_sp_vs:
            self.re_table_tact(self.sovokup_sp_vs, self.table_select_sov)

    # Единичное нажатие на имя такта в таблице с тактами при ред-и совокупности
    def tablet_tact_db_for_sovokup_one_clicked(self, item):
        if item.column() == 0:
            self.lineEdit_add_tact_to_sovocup.setText(item.text())

    # Единичное нажатие на имя такта в таблице редактируемой совокупности
    def table_created_sovokup_one_clicked(self, item):
        if item.column() == 0:
            self.lineEdit_del_tact_index.setText(str(int(item.row() + 1)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TactCalculate()
    window.show()
    sys.exit(app.exec())