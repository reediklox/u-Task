
QTABWIDGET = """
            QTabWidget {
                background-color: #f0f0f0;
            }

            QTabBar::tab {
                background-color: rgb(190, 220, 204);
                border: none;
                color: rgb(70,80,64);
                padding: 10px;
                margin: 0px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }

            QTabBar::tab:selected {
                background-color: rgb(178, 198, 184);
            }

            QTabBar::tab:hover {
                background-color: rgb(178, 198, 184);
            }

            QTabBar::tab:!selected {
                margin-top: 1px; /* Разрыв между вкладками */
            }

            QTabWidget::pane {
                background-color: #f0f0f0;
            }

    
            QTabBar::right-arrow, QTabBar::left-arrow {
                visibility: hidden;
            }
        """
        
QTABWIDGET_IN_PROJECT = """
                        QTabWidget {
                            background-color: #f0f0f0;
                        }

                        QTabBar::tab {
                            background-color: rgb(190, 220, 204);
                            border: none;
                            color: rgb(70,80,64);
                            padding: 10px;
                            margin: 0px;
                            border-top-left-radius: 0px;
                            border-bottom-left-radius: 0px;
                            border-top-right-radius: 10px;
                            border-bottom-right-radius: 10px;
                        }

                        QTabBar::tab:selected {
                            background-color: rgb(183, 204, 190);
                        }

                        QTabBar::tab:hover {
                            background-color: rgb(178, 198, 184);
                        }

                        QTabBar::tab:!selected {
                            margin-top: 1px; /* Разрыв между вкладками */
                        }

                        QTabWidget::pane {
                            background-color: #f0f0f0;
                        }

                        QTabBar::bottom-arrow, QTabBar::top-arrow{
                            visibility: hidden;
                        }
                        
                        QTabBar::close-button {
                            image: url();
                        }
                    """


IN_TAB_BUTTON =  """
            QPushButton {
                background-color: #72a99d;
                border-radius: 10px;
                color: black;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5f9b8d;
            }
            QPushButton:pressed {
                background-color: #619e90;
            }
        """
        
ADD_BUTTON = """
            QPushButton {
                background-color: #72a99d;
                border: none;
                color: rgb(70,80,64);
                font: bold;
                padding: 5px 5px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #5f9b8d; /* Темно-зеленый */
            }
            QPushButton:pressed {
                background-color: #619e90; /* Зеленый при нажатии */
            }
        """
        
        
COMBO_BOX = '''
            QComboBox {
                background-color: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: black;
                font-size: 10px;
            }

            QComboBox::drop-down {
                border: none;
                background-color: transparent;
            }

            QComboBox::down-arrow {
                image: url(resourses/assets/caret-down-solid.svg);
                width: 20px;
                height: 20px;
            }                               
'''

SPIN_BOX = '''
            QSpinBox {
                background-color: rgba(255, 255, 255, 0.2);
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 16px;
            }

            QSpinBox::up-button,
            QSpinBox::down-button {
                background-color: transparent;
                border: none;
            }

            QSpinBox::up-button:hover,
            QSpinBox::down-button:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            QSpinBox::up-arrow {
                image: url(resourses/assets/caret-arrow-up.png)
                width: 20px;
                height: 20px;
            }
            
            QSpinBox::down-arrow {
                image: url(resourses/assets/down.png)
                width: 20px;
                height: 20px;
            }
'''

LINE_EDIT_ERR = '''
                QLineEdit {
                background-color: rgb(190, 220, 204);
                border: 1px solid red;
                padding: 5px;
                }
'''


PROJECT_BUTTON = '''
                QPushButton {
                    background-color: #5f9b8d;
                    border: none;
                    padding: 10px 20px;
                    width: 100px;
                    border-top-left-radius: 40px;
                    border-bottom-right-radius: 40px;
                }
                
                QLabel {
                   background-color: #5f9b8d; 
                   border-radius: 10px;
                }
'''


