DARK_THEME = """
                    /* Темный стиль для всего главного окна */
                    QMainWindow {
                        background-color: #505152;
                    }
                    
                    /* Общее правило для шрифта в QTabWidget и всех вложенных элементах */
                    QTabWidget, QTabWidget * {
                        font-family: 'PT Root UI';
                    }
                    
                    QTabWidget::pane {
                        border-top: none; /* Убираем границу сверху */
                    }
                    
                    QTabWidget > QWidget {
                        background-color: #2b2b2b; /* Основной цвет фона */
                    }
                    
                    QTabBar::tab {
                        background-color: #4A4D50; /* Цвет фона неактивных вкладок */
                        color: #a9b7c6;
                    }
                    
                    QTabBar::tab:selected {
                        background-color: #55575A; /* Цвет фона выбранной вкладки */
                    }
                    
                    QTableWidget {
                        background-color: #333538; /* Темный фон */
                        gridline-color: #555; /* Светлая сетка */
                        show-grid: true; /* Показывать сетку */
                        gridline-width: 2px; /* Устанавливаем толщину линий сетки в 2 пикселя */
                        border: 2px solid #555; /* Толщина общей рамки таблицы тоже 2 пикселя */
                    }
                    
                    /* Изменяем цвет текста в ячейках таблицы */
                    QTableWidget::item {
                        color: #a9b7c6; /* Новый цвет текста в ячейках */
                    }
                    
                    /* Стилизация горизонтальных заголовков */
                    QHeaderView::section:horizontal {
                        background-color: #4A4D50; /* Темный серый фон горизонтальных заголовков */
                        color: #a9b7c6; /* Цвет текста горизонтальных заголовков */
                        font-weight: bold; /* Жирный шрифт горизонтальных заголовков */
                        border-bottom: 2px solid #555; /* Нижняя граница толщиной 2 пикселя */
                        border-right: 2px solid #555; /* Добавляем правую границу */
                    }
                    
                    /* Стилизация вертикальных заголовков */
                    QHeaderView::section:vertical {
                        background-color: #4A4D50; /* Темный серый фон вертикальных заголовков */
                        color: #a9b7c6; /* Цвет текста вертикальных заголовков */
                        font-weight: bold; /* Жирный шрифт вертикальных заголовков */
                        border-right: 2px solid #555; /* Правая граница толщиной 2 пикселя */
                        border-bottom: 2px solid #555; /* Добавляем нижнюю границу */
                    }
                    
                    QTableWidget::item:hover {
                        background-color: #4A4D50; /* Подсветка при наведении */
                        border: 2px solid #555; /* Непрерывная рамка толщиной 2 пикселя при наведении */
                    }
                    
                    /* Общие правила для заголовков */
                    QHeaderView::section {
                        background-color: #4A4D50; /* Однородный цвет фона */
                        color: #a9b7c6; /* Цвет текста */
                        font-weight: bold; /* Жирный шрифт */
                        border: none; /* Нет рамки */
                        text-align: center; /* Центрированный текст */
                    }
                    
                    /* Специальные правила для первого, последнего и единственного раздела */
                    QHeaderView::section:first {
                        border-right: 2px solid #555; /* Граница справа */
                    }
                    
                    QHeaderView::section:last {
                        border-left: 2px solid #555; /* Граница слева */
                    }
                    
                    QHeaderView::section:only-one {
                        border: none; /* Убираем границы, если единственная колонка */
                    }
                    
                    /* Стиль для кнопок */
                    QPushButton {
                        background-color: #3c3f41;
                        color: #a9b7c6;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    /* Стиль для кнопок при наведении мышки */
                    QPushButton:hover {
                        border: 2px solid #3498DB; /* Синяя рамка */
                        border-radius: 10px;
                    }
                    
                    /* Стиль для кнопок при клике мышки */
                    QPushButton:pressed {
                        border: 2px solid #2980B9; /* Тёмно-синяя рамка */
                        border-radius: 10px;
                    }
                    
                    /* Стиль для полей ввода */
                    QLineEdit {
                        background-color: #3c3f41;
                        color: #a9b7c6;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    /* Стиль для QTextBrowser (такой же как у LineEdit) */
                    QTextBrowser {
                        background-color: #3c3f41;
                        color: #a9b7c6;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    /* Стиль для спинбоксов */
                    QSpinBox {
                        background-color: #3c3f41;
                        color: #a9b7c6;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    /* Стиль для комбобоксов */
                    QComboBox {
                        background-color: #3c3f41;
                        color: #a9b7c6;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    /* Стиль для меток QLabel */
                    QLabel {
                        color: #a9b7c6; /* Новый цвет текста в label */
                    }
                    
                    QTableCornerButton {
                        background-color: #4A4D50; /* Темный серый фон для верхнего левого уголка */
                    }
                    
                    QPushButton#btn_note_1 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_2 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_4 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_8 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_16 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_32 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_64 {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_tochka {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_note_delete_one_tact {
                        background-color: #333538;
                    }
                    
                    QPushButton#btn_clear_all_tact {
                        background-color: #333538;
                    }
        """

