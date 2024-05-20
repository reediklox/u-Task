from PyQt5.QtWidgets import (QMessageBox, 
                             QSpinBox,
                             QDialog, 
                             QHBoxLayout,
                             QVBoxLayout,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QComboBox)

from PyQt5.QtCore import Qt

from stylesheets.style import *
from models.models import *

from utlis import config_font
from datetime import datetime


# Класс с диалоговым окном для добавления новой / изменения существующей задачи
class TasksDialog(QDialog):
    def __init__(self, project, is_update=False, task: Task=None):
        super().__init__()
        self.project = project
        self.status = False
        self.is_update = is_update
        self.task = task

        self.setWindowTitle("Добавить задачу")
        self.setStyleSheet('''
                             QDialog {
                                background-color: rgb(183, 204, 190);
                            }
                            
                             QLineEdit {
                                background-color: rgba(255, 255, 255, 0.2);
                                border: 1px solid #ccc;
                                padding: 5px;
                             }
                             
                             QComboBox {
                                background-color: rgba(255, 255, 255, 0.2);
                                border: 1px solid #ccc;
                                padding: 5px;
                             }
                             ''')
        
        layout = QVBoxLayout()

        title_label = QLabel("Название:")
        title_label.setFont(config_font(10))
        self.title_edit = QLineEdit()

        description_label = QLabel("Описание:")
        description_label.setFont(config_font(10))
        self.description_edit = QLineEdit()
        
        if is_update:
            self.title_edit.setText(self.task.name)
            self.description_edit.setText(self.task.description)

        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)
        layout.addWidget(description_label)
        layout.addWidget(self.description_edit)

        deadline_label = QLabel("Дедлайн:")
        deadline_label.setFont(config_font(10))
        self.deadline_day_combo = QComboBox()
        self.deadline_day_combo.setEditText(str(datetime.now().day))
        self.deadline_day_combo.setStyleSheet(COMBO_BOX)
        self.deadline_month_combo = QComboBox()
        self.deadline_month_combo.setEditText(str(datetime.now().month))
        self.deadline_month_combo.setStyleSheet(COMBO_BOX)
        self.deadline_year_combo = QComboBox()
        self.deadline_year_combo.setEditText(str(datetime.now().year))
        self.deadline_year_combo.setStyleSheet(COMBO_BOX)

        for i in range(1, 32):
            self.deadline_day_combo.addItem(str(i))
        for i in range(1, 13):
            self.deadline_month_combo.addItem(str(i))
        for i in range(datetime.now().year, datetime.now().year + 6):
            self.deadline_year_combo.addItem(str(i))

        self.deadline_layout = QHBoxLayout()
        self.deadline_layout.addWidget(self.deadline_day_combo)
        self.deadline_layout.addWidget(self.deadline_month_combo)
        self.deadline_layout.addWidget(self.deadline_year_combo)

        layout.addWidget(deadline_label)
        layout.addLayout(self.deadline_layout)

        hours_spinbox_label = QLabel('Количество часов на задачу')
        hours_spinbox_label.setFont(config_font(10))
        self.hours_spinbox = QSpinBox()
        if is_update:
            self.hours_spinbox.setValue(int(self.task.total_time))
        self.hours_spinbox.setStyleSheet(SPIN_BOX)
        self.hours_spinbox.setRange(0, 100)
        layout.addWidget(hours_spinbox_label)
        layout.addWidget(self.hours_spinbox)
        
        if not is_update:
            self.add_button = QPushButton("Добавить")
            self.add_button.setFont(config_font(12))
            self.add_button.setStyleSheet(IN_TAB_BUTTON)
            self.add_button.clicked.connect(self.add_task)
            layout.addWidget(self.add_button)
        else:
            self.update_button = QPushButton("Изменить")
            self.update_button.setFont(config_font(12))
            self.update_button.setStyleSheet(IN_TAB_BUTTON)
            self.update_button.clicked.connect(self.update_task)
            layout.addWidget(self.update_button)
        
        self.error_label = QLabel('Ошибка')
        self.error_label.setFont(config_font(9))
        self.error_label.setStyleSheet('color: red;')
        self.error_label.setVisible(False)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
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
                
                
    # Обновление задачи при нажатии на кнопку "Обновить"
    #
    # Вызывается на 114 строке
    def update_task(self):
        deadline = self.get_date_from_checkboxes()
        
        if self.title_edit.text() != self.task.name:
            Task.update({Task.name: self.title_edit.text()}).where(Task.id == self.task.id).execute()
        if self.description_edit.text() != self.task.description:
            Task.update({Task.description: self.description_edit.text()}).where(Task.id == self.task.id).execute()
        if int(self.hours_spinbox.text()) == int(self.task.total_time):
            Task.update({Task.total_time: self.hours_spinbox.value()}).where(Task.id == self.task.id).execute()
        if deadline != datetime.strptime(self.task.deadline.split()[0], '%Y-%m-%d'):
            Task.update({Task.deadline:deadline}).where(Task.id == self.task.id).execute()
        self.status = True
        self.close()


    # Добавляет новую задачу при нажатии на кнопку "Добавить"
    #
    # Вызывается на 108 строке
    def add_task(self):
        print("Добавление задачи...")
        self.title_edit.setStyleSheet('''
                                      QLineEdit {
                                        background-color: rgb(190, 220, 204);
                                        border: 1px solid #ccc;
                                        padding: 5px;
                                      }
                                      ''')
        
        
        if not self.title_edit.text():
            self.title_edit.setStyleSheet(LINE_EDIT_ERR)
            self.error_label.setText('Ошибка')
            self.error_label.setVisible(True)
            return
        else:
            print("Название:", self.title_edit.text())
            print("Описание:", self.description_edit.text())
            print("Дедлайн: {}-{}-{}".format(self.deadline_year_combo.currentText(),
                                            self.deadline_month_combo.currentText(),
                                            self.deadline_day_combo.currentText()))
            
            if int(self.hours_spinbox.text()) == 0:
                self.error_label.setText('Ошибка. Нулевое значение')
                self.error_label.setVisible(True)
                return
            deadline_date = self.get_date_from_checkboxes()
            print(datetime.strptime(self.project.deadline.split()[0], '%Y-%m-%d').year, int(self.deadline_year_combo.currentText()))
            if datetime.strptime(self.project.start_date.split()[0], '%Y-%m-%d').year > int(self.deadline_year_combo.currentText()) or int(self.deadline_year_combo.currentText()) > datetime.strptime(self.project.deadline.split()[0], '%Y-%m-%d').year:
                self.error_label.setText('Ошибка времени')
                self.error_label.setVisible(True)
                return
            if datetime.strptime(self.project.start_date.split()[0], '%Y-%m-%d').month > int(self.deadline_month_combo.currentText()) or int(self.deadline_month_combo.currentText()) > datetime.strptime(self.project.deadline.split()[0], '%Y-%m-%d').month:
                self.error_label.setText('Ошибка времени')
                self.error_label.setVisible(True)
                return
            if datetime.strptime(self.project.start_date.split()[0], '%Y-%m-%d').day > int(self.deadline_day_combo.currentText()) or int(self.deadline_day_combo.currentText()) > datetime.strptime(self.project.deadline.split()[0], '%Y-%m-%d').day:
                self.error_label.setText('Ошибка времени')
                self.error_label.setVisible(True)
                return
            
            Task.create(name=self.title_edit.text(),
                           description=self.description_edit.text(),
                           total_time=self.hours_spinbox.text(),
                           deadline=deadline_date,
                           project_id=self.project
                           )
            self.status = True
            self.close()
    
    
    # Возвращает дату в формате datetime из checkbox для выбора дат
    #
    # Вызывается на 144, 188 строках
    def get_date_from_checkboxes(self):
        deadline_day = self.get_checkbox_value(self.deadline_day_combo)
        deadline_month = self.get_checkbox_value(self.deadline_month_combo)
        deadline_year = self.get_checkbox_value(self.deadline_year_combo)

        deadline_str = f'{deadline_day.currentText()}.{deadline_month.currentText()}.{deadline_year.currentText()}'
        return datetime.strptime(deadline_str, "%d.%m.%Y")

    
    # Возвращает значение checkbox
    def get_checkbox_value(self, checkbox):
        if checkbox:
            return checkbox
        return ""