import os
from PyQt6.QtCore import QUrl, pyqtSignal, QObject, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from design_files.help import Ui_Form
from PyQt6.QtWidgets import QWidget


class MediaController(QObject):
    finished = pyqtSignal()

    def __init__(self, durations):
        super().__init__()
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.file_path = QUrl.fromLocalFile(os.path.abspath('_internal/фа_первая_октава.mp3'))
        self.media_player.setSource(self.file_path)
        self.audio_output.setVolume(1.0)
        self.durations = durations
        self.current_duration_idx = 0
        self.is_stopped = False

    def play_next_segment(self):
        if self.is_stopped or self.current_duration_idx >= len(self.durations):
            self.finished.emit()
            return

        current_duration_seconds = self.durations[self.current_duration_idx]
        # Добавляем минимальное значение длительности для надежности воспроизведения
        extended_duration_ms = max(int(current_duration_seconds * 1000), 50)  # Минимальная продолжительность 50 мс
        self.media_player.play()
        QTimer.singleShot(extended_duration_ms, lambda: self.advance_segment())

    def advance_segment(self):
        self.current_duration_idx += 1
        self.media_player.stop()
        self.play_next_segment()

    def reset_and_start(self):
        self.media_player.stop()
        self.current_duration_idx = 0
        self.is_stopped = False
        self.play_next_segment()

    def stop(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
            self.is_stopped = True


# Класс для нот
class Note:
    def __init__(self, note, theme):
        self.note = note

        dark_theme_slov_link = {2: '_internal/images/black_notes/main/половинная.png',
                                4: '_internal/images/black_notes/main/четвертная.png',
                                8: '_internal/images/black_notes/main/8-ая.png',
                                16: '_internal/images/black_notes/main/16-ая.png',
                                32: '_internal/images/black_notes/main/32-ая.png',
                                64: '_internal/images/black_notes/main/64-ая.png',
                                1: '_internal/images/black_notes/main/целая.png',
                                '.': '_internal/images/black_notes/main/точка.png'}

        light_theme_slov_link = {2: '_internal/images/light_notes/main/половинная.png',
                                 4: '_internal/images/light_notes/main/четвертная.png',
                                 8: '_internal/images/light_notes/main/8-ая.png',
                                 16: '_internal/images/light_notes/main/16-ая.png',
                                 32: '_internal/images/light_notes/main/32-ая.png',
                                 64: '_internal/images/light_notes/main/64-ая.png',
                                 1: '_internal/images/light_notes/main/целая.png',
                                 '.': '_internal/images/light_notes/main/точка.png'}

        light_theme_slov_link_label = {2: '_internal/images/light_notes/label/половинная.png',
                                       4: '_internal/images/light_notes/label/четвертная.png',
                                       8: '_internal/images/light_notes/label/8-ая.png',
                                       16: '_internal/images/light_notes/label/16-ая.png',
                                       32: '_internal/images/light_notes/label/32-ая.png',
                                       64: '_internal/images/light_notes/label/64-ая.png',
                                       1: '_internal/images/light_notes/label/целая.png',
                                       '.': '_internal/images/light_notes/label/точка.png'}

        dark_theme_slov_link_label = {2: '_internal/images/black_notes/label/половинная.png',
                                      4: '_internal/images/black_notes/label/четвертная.png',
                                      8: '_internal/images/black_notes/label/8-ая.png',
                                      16: '_internal/images/black_notes/label/16-ая.png',
                                      32: '_internal/images/black_notes/label/32-ая.png',
                                      64: '_internal/images/black_notes/label/64-ая.png',
                                      1: '_internal/images/black_notes/label/целая.png',
                                      '.': '_internal/images/black_notes/label/точка.png'}

        self.slov_note_link = light_theme_slov_link if theme == 'LIGHT_THEME' else dark_theme_slov_link
        self.slov_note_link_label = light_theme_slov_link_label if theme == 'LIGHT_THEME' else dark_theme_slov_link_label

    def get_note_duration(self):
        return 4 / self.note

    def get_note_link(self):
        return self.slov_note_link[self.note]

    def get_note(self):
        return self.note

    def get_note_link_label(self):
        return self.slov_note_link_label[self.note]


# Линеаризация списка
def linear(sp):
    if not sp:
        return sp
    if type(sp[0]) is list:
        return linear(sp[0]) + linear(sp[1:])
    return sp[:1] + linear(sp[1:])


# Список длительностей для проигрывания
def correct_sp_dur_for_media(sp, theme):
    # sp - копия self.tact_for_table
    sp_out = sp.copy()
    for i, li in enumerate(sp):
        if li == '.':
            sp_out[i - 1] = Note(sp[i - 1], theme).get_note_duration() + Note(int(sp[i - 1] * 2),
                                                                              theme).get_note_duration()
        else:
            sp_out[i] = Note(sp[i], theme).get_note_duration()
    sp_out = [i for i in list(filter(lambda x: isinstance(x, float), sp_out))]
    return sp_out


# Окошко помощи
class Help(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        html = '''    <h2>Главная страница</h2>
    <p style="font-size: 18px; line-height: 21px">
      Здесь вы можете открыть мануал с инструкцией или поменять тему
    </p>
    <br />
    <h2>Задание размера такта</h2>
    <p style="font-size: 18px; line-height: 21px">
      На этой странице можно задать размер нового такта (обязательное условие
      перед редактированием такта), загрузить для редактирования уже готовый или
      проиграть такт в его изначальном виде
    </p>
    <br />
    <h2>Редактор такта</h2>
    <p style="font-size: 18px; line-height: 21px">
      Если задан размер такта или такт загружен из csv или базы данных, то можно
      приступать к его редактированию. В такт можно добавить ноты из
      предложенных (максимум с одной точкой), удалить их, сохранить верно
      составленный такт в csv или в базу данных. Также реализованы таблицы с
      подсказками какие ноты какого вида ещё могут вместится в такт. Кроме
      этого, есть возможность проиграть редактируемый такт
    </p>
    <br />
    <h2>База данных тактов</h2>
    <p style="font-size: 18px; line-height: 21px">
      В этом окне вы можете взаимодействовать с базой данных тактов.
      Присутствует поиск такта в БД по введённому в отдельном поле имени такта.
      Двойным нажатием по имени в таблице можно добавить выбранный такт в
      редактор. Помимо этого, такты можно удалять из БД (само собой при их
      наличии)
    </p>
    <br />
    <h2>Редактор совокупности тактов</h2>
    <p style="font-size: 18px; line-height: 21px">
      Кроме создания отдельных тактов, их можно объединять в
      <i>"совокупности тактов"</i>, которые в свою очередь представляют из себя
      "склейку" тактов. В этом окне есть визуализация таблицы с тактами из базы
      данных, по двойному нажатию на имя такта в этой таблице, выбранный такт
      добавляется в редактируемую совокупность. По двойному нажатию на имя такта
      в таблице редактируемой совокупности выбранный такт из неё удаляется.
      Также можно проиграть совокупность или добавить её в базу данных
    </p>
    <br />
    <h2>База данных совокупностей</h2>
    <p style="font-size: 18px; line-height: 21px">
      Через это окно осуществляется управление базой данных совокупностей
      тактов. В табличке страва визуализируется база данных совокупностей в
      виде: имя совокупности - список имён тактов в ней. По двойному нажатию на
      имя совокупности в этой таблице выбранная совокупность отображается в табличке
      слева, откуда есть возможность открыть её в редакторе. Также совокупность
      можно проиграть или удалить из базы данных
    </p>
    <br />
    <h2>Примечания</h2>
    <p style="font-size: 18px; line-height: 21px">
      Все такты проигрываются в 60 bpm (60 четвертных нот в минуту), в
      большинстве таблиц реализован поиск элемента по его имени
    </p>'''

        self.textBrowser_help.setHtml(html)
