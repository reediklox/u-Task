from PyQt5.QtWidgets import (QScrollArea, 
                             QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QLabel, 
                             QPushButton, 
                             QCalendarWidget, 
                             QSizePolicy)

from PyQt5.QtCore import (Qt, 
                          QDate, 
                          QRectF, 
                          QRect)

from PyQt5.QtGui import QPainter, QColor

from stylesheets.style import *
from models.models import *
from Frames.EventDialog import EventDialog

from utlis import config_font, parse_holidays
from datetime import datetime

class CalendarWidget(QCalendarWidget):
    def __init__(self, event_ids:list[Event]=None, calendar_id = None) -> None:
        super().__init__()
        self.setGridVisible(True)
        self.setStyleSheet(CALENDAR)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setFont(config_font(10))
        
        self.calendar_id = calendar_id
        self.holidays = parse_holidays()
        self.events = event_ids
        
        self.tasks_days = [task.deadline.split()[0] for task in Task.select()]
        self.project_days = [project.deadline.split()[0] for project in Project.select()]
        self.days_list = [event.date.strftime("%Y-%m-%d") for event in self.events]
        
    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        painter.setRenderHint(QPainter.Antialiasing, True)
        
        _date = '{}-{:02}-{:02}'.format(* date.getDate())
        if _date in list(self.holidays.keys()):
            painter.save()
            painter.fillRect(rect, QColor('#9b5f6d'))
            painter.setPen(QColor('black'))        
            painter.drawText(QRectF(rect), Qt.TextSingleLine|Qt.AlignCenter, str(date.day()))
            painter.restore()
            
        elif _date in self.tasks_days and self.calendar_id == Calendar.get_by_id(2):
            color = '#6f5f9b'
            painter.save()
            
            painter.fillRect(rect, QColor(color))
            painter.setPen(QColor('black'))        
            painter.drawText(QRectF(rect), Qt.TextSingleLine|Qt.AlignCenter, str(date.day()))
            painter.restore()
        
        elif _date in self.project_days and self.calendar_id == Calendar.get_by_id(2):
            color = '#aac2cb'
            painter.save()
            
            painter.fillRect(rect, QColor(color))
            painter.setPen(QColor('black'))        
            painter.drawText(QRectF(rect), Qt.TextSingleLine|Qt.AlignCenter, str(date.day()))
            painter.restore()
        
        elif _date in self.days_list:
            painter.save()
            
            event_type = self.events[self.days_list.index(_date)].type
            
            if event_type in ['День рождения', 'Праздник']:
                color = '#c39da0'
            elif event_type == 'Больничный':
                color = '#9b8d5f'
            elif event_type == 'Митинг':
                color = '#8d5f9b'
            elif event_type == 'Задача':
                color = '#6f5f9b'
            else:
                color = '#8b9b5f'
                
            painter.fillRect(rect, QColor(color))
            painter.setPen(QColor('black'))        
            painter.drawText(QRectF(rect), Qt.TextSingleLine|Qt.AlignCenter, str(date.day()))
            painter.restore()
        else:
            QCalendarWidget.paintCell(self, painter, rect, date)
        

