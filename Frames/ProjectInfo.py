from PyQt5.QtWidgets import (QMenu, 
                             QAction,
                             QLineEdit,
                             QPushButton,
                             QGraphicsDropShadowEffect,
                             QSpacerItem,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLabel,
                             QScrollArea,
                             QGridLayout,
                             QDesktopWidget)

from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtGui

from models.models import *
from stylesheets.style import *

from Frames.TaskDialog import TasksDialog

from utlis import config_font


class ProjectWindow(QWidget):
    def __init__(self, project):
        super().__init__()
        self.project: Project = project
        self.init_ui()
        

    def init_ui(self):
        self.setFixedSize(980, 720)
        self.setStyleSheet('background-color: rgb(190, 220, 204)')
        
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        
        self.move(x, y)
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        project_name_label = QLabel(self.project.name)
        project_name_label.setFont(config_font(24))
        header_layout.addWidget(project_name_label)

        description_layout = QVBoxLayout()

        desc_layout = QVBoxLayout()
        description_label = QLabel('Описание: ')
        description_label.setFont(config_font(12))
        description_text = QLabel(self.project.description)
        description_txt = '<br>'.join([description_text.text()[i:i+25] for i in range(0, len(description_text.text()), 25)])
        description_text.setToolTip(description_txt)
        description_text.setWordWrap(True)
        description_text.setMaximumWidth(150)
        description_text.setMaximumWidth(100)
        description_text.setFont(config_font(10))
        desc_layout.addWidget(description_label)
        desc_layout.addWidget(description_text)
        description_layout.addLayout(desc_layout)

        comment_layout = QVBoxLayout()
        comment_label = QLabel('Комментарий к проекту: ')
        comment_text = QLabel(self.project.comment)
        comment_txt = '<br>'.join([comment_text.text()[i:i+25] for i in range(0, len(comment_text.text()), 25)])
        comment_text.setToolTip(comment_txt)
        comment_text.setWordWrap(True)
        comment_text.setMaximumWidth(150)
        comment_text.setMaximumWidth(100)
        comment_text.setFont(config_font(10))
        comment_label.setFont(config_font(12))
        
        comment_layout.addWidget(comment_label)
        comment_layout.addWidget(comment_text)
        description_layout.addLayout(comment_layout)

        date_layout = QVBoxLayout()

        start_date_layout = QHBoxLayout()
        start_date_label = QLabel('Дата начала:')
        start_date = QLabel(self.project.start_date.split()[0])
        
        start_date.setFont(config_font(12))
        start_date_label.setFont(config_font(12))
        
        start_date_layout.addWidget(start_date_label)
        start_date_layout.addWidget(start_date)
        date_layout.addLayout(start_date_layout)

        
        deadline_layout = QHBoxLayout()
        deadline_label = QLabel('Дедлайн:')
        deadline_text = QLabel(self.project.deadline.split()[0])
        
        deadline_text.setFont(config_font(12))
        deadline_label.setFont(config_font(12))
        
        deadline_layout.addWidget(deadline_label)
        deadline_layout.addWidget(deadline_text)
        date_layout.addLayout(deadline_layout)

        time_layout = QHBoxLayout()
        time_label = QLabel('Времени в день:')
        time = QLabel(' '.join(self.project.spend_time.split()[:-2]))
        
        time.setFont(config_font(12))
        time_label.setFont(config_font(12))
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(time)
        description_layout.addLayout(time_layout)

        header_layout.addLayout(description_layout)

        header_layout.addSpacing(60)
        header_layout.addLayout(date_layout)

        main_layout.addLayout(header_layout)

        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(SCROLLAREA)

        self.tasks_layout = QGridLayout()
        self.tasks_layout.setSpacing(80)
        
        self.tasks_layout.setColumnStretch(0, 1)
        self.tasks_layout.setColumnStretch(1, 1)
        self.tasks_layout.setColumnStretch(2, 1)
        
        self.tasks_layout.setColumnMinimumWidth(0, 250)
        self.tasks_layout.setColumnMinimumWidth(1, 250)
        self.tasks_layout.setColumnMinimumWidth(2, 250)
        
        tasks: list[QWidget] = []
        
        db_tasks = Task.select().where(Task.project_id == self.project)
        for task in db_tasks:
            l = QVBoxLayout()
            
            name = QLabel(task.name)
            deadline = QLabel('.'.join(task.deadline.split()[0].split('-')[1:]))
            deadline.setToolTip(task.deadline)
            description = QLabel(task.description)
            description_txt = '<br>'.join([description.text()[i:i+25] for i in range(0, len(description.text()), 25)])
            print(description_txt)
            description.setWordWrap(True)
            description.setMaximumWidth(80)
            description.setToolTip(description_txt)
            total_time = QLabel(str(task.total_time) + ' часов')
            
            name.setFont(config_font(14))
            deadline.setFont(config_font(14))
            description.setFont(config_font(10))
            total_time.setFont(config_font(14))
            
            name.setStyleSheet(PROJECT_BUTTON)
            deadline.setStyleSheet(PROJECT_BUTTON)
            description.setStyleSheet(PROJECT_BUTTON)
            total_time.setStyleSheet(PROJECT_BUTTON)
            
            l.addWidget(name)
            l.addSpacing(40)
            l.addWidget(description)
            l.addSpacing(80)
            l.addWidget(total_time)
            l.addSpacing(10)
            l.addWidget(deadline)
            
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setColor(QtGui.QColor(0, 0, 0, 150))
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 4)
            
            project_button = QPushButton()
            
            project_button.setContextMenuPolicy(Qt.CustomContextMenu)
            project_button.customContextMenuRequested.connect(lambda position, pbutton=project_button, t=task: self.task_context_menu(position, pbutton, t))
            
            project_button.setStyleSheet(PROJECT_BUTTON)
            project_button.setGraphicsEffect(shadow)
            project_button.setLayout(l)
    
            tasks.append(project_button)
        
        if tasks:    
            ind = 0
            for i in range(int(len(tasks) / 2 + 0.5)):
                for j in range(3):
                    try:
                        tasks[ind].setFixedWidth(150)
                        tasks[ind].setFixedHeight(300)
                        self.tasks_layout.addWidget(tasks[ind], i, j, Qt.AlignmentFlag.AlignCenter)
                    except IndexError:
                        break
                    ind += 1
        else:
            print('Проектов нет')
            no_tasks_label = QLabel('Задач пока нет')
            no_tasks_label.setFont(config_font(24))
            
            self.tasks_layout.addWidget(no_tasks_label)

        scroll_widget = QWidget()
        scroll_widget.setLayout(self.tasks_layout)
        scroll_area.setWidget(scroll_widget)
        
        hori_layout = QHBoxLayout()
        
        shadow_effect1 = QGraphicsDropShadowEffect(self)
        shadow_effect1.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_effect1.setBlurRadius(10)
        shadow_effect1.setOffset(0, 4)
        
        shadow_effect2 = QGraphicsDropShadowEffect(self)
        shadow_effect2.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_effect2.setBlurRadius(10)
        shadow_effect2.setOffset(0, 4)
        
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_effect.setBlurRadius(10) 
        shadow_effect.setOffset(0, 4)
        
        shadow_effectl = QGraphicsDropShadowEffect(self)
        shadow_effectl.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_effectl.setBlurRadius(10) 
        shadow_effectl.setOffset(0, 4)
        
        search_button = QPushButton('Поиск')
        search_button.setFont(config_font(14))
        search_button.setIcon(QtGui.QIcon('resourses\\assets\\icons8-поиск-50.png'))
        search_button.setStyleSheet(IN_TAB_BUTTON)
        search_button.setGraphicsEffect(shadow_effect1)
        
        self.search_line = QLineEdit()
        self.search_line.setFont(config_font(14))
        self.search_line.setStyleSheet(IN_TAB_LINE)
        self.search_line.setGraphicsEffect(shadow_effectl)
        self.search_line.textChanged.connect(self.search_click)
        
        self.add_task_button = QPushButton('Добавить задачу')
        self.add_task_button.setFont(config_font(14))
        self.add_task_button.setStyleSheet(IN_TAB_BUTTON)
        self.add_task_button.setGraphicsEffect(shadow_effect2)
        self.add_task_button.clicked.connect(self.addTask)
        
        self.sort_button = QPushButton('Сортировка')
        self.sort_button.setFont(config_font(14))
        self.sort_button.setStyleSheet(IN_TAB_BUTTON)
        self.sort_button.setGraphicsEffect(shadow_effect)
        self.sort_menu()
        
        space_start = QSpacerItem(100, 20)
        space = QSpacerItem(50, 20)
        
        hori_layout.addSpacerItem(space_start)
        hori_layout.addWidget(search_button)
        hori_layout.addWidget(self.search_line)
        hori_layout.addSpacerItem(space)
        hori_layout.addWidget(self.add_task_button)
        hori_layout.addSpacerItem(space)
        hori_layout.addWidget(self.sort_button)
        hori_layout.addSpacerItem(space_start)
        main_layout.addSpacerItem(QSpacerItem(10, 50))

        main_layout.addLayout(hori_layout)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        self.setWindowTitle('Проект')
        self.show()    
    
    
    def task_context_menu(self, position: QPoint, button: QPushButton, task: Task):
        context_menu = QMenu(self)
        
        remove_action = QAction('Удалить', self)
        remove_action.triggered.connect(lambda: self.task_delete_action(task))
        update_action = QAction('Изменить', self)
        update_action.triggered.connect(lambda: self.task_update_action(task))
        
        context_menu.addAction(remove_action)
        context_menu.addAction(update_action)
        
        context_menu.exec_(button.mapToGlobal(position))
        
    def task_update_action(self, task: Task):
        tasks_update = TasksDialog(self.project, True, task)
        tasks_update.exec()
        if tasks_update.status:
            self.update_window()
        
    def task_delete_action(self, task: Task):
        Task.delete_by_id(task.id)
        self.update_window()
    
    def sort_menu(self):
        self.menu = QMenu(self.sort_button)

        self.action_date_desc = QAction('По дате (Убывание)', self)
        self.action_date_desc.setFont(config_font(10))
        self.action_date_asc = QAction('По дате (Возрастание)', self)
        self.action_date_asc.setFont(config_font(10))
        self.action_name = QAction('По названию', self)
        self.action_name.setFont(config_font(10))

        self.menu.addAction(self.action_date_desc)
        self.menu.addAction(self.action_date_asc)
        self.menu.addAction(self.action_name)

        self.menu.setStyleSheet(COMBO_MENU)

        self.action_date_desc.triggered.connect(lambda: self.sort_action_triggered(self.action_date_desc))
        self.action_date_asc.triggered.connect(lambda: self.sort_action_triggered(self.action_date_asc))
        self.action_name.triggered.connect(lambda: self.sort_action_triggered(self.action_name))

        self.sort_button.setMenu(self.menu)


    def sort_action_triggered(self, action):
        if action == self.action_date_desc:
            tasks = Task.select().where(Task.project_id == self.project.id).order_by(Task.deadline.desc())
        elif action == self.action_date_asc:
            tasks = Task.select().where(Task.project_id == self.project.id).order_by(Task.deadline.asc())
        elif action == self.action_name:
            tasks = Task.select().where(Task.project_id == self.project.id).order_by(Task.name.asc())
        
        self.update_window(tasks)
            
    
    
    def search_click(self, text):
        tasks = Task.select().where(Task.name.contains(text))
        self.update_window(tasks)
    
    
    def addTask(self):
        task_dialog = TasksDialog(self.project)
        task_dialog.exec()
        if task_dialog.status:
            self.update_window()
    
        
    def update_window(self, tasks=None):
        
        for i in reversed(range(self.tasks_layout.count())):
            widget = self.tasks_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        tsks: list[QWidget] = []
        if not tasks:
            tasks = Task.select().where(Task.project_id == self.project)
            
        for task in tasks:
            l = QVBoxLayout()
            
            name = QLabel(task.name)
            deadline = QLabel('.'.join(task.deadline.split()[0].split('-')[1:]))
            deadline.setToolTip(task.deadline)
            description = QLabel(task.description)
            description_txt = '<br>'.join([description.text()[i:i+25] for i in range(0, len(description.text()), 25)])
            print(description_txt)
            description.setWordWrap(True)
            description.setMaximumWidth(80)
            description.setToolTip(description_txt)
            total_time = QLabel(str(task.total_time) + ' часов')
            
            name.setFont(config_font(14))
            deadline.setFont(config_font(14))
            description.setFont(config_font(10))
            total_time.setFont(config_font(14))
            
            name.setStyleSheet(PROJECT_BUTTON)
            deadline.setStyleSheet(PROJECT_BUTTON)
            description.setStyleSheet(PROJECT_BUTTON)
            total_time.setStyleSheet(PROJECT_BUTTON)
            
            l.addWidget(name)
            l.addSpacing(40)
            l.addWidget(description)
            l.addSpacing(80)
            l.addWidget(total_time)
            l.addSpacing(10)
            l.addWidget(deadline)
            
            l.setAlignment(Qt.AlignmentFlag.AlignCenter)
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setColor(QtGui.QColor(0, 0, 0, 150)) 
            shadow.setBlurRadius(10) 
            shadow.setOffset(0, 4)
            
            project_button = QPushButton()
            
            project_button.setContextMenuPolicy(Qt.CustomContextMenu)
            project_button.customContextMenuRequested.connect(lambda position, pbutton=project_button, t=task: self.task_context_menu(position, pbutton, t))
                     
            
            project_button.setStyleSheet(PROJECT_BUTTON)
            project_button.setGraphicsEffect(shadow)
            project_button.setLayout(l)
    
            tsks.append(project_button)
        
        if tsks:    
            ind = 0
            for i in range(int(len(tsks) / 2 + 0.5)):
                for j in range(3):
                    try:
                        tsks[ind].setFixedWidth(150)
                        tsks[ind].setFixedHeight(300)
                        self.tasks_layout.addWidget(tsks[ind], i, j, Qt.AlignmentFlag.AlignCenter)
                    except IndexError:
                        break
                    ind += 1
        else:
            print('Проектов нет')
            no_tasks_label = QLabel('Задач пока нет')
            no_tasks_label.setFont(config_font(24))
            
            self.tasks_layout.addWidget(no_tasks_label)