from PyQt5.QtWidgets import (QMessageBox, 
                             QTimeEdit,
                             QDialog, 
                             QVBoxLayout, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton, 
                             QComboBox)

from PyQt5.QtCore import Qt

from stylesheets.style import *
from models.models import *

from utlis import config_font
from datetime import datetime, date


# Класс диалоговое окно для создания новых событий
class EventDialog(QDialog):
    def __init__(self, parent=None, calendar_id: Calendar=None, choosen_date: date=None):
        super().__init__(parent)
        
        self.calendar_id = calendar_id
        self.choosen_date = choosen_date
        
        self.status = False
        
        self.setWindowTitle('Добавление события')
        self.setStyleSheet('''
                             QDialog {
                                background-color: rgb(183, 204, 190);
                            }
                            
                             QLineEdit {
                                background-color: rgba(255, 255, 255, 0.2);
                                border: 1px solid #ccc;
                                padding: 5px;
                             }
                             
                             QTimeEdit {
                                 background-color: rgba(255, 255, 255, 0.2);
                                 border: none;
                             }
                             
                             QTimeEdit::up-button { 
                                 subcontrol-origin: padding; 
                                 subcontrol-position: top right; 
                                 width: 0px; 
                             }
                             QTimeEdit::down-button { 
                                 subcontrol-origin: padding; 
                                 subcontrol-position: bottom right; 
                                 width: 0px; 
                             }
                             ''')
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Название:")
        title_label.setFont(config_font(12))
        self.title_edit = QLineEdit()
        
        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)
        
        type_label = QLabel("Тип:")
        type_label.setFont(config_font(12))
        self.type_combo = QComboBox()
        self.type_combo.setStyleSheet(COMBO_BOX)
        self.type_combo.setFont(config_font(10))
        
        if calendar_id.type == 'Праздники':
            self.type_combo.addItems(['День рождения', 'Праздник', 'Больничный', 'Отпуск'])
        else:
            self.type_combo.addItems(['Митинг', 'Задача'])
            
        layout.addWidget(type_label)
        layout.addWidget(self.type_combo)
        if calendar_id.type == 'Работа':
            time_label = QLabel('Время:')
            time_label.setFont(config_font(12))
            self.time_edit = QTimeEdit()
            self.time_edit.setFont(config_font(10))
            
            layout.addWidget(time_label)
            layout.addWidget(self.time_edit)
        
        description_label = QLabel("Описание:")
        description_label.setFont(config_font(12))
        self.description = QLineEdit()
        self.description.setMinimumHeight(50)
        
        layout.addWidget(description_label)
        layout.addWidget(self.description)
        
        self.add_button = QPushButton("Добавить")
        self.add_button.setFont(config_font(12))
        self.add_button.setStyleSheet(IN_TAB_BUTTON)
        self.add_button.clicked.connect(self.add_event)
        
        self.error_label = QLabel('Ошибка')
        self.error_label.setFont(config_font(9))
        self.error_label.setStyleSheet('color: red;')
        self.error_label.setVisible(False)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        layout.addWidget(self.add_button)
        layout.addWidget(self.error_label)
        
        self.setLayout(layout)
        self.show()
    
    
    # Обработка нажатия на кнопку "Закрыть окно" (крестик)
    def closeEvent(self, event):
        if self.status == True:
            event.accept()
        else:
            reply = QMessageBox.question(self, 'Message', 
                "Вы уверены, что хотите закрыть вкладку?", QMessageBox.Yes | 
                QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.status = False
                event.accept()
            else:
                event.ignore()
    
    
    # Добавляет новое событие при нажатии на кнопку "Добавить"
    #
    # Вызывается на 100 строке
    def add_event(self):
        if not self.title_edit.text():
            self.title_edit.setStyleSheet(LINE_EDIT_ERR)
            self.error_label.setText('Ошибка')
            self.error_label.setVisible(True)
            
        if self.calendar_id.type == 'Работа':
            time=datetime.strptime(self.time_edit.time().toString('HH:mm'), "%H:%M").time()
        else:
            time=None
        
        
        Event.create(name=self.title_edit.text(),
                     type=self.type_combo.currentText(),
                     date=self.choosen_date,
                     time=time,
                     description=self.description.text(),
                     calendar_id=self.calendar_id)
        
        self.status = True
        self.close()