class CalendarWindow(QWidget):
    def __init__(self, calendar_id):
        super().__init__()
        
        self.calendar_id: Calendar = calendar_id
        
        main_layout = QHBoxLayout()
        
        layout = QVBoxLayout()
        layout.addSpacing(40)
        self.setStyleSheet('background-color: rgb(255, 255, 255);')
        
        events = self.get_events_list()
        
        self.calendar = CalendarWidget(events, calendar_id)
        
        self.calendar.clicked[QDate].connect(self.show_date_info)
        
        layout.addWidget(self.calendar)
        main_layout.addLayout(layout, stretch=5)
        
        self.right_layout = QVBoxLayout()
        self.right_layout.addSpacing(40)
        self.date_label = QLabel()
        self.date_label.setStyleSheet('background-color: rgb(190, 220, 204)')
        self.date_label.setFont(config_font(14))
        
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.addSpacing(50)
        
        self.date_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.right_layout.addWidget(self.date_label)
        self.right_layout.addLayout(self.scroll_layout)
        
        self.add_event_button = QPushButton('Добавить событие')
        self.add_event_button.setStyleSheet(IN_TAB_BUTTON)
        self.add_event_button.setFont(config_font(12))
        self.add_event_button.clicked.connect(self.add_event)
        
        self.add_event_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.right_layout.addWidget(self.add_event_button)

        main_layout.addLayout(self.right_layout, stretch=2)
        
        self.setLayout(main_layout)


    def show_date_info(self, date: QDate):
        
        for i in reversed(range(self.scroll_layout.count())):
            if self.scroll_layout.itemAt(i).widget():
                self.scroll_layout.itemAt(i).widget().setParent(None)
        
        append_str = ''
        
        _date = '{}-{:02}-{:02}'.format(* date.getDate())
        if _date in list(self.calendar.holidays.keys()) and self.calendar_id == Calendar.get_by_id(1):
            append_str = self.calendar.holidays[_date]
            if '(' in append_str and ')' in append_str:
                append_str = append_str.split('(')[-1].strip(')')
                
        if _date in self.calendar.project_days and self.calendar_id == Calendar.get_by_id(2):
            projects: list[Project] = Project.select().where(Project.deadline.contains(_date))
            for ind, project in enumerate(projects):
                append_str += f'Проект {project.name}'
                append_str += '\n'
                    
        if _date in self.calendar.tasks_days and self.calendar_id == Calendar.get_by_id(2):
            tasks: list[Task] = Task.select().where(Task.deadline.contains(_date))
            for ind, task in enumerate(tasks):
                append_str += f'Задача {task.name}'
                if ind + 1 != len(tasks):
                    append_str += '\n'
        
        self.date_label.setText(date.toString(Qt.DefaultLocaleLongDate) + '\n' + append_str)
        
        selected = self.calendar.selectedDate()
        
        year = selected.year()
        month = selected.month()
        day = selected.day()
        
        
        self.current_date = datetime(year, month, day).date()
    
        events: list[Event] = Event.select().where(Event.calendar_id == self.calendar_id).where(Event.date == self.current_date)
        print(list(events))
        if events:
            self.scroll_area = QScrollArea()
            self.scroll_area.setStyleSheet(SCROLLAREA)
            
            self.scroll_widget = QWidget()
            self.scroll_widget.setStyleSheet('background-color: rgb(190, 220, 204)')
            self.scroll_widget.setObjectName('ScrollWidget')
            
            event_main_layout = QVBoxLayout()
            
            for event in events:
                
                event_layout = QVBoxLayout()
                
                
                name = QLabel(event.name)
                name.setFont(config_font(12))
                name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                etype = QLabel(event.type)
                etype.setFont(config_font(8))
                etype.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                
                event_layout.addWidget(name)
                event_layout.addWidget(etype)
                
                
                desc = QLabel(event.description)
                desc.setMinimumHeight(60)
                desc.setToolTip(desc.text())
                desc.setWordWrap(True)
                desc.setFont(config_font(12))
                desc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                
                event_layout.addWidget(desc)
                
                if self.calendar_id.type == 'Работа':
                    etime = QLabel(event.time)
                    etime.setFont(config_font(12))
                    
                    etime.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    
                    event_layout.addWidget(etime)
                
                event_main_layout.addLayout(event_layout)
                event_main_layout.addSpacing(30)
            
            self.scroll_widget.setLayout(event_main_layout)
            
            self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.scroll_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.scroll_area.setWidget(self.scroll_widget)
            
            self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.scroll_layout.addWidget(self.scroll_area)
            
        
        

    def add_event(self):
        event = EventDialog(calendar_id=self.calendar_id, choosen_date=self.current_date)
        event.exec()
        if event.status:
            self.calendar.repaint(QRect())
        
    def get_events_list(self):
        return list(Event.select().where(Event.calendar_id == self.calendar_id))