LIGHT_THEME = """
                    /* Стиль для всего главного окна */
                    QMainWindow {
                        background-color: #FFFFFF;
                    }

                    /* Общее правило для шрифта в QTabWidget и всех вложенных элементах */
                    QTabWidget, QTabWidget * {
                        font-family: 'PT Root UI';
                    }

                    QTabWidget::pane {
                        border-top: none; /* Убираем границу сверху */
                    }

                    QTabWidget > QWidget {
                        background-color: #f5f5f5; /* Основной цвет фона */
                    }

                    QTabBar::tab {
                        background-color: #E8E8E8; /* Цвет фона неактивных вкладок */
                    }

                    QTabBar::tab:selected {
                        background-color: #D0D0D0; /* Цвет фона выбранной вкладки */
                    }

                    QTableWidget {
                        background-color: #F4F7FC; /* Белый фон */
                        gridline-color: #DDD; /* Цвет сетчатой структуры */
                        show-grid: true; /* Показывать сетку */
                        gridline-width: 2px; /* Устанавливаем толщину линий сетки в 2 пикселя */
                        border: 2px solid #DDD; /* Толщина общей рамки таблицы тоже 2 пикселя */
                    }

                    /* Стилизация горизонтальных заголовков */
                    QHeaderView::section:horizontal {
                        background-color: #ededed; /* Серый фон горизонтальных заголовков */
                        color: #333; /* Цвет текста горизонтальных заголовков */
                        font-weight: bold; /* Жирный шрифт горизонтальных заголовков */
                        border-bottom: 2px solid #DDD; /* Нижняя граница толщиной 2 пикселя */
                        border-right: 2px solid #DDD; /* Добавляем правую границу */
                    }
                    
                    /* Стилизация вертикальных заголовков */
                    QHeaderView::section:vertical {
                        background-color: #ededed; /* Серый фон вертикальных заголовков */
                        color: #333; /* Цвет текста вертикальных заголовков */
                        font-weight: bold; /* Жирный шрифт вертикальных заголовков */
                        border-right: 2px solid #DDD; /* Правая граница толщиной 2 пикселя */
                        border-bottom: 2px solid #DDD; /* Добавляем нижнюю границу */
                    }

                    QTableWidget::item:hover {
                        background-color: #E8E8E8; /* Подсветка при наведении */
                        border: 2px solid #DDD; /* Непрерывная рамка толщиной 2 пикселя при наведении */
                    }

                    /* Общие правила для заголовков */
                    QHeaderView::section {
                        background-color: #E8E8E8; /* Однородный цвет фона */
                        color: #333; /* Цвет текста */
                        font-weight: bold; /* Жирный шрифт */
                        border: none; /* Нет рамки */
                        text-align: center; /* Центрированный текст */
                    }

                    /* Специальные правила для первого, последнего и единственного раздела */
                    QHeaderView::section:first {
                        border-right: 2px solid #DDD; /* Граница справа */
                    }

                    QHeaderView::section:last {
                        border-left: 2px solid #DDD; /* Граница слева */
                    }

                    QHeaderView::section:only-one {
                        border: none; /* Убираем границы, если единственная колонка */
                    }

                    /* Стиль для кнопок */
                    QPushButton {
                        background-color: #F4F7FC;
                        color: #000000 ;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }

                    /* Стиль для кнопок при наведении мышки */
                    QPushButton:hover {
                        border: 2px solid #3498db; /* Синяя рамка */
                        border-radius: 10px;
                    }

                    /* Стиль для кнопок при клике мышки */
                    QPushButton:pressed {
                        border: 2px solid #2980b9; /* Тёмно-синяя рамка */
                        border-radius: 10px;
                    }

                    QLineEdit {
                        background-color: #fcfdff;
                        color: #000000;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    QSpinBox {
                        background-color: #F4F7FC;
                        color: #000000 ;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }
                    
                    /* Стиль для комбобоксов */
                    QComboBox {
                        background-color: #F4F7FC;
                        color: #000000 ;
                        border: 1px solid #555;
                        border-radius: 5px;
                        padding: 5px 10px;
                        outline: none; /* Убираем пунктирную обводку */
                    }

                """