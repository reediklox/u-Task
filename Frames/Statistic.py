from PyQt5.QtWidgets import (QWidget,
                             QWidget,
                             QTabWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QLabel)

from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from models.models import *
from stylesheets.style import *

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from utlis import config_font, count_weekends


my_events = [('Митинги', 'Проекты'), ('Больничные', 'Отпуск')]
my_hours = [[0, 0], [0, 0]]

class HistogramWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.htype = None
        self.ax.spines['bottom'].set_color('darkgreen')
        self.ax.spines['top'].set_color('darkgreen')
        self.ax.spines['left'].set_color('darkgreen')
        self.ax.spines['right'].set_color('darkgreen')

    def plot_histogram(self):
        self.ax.clear()
        e = my_events
        h = my_hours
        events = e[0] if self.htype == 'Митинги/Проекты' else e[1]
        hours = h[0]if self.htype == 'Митинги/Проекты' else h[1]
        bars = self.ax.bar(events, hours, linewidth=0, color=[0.3725, 0.6078, 0.5529])
        for bar, hour in zip(bars, hours):
            height = bar.get_height()
            self.ax.annotate(f'{hour} ч' if self.htype == 'Митинги/Проекты' else f'{hour} д', xy=(bar.get_x() + bar.get_width() / 2, height),
                             xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
        self.ax.set_xlabel('События')
        if self.htype == 'Митинги/Проекты':
            self.ax.set_ylabel('Время, часы')
        else:
            self.ax.set_ylabel('Время, дни')
        self.ax.set_title('Гистограмма времени для событий')
        
        self.fig.patch.set_facecolor([0.7451, 0.8627, 0.8])
        self.ax.patch.set_facecolor([0.7451, 0.8627, 0.8])
        self.canvas.draw()

class Statistic(QWidget):
    def __init__(self):
        super().__init__()
        self.current_date = datetime.now()
        self.buff_type = ''

        self.setObjectName('histogramWidget')
        self.setWindowTitle('Статистика событий')
        self.setStyleSheet('background-color: rgb(190, 220, 204);')

        main_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()

        period_widget = QWidget()
        period_layout = QHBoxLayout()
        self.period_label = QLabel('Выберите период:')
        self.period_label.setFont(config_font(14))
        period_layout.addWidget(self.period_label)
        self.period_buttons = [QPushButton(text) for text in ['Неделя', 'Месяц', 'Полгода']]
        for button in self.period_buttons:
            button.setStyleSheet(IN_TAB_BUTTON)
            button.setFont(config_font(10))
            button.clicked.connect(self.handle_period_selection)
            period_layout.addWidget(button)
        period_widget.setLayout(period_layout)

        main_layout.addWidget(period_widget)

        self.histogram_type_widget = QWidget()
        self.histogram_type_layout = QHBoxLayout()
        self.histogram_type_label = QLabel('Выберите тип гистограммы:')
        self.histogram_type_label.setFont(config_font(14))
        self.histogram_type_layout.addWidget(self.histogram_type_label)
        self.histogram_type_buttons = [QPushButton(text) for text in ['Митинги/Проекты', 'Больничный/Отпуск']]
        for button in self.histogram_type_buttons:
            button.setStyleSheet(IN_TAB_BUTTON)
            button.setFont(config_font(10))
            button.clicked.connect(self.handle_histogram_type_selection)
            self.histogram_type_layout.addWidget(button)
        self.histogram_type_widget.setLayout(self.histogram_type_layout)

        main_layout.addWidget(self.histogram_type_widget)

        self.histogram_widget = HistogramWidget()
        self.histogram_widget.hide()  
        
        main_layout.addWidget(self.histogram_widget)

        self.error_label = QLabel('Ошибка')
        self.error_label.setFont(config_font(9))
        self.error_label.setStyleSheet('color: red;')
        self.error_label.setVisible(False)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(self.error_label)
        
        self.setLayout(main_layout)

        self.show()

    def handle_period_selection(self):
        period = self.sender().text()
        self.period_label.setText(f'Выбран период: {period}')
        
        if period == 'Неделя':
            print('неделя')
            self.ago_date = self.current_date - timedelta(weeks=1)
            print(self.ago_date.strftime('%Y-%m-%d'))
        elif period == 'Месяц':
            print('месяц')
            self.ago_date = self.current_date - relativedelta(months=1)
            print(self.ago_date.strftime('%Y-%m-%d'))
        else:
            print('полгода')
            self.ago_date = self.current_date - relativedelta(months=6)
            print(self.ago_date.strftime('%Y-%m-%d'))


        tasks: list[Task] = Task.select()
        self.success_tasks: list[Task] = []
        for task in tasks:
            format = '%Y-%m-%d'
            print(task.project_id.start_date, type(task.project_id.start_date))
            try:
                task_start = datetime.strptime(task.project_id.start_date.split()[0], format)
                if self.ago_date <= task_start <= self.current_date:
                    print(True)
                    self.success_tasks.append(task)
            except Project.DoesNotExist:
                print(f"Task with id {task} or its related project does not exist.")
                
                
        mititngs: list[Event] = Event.select().where(Event.type == 'Митинг')
        self.success_mitings: list[int] = []
        for miting in mititngs:
            if self.ago_date.date() <= miting.date <= self.current_date.date():
                self.success_mitings.append(2)
                
                
        ill_days: list[Event] = Event.select().where(Event.type == 'Больничный')    
        self.success_ill: list[int] = []
        for ill in ill_days:
            print('ill: ', self.ago_date, datetime.combine(ill.date, datetime.min.time()), self.current_date)
            if self.ago_date.date() <= ill.date <= self.current_date.date():
                self.success_ill.append(1)
                
                
        vocation_days: list[Event] = Event.select().where(Event.type == 'Отпуск')
        self.success_vocation: list[int] = []
        for vacation in vocation_days:
            print('vacation: ', self.ago_date.date(), vacation.date, self.current_date.date())
            if self.ago_date.date() <= vacation.date <= self.current_date.date():
                self.success_vocation.append(1)
                    
                    
        if self.error_label.isVisible():
            self.error_label.setVisible(False)
            
        if self.histogram_type_label.text() != 'Выберите тип гистограммы:':
            self.handle_histogram_type_selection()
            

    def handle_histogram_type_selection(self):
        if self.period_label.text() == 'Выберите период:':
            self.error_label.setText('Выберите сначала период!')
            self.error_label.setVisible(True)
            return
        
        self.histogram_type = self.sender().text()
        
        if self.histogram_type not in ('Митинги/Проекты', 'Больничный/Отпуск'):
            self.histogram_type_label.setText(f'Выбран тип гистограммы: {self.buff_type}')
        else:
            self.histogram_type_label.setText(f'Выбран тип гистограммы: {self.histogram_type}')
            self.buff_type = self.histogram_type
        
        self.histogram_widget.htype = self.buff_type
        
        print(self.buff_type)
        if self.buff_type == 'Митинги/Проекты':
            self.all_time = 0
            for success_task in self.success_tasks:
                if datetime.strptime(success_task.deadline.split()[0], '%Y-%m-%d') > datetime.now():
                    hours_per_day = success_task.total_time // count_weekends(datetime.strptime(success_task.project_id.start_date.split()[0], '%Y-%m-%d'), datetime.strptime(success_task.deadline.split()[0], '%Y-%m-%d'))
                    self.all_time += count_weekends(datetime.strptime(success_task.project_id.start_date.split()[0], '%Y-%m-%d'), datetime.now()) * hours_per_day
                else:
                    self.all_time += success_task.total_time
                
                etasks = Event.select().where(Event.type == 'Задача')
                if etasks:
                    for etask in etasks:
                        if self.ago_date <= datetime.combine(etask.date, datetime.min.time()) <= datetime.now():
                            self.all_time += 2

            my_hours[0][1] = self.all_time
            
            if self.success_mitings:
                my_hours[0][0] = sum(self.success_mitings)
            else:
                my_hours[0][0] = 0
        
        else:
            if self.success_ill:
                my_hours[1][0] = sum(self.success_ill)
            else:
                my_hours[1][0] = 0
            if self.success_vocation:
                my_hours[1][1] = sum(self.success_vocation)
            else:
                my_hours[1][1] = 0
        
        self.histogram_widget.plot_histogram()
        self.histogram_widget.show()