SCROLLAREA = '''
            QScrollArea{
                border:  1px solid lightgray;
                background-color: rgb(190, 220, 204);
            }
            /* SCROLLBAR */
            QScrollArea QScrollBar:Vertical{
                border:  none;
                background-color: #0d1a14;
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius:10px;
            }
            /* HANDLE BAR VERTICAL */
            QScrollArea QScrollBar::handle:vertical{
                background-color: rgb(178, 190, 171);
                min-height: 30px;
                border-bottom-left-radius:7px;
                border-bottom-right-radius:7px;
                
            }
            QScrollArea QScrollBar::handle:vertical:hover{
                background-color: rgb(178, 190, 171);
            }
            QScrollArea QScrollBar::handle:vertical:pressed{
                background-color: rgb(178, 190, 171);
            }
            /* BTN TOP-SCROLLBAR */
            QScrollArea QScrollBar::sub-line:vertical{
                border:  none;
                background-color: #0d1a14;
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollArea QScrollBar::sub-line:vertical:hover{
                background-color: #0d1a14;
            }
            QScrollArea QScrollBar::sub-line:vertical:pressed{
                background-color: #0d1a14;
            }
            /* BTN BOTTOM-SCROLLBAR */
            QScrollArea QScrollBar::add-line:vertical{
                border:  none;
                background-color: #0d1a14;
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollArea QScrollBar::add-line:vertical:hover{
                background-color: #0d1a14;
            }
            QScrollArea QScrollBar::add-line:vertical:pressed{
                background-color: #0d1a14;
            }
            /* RESET ARROW */
            QScrollArea QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
                background:none;
            }
            QScrollArea QScrollBar::add-page:vertical, QScrollBar::sup-page:vertical{
                background:none;
            }
'''


COMBO_MENU = '''
            QMenu {
                background-color: #72a99d;
                border-radius: 10px;
                color: black;
                padding: 10px 20px;
                border: none;
            }
            QMenu::item:selected {
                background-color: #5f9b8d;
            } 
'''

IN_TAB_LINE =  """
            QLineEdit {
                background-color: #72a99d;
                border-radius: 10px;
                color: black;
                padding: 10px 20px;
                border: none;
            }
            QLineEdit:hover {
                background-color: #5f9b8d;
            }
            QLineEdit:pressed {
                background-color: #619e90;
            }
        """
    
CALENDAR = '''
        QCalendarWidget {
            background-color: rgb(255, 255, 255); /* Цвет фона */
            border: 1px solid #c4c4c4; /* Граница */
            color: black;
        }

        QCalendarWidget QAbstractItemView {
            selection-background-color: #5f9b8d; /* Цвет выделенного дня */
            font-size: 14px; /* Размер шрифта */
        }

        QCalendarWidget QToolButton {
            width: 50px; /* Ширина кнопок */
            height: 40px; /* Высота кнопок */
        }
        
        QToolButton#qt_calendar_prevmonth {
            background-color: #5f9b8d;
            border: none;
            width: 40px;
            qproperty-icon: url();
        }
        QToolButton#qt_calendar_nextmonth {
            background-color: #5f9b8d;
            border: none;
            width: 40px;
            qproperty-icon: url();
        }
        
        QToolButton#qt_calendar_yearbutton {
            background-color: #72a99d;
        }
        
        QToolButton#qt_calendar_yearbutton::hover {
            background-color: #72a99d;
            border: none;
            color: #5f9b8d
        }
        
        QToolButton#qt_calendar_monthbutton {
            background-color: #72a99d;
        }
        
        QToolButton#qt_calendar_monthbutton::hover {
            background-color: #72a99d;
            border: none;
            color: #5f9b8d
        }
        
        QToolButton#qt_calendar_monthbutton::pressed {
            background-color: #72a99d;
            border: none;
            color: #5f9b8d
        }
        
        QToolButton#qt_calendar_monthbutton QMenu {
            background-color: #72a99d;
            border-radius: 10px;
            color: white;
            padding: 5px 10px;
            border: none;
        }
        
        QToolButton#qt_calendar_monthbutton QMenu::item:selected {
            background-color: #5f9b8d;
        } 

        QCalendarWidget QWidget#qt_calendar_navigationbar {
            background-color: #72a99d; /* Цвет фона панели навигации */
            border: none; /* Убираем границу */
        }

        QCalendarWidget QSpinBox {
            background-color: #5f9b8d; /* Цвет фона */
            border: 1px solid #72a99d; /* Граница */
            selection-background-color: #5f9b8d; /* Цвет выделенного элемента */
            font-size: 14px; /* Размер шрифта */
        }
    
        QCalendarWidget QAbstractSpinBox::up-button, 
        QCalendarWidget QAbstractSpinBox::down-button {
            width: 20px; /* Ширина кнопок */
            border: none; 
        }

        QCalendarWidget QAbstractSpinBox::up-button {
            subcontrol-origin: padding; /* Отступ от края */
            subcontrol-position: top right; /* Позиция */
        }

        QCalendarWidget QAbstractSpinBox::down-button {
            subcontrol-origin: padding; /* Отступ от края */
            subcontrol-position: bottom right; /* Позиция */
        }

'''