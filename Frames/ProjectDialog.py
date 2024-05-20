from PyQt5.QtWidgets import (QMessageBox,
                             QSpinBox, 
                             QDialog, 
                             QHBoxLayout,
                             QVBoxLayout,
                             QLabel, QLineEdit, 
                             QPushButton, 
                             QComboBox)

from PyQt5.QtCore import Qt

from stylesheets.style import *
from models.models import *

from utlis import config_font
from datetime import datetime


# Класс диалоговое окно для создания новых / изменения существующих проектов
class ProjectDialog(QDialog):
    def __init__(self, board_id, is_update=False, project=None):
        super().__init__()
        self.board = board_id
        self.status = False
        
        if is_update:
            self.project: Project = project

        self.setWindowTitle("Добавить проект")
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
        
        if is_update:
            self.title_edit.setText(self.project.name)

        description_label = QLabel("Описание:")
        description_label.setFont(config_font(10))
        self.description_edit = QLineEdit()
        if is_update:
            self.description_edit.setText(self.project.description)

        comment_label = QLabel("Комментарий:")
        comment_label.setFont(config_font(10))
        self.comment_edit = QLineEdit()
        if is_update:
            self.comment_edit.setText(self.project.comment)

        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)
        layout.addWidget(description_label)
        layout.addWidget(self.description_edit)
        layout.addWidget(comment_label)
        layout.addWidget(self.comment_edit)

        start_date_label = QLabel("Дата начала:")
        start_date_label.setFont(config_font(10))
        self.start_day_combo = QComboBox()
        self.start_day_combo.setEditText(str(datetime.now().day))
        self.start_day_combo.setStyleSheet(COMBO_BOX)
        self.start_month_combo = QComboBox()
        self.start_month_combo.setEditText(str(datetime.now().month))
        self.start_month_combo.setStyleSheet(COMBO_BOX)
        self.start_year_combo = QComboBox()
        self.start_year_combo.setEditText(str(datetime.now().year))
        self.start_year_combo.setStyleSheet(COMBO_BOX)

        for i in range(1, 32):
            self.start_day_combo.addItem(str(i))
        for i in range(1, 13):
            self.start_month_combo.addItem(str(i))
        for i in range(datetime.now().year, datetime.now().year + 6):
            self.start_year_combo.addItem(str(i))

        self.start_date_layout = QHBoxLayout()
        self.start_date_layout.addWidget(self.start_day_combo)
        self.start_date_layout.addWidget(self.start_month_combo)
        self.start_date_layout.addWidget(self.start_year_combo)
        
        layout.addWidget(start_date_label)
        layout.addLayout(self.start_date_layout)

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

        status_label = QLabel("Статус:")
        status_label.setFont(config_font(10))
        self.status_combo = QComboBox()
        self.status_combo.setStyleSheet(COMBO_BOX)
        self.status_combo.addItems(["В процессе", "Завершено", "Приостановлено"])
        self.status_combo.setFont(config_font(10))

        layout.addWidget(status_label)
        layout.addWidget(self.status_combo)

        hours_spinbox_label = QLabel('Количество часов на проект')
        hours_spinbox_label.setFont(config_font(10))
        self.hours_spinbox = QSpinBox()
        self.hours_spinbox.setStyleSheet(SPIN_BOX)
        
        self.hours_spinbox.setRange(0, 1000)
        layout.addWidget(hours_spinbox_label)
        layout.addWidget(self.hours_spinbox)
        
        hours_spinbox_label_day = QLabel('Количество рабочих дней')
        hours_spinbox_label_day.setFont(config_font(10))
        self.hours_spinbox_day = QSpinBox()
        self.hours_spinbox_day.setStyleSheet(SPIN_BOX)
        self.hours_spinbox_day.setRange(0, 1000)
        layout.addWidget(hours_spinbox_label_day)
        layout.addWidget(self.hours_spinbox_day)
        
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
            self.update_button.clicked.connect(self.update_project)
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
    
    
    # Обновление проекта при нажатии на кнопку "Обновить"
    #
    # Вызывается на 167 строке
    def update_project(self):
        start_date, deadline = self.get_date_from_checkboxes()
        spend_time_total = int(self.hours_spinbox.text()) / int(self.hours_spinbox_day.text())
        spend_time_day = f'{int(spend_time_total)} часов {int((spend_time_total-int(spend_time_total)) * 60)} минут в день'
        
        if self.title_edit.text() != self.project.name:
            Project.update({Project.name: self.title_edit.text()}).where(Project.id == self.project.id).execute()
        if self.description_edit.text() != self.project.description:
            Project.update({Project.description: self.description_edit.text()}).where(Project.id == self.project.id).execute()
        if self.comment_edit.text() != self.project.comment:
            Project.update({Project.comment: self.comment_edit.text()}).where(Project.id == self.project.id).execute()
        if start_date != datetime.strptime(self.project.start_date.split()[0], '%Y-%m-%d'):
            Project.update({Project.start_date: start_date}).where(Project.id == self.project.id).execute()
        if deadline != datetime.strptime(self.project.deadline.split()[0], '%Y-%m-%d'):
            Project.update({Project.deadline: deadline}).where(Project.id == self.project.id).execute()
        if spend_time_day != self.project.spend_time:
            Project.update({Project.spend_time: spend_time_day}).where(Project.id == self.project.id).execute()
        if self.status_combo.currentText() != self.project.status:
            Project.update({Project.status: self.status_combo.currentText()}).where(Project.id == self.project.id).execute()
        
        self.status = True
        self.close()
        
    
    # Добавление нового проекта при нажатии на кнопку "Добавить"
    #
    # Вызывается на 161 строке
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
        else:
            start_date, deadline_date = self.get_date_from_checkboxes()
            try:
                spend_time_total = int(self.hours_spinbox.text()) / int(self.hours_spinbox_day.text())
            except ZeroDivisionError as e:
                self.error_label.setText('Вы указали неверное количество часов')
                self.error_label.setVisible(True)
                return
            
            spend_time_day = f'{int(spend_time_total)} часов {int((spend_time_total-int(spend_time_total)) * 60)} минут в день'
            
            Project.create(name=self.title_edit.text(),
                           description=self.description_edit.text(),
                           comment=self.comment_edit.text(),
                           start_date=start_date,
                           deadline=deadline_date,
                           spend_time=spend_time_day,
                           status=self.status_combo.currentText(),
                           board_id=self.board
                           )
            self.status = True
            self.close()
    
    
    # Возвращает дату в формате datetime из checkbox для выбора дат
    #
    # Вызывается на 204, 246 строках
    def get_date_from_checkboxes(self):
        day = self.get_checkbox_value(self.start_day_combo)
        month = self.get_checkbox_value(self.start_month_combo)
        year = self.get_checkbox_value(self.start_year_combo)
        
        deadline_day = self.get_checkbox_value(self.deadline_day_combo)
        deadline_month = self.get_checkbox_value(self.deadline_month_combo)
        deadline_year = self.get_checkbox_value(self.deadline_year_combo)

        date_str = f"{day.currentText()}.{month.currentText()}.{year.currentText()}"
        deadline_str = f'{deadline_day.currentText()}.{deadline_month.currentText()}.{deadline_year.currentText()}'
        return datetime.strptime(date_str, "%d.%m.%Y"), datetime.strptime(deadline_str, "%d.%m.%Y")

    
    # Возвращает значение checkbox
    def get_checkbox_value(self, checkbox):
        if checkbox:
            return checkbox
        return ""