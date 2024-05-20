from PyQt5.QtWidgets import (QTabWidget, 
                             QWidget, 
                             QVBoxLayout, 
                             QLabel,
                             QWidget, 
                             QPushButton, 
                             QDesktopWidget, 
                             QHBoxLayout, 
                             QSpacerItem,
                             QMenu,
                             QAction,
                             QLineEdit,
                             QGridLayout,
                             QGraphicsDropShadowEffect,
                             QScrollArea)

from PyQt5.QtCore import Qt, QEvent, QPoint
from PyQt5 import QtGui, QtWidgets

from Frames.ProjectDialog import ProjectDialog
from Frames.ProjectInfo import ProjectWindow
from Frames.Statistic import Statistic
from Frames.Calendar import CalendarWindow

from models.models import *
from stylesheets.style import *

from utlis import config_font


# Основное окно приложения
class Ui_MainWindow(QtWidgets.QMainWindow):
    
    # Инициализатор основного окна (Объявление всех виджетов на основном экране)
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        
        ########
        # Window Work
        
        
        self.setWindowTitle('uTask')
        self.setFixedSize(1280, 720)
        self.setStyleSheet('background-color: rgb(190, 220, 204)')
        
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        
        self.move(x, y)
        
        self.setWindowIcon(QtGui.QIcon('resourses\\assets\\Note.ico'))
        
        # End Window Work
        #########
        
        #########
        # Header Work
        
        self.header = QLabel()
        self.header.setText('uTask')
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setFont(config_font(24))
        self.header.setStyleSheet('color: rgb(70,80,64)')
        
        # End Header Work
        #########
        
        #########
        # Main Tab Widget
        
        self.qTabWidget = QTabWidget()
        self.qTabWidget.setFont(config_font(16))
        self.qTabWidget.setStyleSheet(QTABWIDGET)
        
        self.projects_tab = QWidget()
        self.projects_tab.setStyleSheet('background-color: rgb(190, 220, 204);')
        
        self.calendar_tab = CalendarWindow(Calendar.get_by_id(1))
        self.time_table_tab = CalendarWindow(Calendar.get_by_id(2))
        self.statistic_tab = Statistic()

        self.qTabWidget.addTab(self.projects_tab, 'Проекты')
        self.qTabWidget.addTab(self.calendar_tab, 'Календарь')
        self.qTabWidget.addTab(self.time_table_tab, 'Расписание')
        self.qTabWidget.addTab(self.statistic_tab, 'Статистика')
        
        # End Main Tab Widget
        #########
        
        #########
        # QTabWidget inside MainTabWidget (Проекты)
        self.qTabWidgetInProjects = QTabWidget()
        self.qTabWidgetInProjects.setFont(config_font(16))
        self.qTabWidgetInProjects.setTabPosition(QTabWidget.TabPosition.East)
        self.qTabWidgetInProjects.setTabsClosable(True)
        self.qTabWidgetInProjects.setStyleSheet(QTABWIDGET_IN_PROJECT)
        
        boards = WorkSpace.select()
        if boards:
            for board in boards:
                self.add_tab(board)
        
        self.add_tab_button = QPushButton('+')
        self.add_tab_button.setStyleSheet(ADD_BUTTON)
        
        self.add_tab_button.setFont(config_font(16))
        
        self.add_tab_button.clicked.connect(self.add_tab)
        self.qTabWidgetInProjects.tabBar().installEventFilter(self)
        
        horizonl_layout = QHBoxLayout()

        space_item = QSpacerItem(1200, 21)
        horizonl_layout.addSpacerItem(space_item)
        horizonl_layout.addWidget(self.add_tab_button)
        
        projects_tab_layout = QVBoxLayout(self.projects_tab)
        projects_tab_layout.addWidget(self.qTabWidgetInProjects)
        projects_tab_layout.addLayout(horizonl_layout)
        
        # End QTabWidget inside MainTabWidget (Проекты)
        #########
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header)
        main_layout.addWidget(self.qTabWidget)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        
        self.setCentralWidget(central_widget)
        
    
    # Открывает контекстное меню при клике ПКМ по проекту
    # Вызывается на строках (344, 461)
    def project_context_menu(self, position: QPoint, button: QPushButton, project: Project):
        context_menu = QMenu(self)
        
        remove_action = QAction('Удалить', self)
        remove_action.triggered.connect(lambda: self.project_delete_action(project))
        update_action = QAction('Изменить', self)
        update_action.triggered.connect(lambda: self.project_update_action(project))
        
        context_menu.addAction(remove_action)
        context_menu.addAction(update_action)
        
        context_menu.exec_(button.mapToGlobal(position))
        
    
    # Обработка нажатия на пункт "Изменить" в контекстном меню проекта
    def project_update_action(self, project):
        project_update = ProjectDialog(WorkSpace.select().where(WorkSpace.name == self.qTabWidgetInProjects.tabBar().tabText(self.qTabWidgetInProjects.currentIndex())), True, project)
        project_update.exec()
        if project_update.status:
            self.update_tab(self.qTabWidgetInProjects.currentWidget())
            
    
    # Обработка нажатия на пункт "Удалить" в контекстном меню проекта
    def project_delete_action(self, project: Project):
        Project.delete_by_id(project.id)
        
        remaining_tasks: list[Task] = Task.select().where(Task.project_id == project.id)
        if remaining_tasks.count() != 0:
            for remain in remaining_tasks:
                Task.delete_by_id(remain.id)
        
        self.update_tab(self.qTabWidgetInProjects.currentWidget())
        
    
    # Создание фильтра для вызова контекстного меню вкладки (Панель вкладок справа)
    # Методы: Удалить вкладку;  Изменить название вкладки
    #
    # Задается на 112 строке
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu:
            context_menu = QMenu(self)
            context_menu.setStyleSheet('''
                                       QMenu {
                                           color: white;
                                       }
                                       ''')
            if source == self.qTabWidgetInProjects.tabBar():
                index = self.qTabWidgetInProjects.tabBar().tabAt(event.pos())
                delete_action = context_menu.addAction("Удалить")
                change_name_action = context_menu.addAction('Изменить название')
                delete_action.triggered.connect(lambda: self.close_tab(index))
                change_name_action.triggered.connect(lambda: self.rename_tab(index))
                context_menu.exec_(event.globalPos())
                return True

        return super().eventFilter(source, event)
    
    
    # Изменение названия вкладки
    # Открывает новое окно, где вписывается новое название
    #
    # Вызывается на 190 строке
    def rename_tab(self, index):
        dialog = QLineEdit(self.qTabWidgetInProjects.tabText(index))
        
        dialog.setStyleSheet('''
                             QLineEdit {
                                background-color: rgb(183, 204, 190);
                                border: 1px solid #ccc;
                                padding: 5px;
                            }
                             ''')
        dialog.setFixedWidth(200)
        dialog.setFixedHeight(50)
        
        dialog.setWindowTitle('Изменение названия')
        dialog.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
        dialog.show()
        old_text = self.qTabWidgetInProjects.tabText(index)
        dialog.textChanged.connect(lambda text: self._rename(index, text))
        dialog.returnPressed.connect(lambda: self.close_dialog(dialog, old_text))
    
    
    # Закрытие диалогового окна изменения названия вкладки(При нажатии на Enter(Return))
    #
    # Вызывается на 220 строке
    def close_dialog(self, dialog, old_text):
        update = WorkSpace.update({WorkSpace.name: dialog.text()}).where(WorkSpace.name == old_text)
        update.execute()
        
        dialog.close()
    
    
    # Обновление текста вкладки (После каждого нажатия клавиши на клавиатуре)
    #
    # Вызывается на 219 строке
    def _rename(self, index, text):
        self.qTabWidgetInProjects.setTabText(index, text)
        
        
    # Процесс удаления вкладки
    #
    # Вызывается на 189 строке    
    def close_tab(self, index):
        old_text = self.qTabWidgetInProjects.tabText(index)
        try:
            workspace: WorkSpace = WorkSpace.select().where(WorkSpace.name == old_text).get()
        except Exception:
            return
        id = workspace.id
        WorkSpace.delete().where(WorkSpace.name == old_text).execute()
        remaining_projects: list[Project] = Project.select().where(Project.board_id == id)
        if remaining_projects.count() != 0:
            for remain in remaining_projects:
                self.project_delete_action(remain)
        self.qTabWidgetInProjects.removeTab(index)
        
    
    # Процесс создания новой вкладки (Нажатием на кнопку)
    # Создаются все необходимы виджеты: Хедер с навигационными кнопками и ScrollArea со списком проектов
    #
    # Вызывается на 104 и 111 строках
    # 104 строка - создаются вкладки при открытии приложения (Если они есть в БД)
    # 111 строка - при нажатии на кнопку "+" создается строка со стандартным (неповторяющимся) названием
    def add_tab(self, board_id = None):
        count = self.qTabWidgetInProjects.count()
        
        if board_id:
            board = WorkSpace.get_by_id(board_id)
        else:
            board_name = f'Доска {count + 1}'
            check = list(WorkSpace.select().where(WorkSpace.name.contains(board_name)))
            if check:
                board_name += f'.{len(check) + 1}'
            board = WorkSpace.create(name=board_name)
        
        new_tab = QWidget()
        
        scroll = QScrollArea()
        scroll.setStyleSheet(SCROLLAREA)
        
        vert_layout = QVBoxLayout()
        
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
        
        hori_layout = QHBoxLayout()
        
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
        
        self.add_project_button = QPushButton('Добавить проект')
        self.add_project_button.setFont(config_font(14))
        self.add_project_button.setStyleSheet(IN_TAB_BUTTON)
        self.add_project_button.setGraphicsEffect(shadow_effect2)
        self.add_project_button.clicked.connect(lambda checked, b=board: self.addProject(b, count))
        
        self.sort_button = QPushButton('Сортировка')
        self.sort_button.setFont(config_font(14))
        self.sort_button.setStyleSheet(IN_TAB_BUTTON)
        self.sort_button.setGraphicsEffect(shadow_effect)
        self.sort_menu(board)
        
        space_start = QSpacerItem(150, 20)
        space = QSpacerItem(100, 20)
        
        hori_layout.addSpacerItem(space_start)
        hori_layout.addWidget(search_button)
        hori_layout.addWidget(self.search_line)
        hori_layout.addSpacerItem(space)
        hori_layout.addWidget(self.add_project_button)
        hori_layout.addSpacerItem(space)
        hori_layout.addWidget(self.sort_button)
        hori_layout.addSpacerItem(space_start)
        
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(80)
        
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)
        
        grid_layout.setColumnMinimumWidth(0, 500)
        grid_layout.setColumnMinimumWidth(1, 500)
        
        prs: list[QWidget] = []
        
        projects = Project.select().where(Project.board_id == board)
        for project in projects:
            l = QHBoxLayout()
            
            name = QLabel(project.name)
            deadline = QLabel('.'.join(project.deadline.split()[0].split('-')[1:]))
            
            name.setFont(config_font(14))
            deadline.setFont(config_font(14))
            
            name.setStyleSheet(PROJECT_BUTTON)
            deadline.setStyleSheet(PROJECT_BUTTON)
            
            l.addWidget(name)
            l.addStretch()
            l.addWidget(deadline)
            
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setColor(QtGui.QColor(0, 0, 0, 150))
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 4)
            
            project_button = QPushButton()
            
            project_button.setContextMenuPolicy(Qt.CustomContextMenu)
            project_button.customContextMenuRequested.connect(lambda position, pbutton=project_button, p=project: self.project_context_menu(position, pbutton, p))
            
            project_button.clicked.connect(lambda checked, p=project: self.project_menu(p))
            project_button.setStyleSheet(PROJECT_BUTTON)
            project_button.setGraphicsEffect(shadow)
            project_button.setLayout(l)
            
            prs.append(project_button)
        
        if prs:    
            ind = 0
            for i in range(int(len(prs) / 2 + 0.5)):
                for j in range(2):
                    try:
                        prs[ind].setFixedWidth(400)
                        prs[ind].setFixedHeight(100)
                        grid_layout.addWidget(prs[ind], i, j, Qt.AlignmentFlag.AlignCenter)
                    except IndexError:
                        break
                    ind += 1
        else:
            no_projects_label = QLabel('Проектов пока нет')
            no_projects_label.setFont(config_font(24))
            
            grid_layout.addWidget(no_projects_label, 1, 1, 3, 3, Qt.AlignmentFlag.AlignCenter)
            
        scroll.setWidgetResizable(True)
        scroll.setWidget(QWidget())
        scroll.widget().setLayout(grid_layout)
            
        vert_layout.addLayout(hori_layout)
        vert_layout.addWidget(scroll)
            
        new_tab.setLayout(vert_layout)
        
        
        self.qTabWidgetInProjects.addTab(new_tab, board.name)
    
    
    # При нажатии на кнопку поиск появляется список совпадений по введенному в поле справа
    #~~ Технически эта кнопка бесполезна, так как при вводе текста в поле, леер с проектами обновляется динамически ~~#
    #
    # Вызывается на 315 строке
    def search_click(self, text):
        projects = Project.select().where(Project.name.contains(text))
        
        self.update_tab(self.qTabWidgetInProjects.currentWidget(), projects)
        
    
    # Создается контекстное меню при нажатии на кнопку сортировки (Убывание (по дате), Возрастание (по дате), По названию)
    #
    # Вызывается на 327 строке
    def sort_menu(self, board):
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

        self.action_date_desc.triggered.connect(lambda: self.sort_action_triggered(self.action_date_desc, board))
        self.action_date_asc.triggered.connect(lambda: self.sort_action_triggered(self.action_date_asc, board))
        self.action_name.triggered.connect(lambda: self.sort_action_triggered(self.action_name, board))

        self.sort_button.setMenu(self.menu)


    # Скрипт для сортировки
    #
    # Вызывается на 446, 447, 448 строках
    def sort_action_triggered(self, action, board):
        if action == self.action_date_desc:
            projects = Project.select().where(Project.board_id == board.id).order_by(Project.deadline.desc())
        elif action == self.action_date_asc:
            projects = Project.select().where(Project.board_id == board.id).order_by(Project.deadline.asc())
        elif action == self.action_name:
            projects = Project.select().where(Project.board_id == board.id).order_by(Project.name.asc())
        
        self.update_tab(self.qTabWidgetInProjects.currentWidget(), projects)
            
    
    # Обновление леера с проектами, при каком либо действии, связанном с проектами (Добавление, Поиск, Сортировка)
    #
    # Вызывается на 158, 170, 424, 464, 543 строках
    def update_tab(self, tab_widget: QWidget, projects=None):
        grid_layout = tab_widget.findChild(QGridLayout)

        for i in reversed(range(grid_layout.count())):
            widget = grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        prs: list[QWidget] = []
        
        board = WorkSpace.select().where(WorkSpace.name == self.qTabWidgetInProjects.tabText(self.qTabWidgetInProjects.currentIndex()))
        
        if not projects:
            projects = Project.select().where(Project.board_id == board)
        
        for project in projects:
            l = QHBoxLayout()
            
            name = QLabel(project.name)
            deadline = QLabel('.'.join(project.deadline.split()[0].split('-')[1:]))
            
            name.setFont(config_font(14))
            deadline.setFont(config_font(14))
            
            name.setStyleSheet(PROJECT_BUTTON)
            deadline.setStyleSheet(PROJECT_BUTTON)
            
            l.addWidget(name)
            l.addStretch()
            l.addWidget(deadline)
            
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setColor(QtGui.QColor(0, 0, 0, 150)) 
            shadow.setBlurRadius(10) 
            shadow.setOffset(0, 4)
            
            project_button = QPushButton()
            
            project_button.setContextMenuPolicy(Qt.CustomContextMenu)
            project_button.customContextMenuRequested.connect(lambda position, pbutton=project_button, p=project: self.project_context_menu(position, pbutton, p))
                      
            
            project_button.clicked.connect(lambda checked, p=project: self.project_menu(p))
            project_button.setStyleSheet(PROJECT_BUTTON)
            project_button.setLayout(l)
            project_button.setGraphicsEffect(shadow)
            
            prs.append(project_button)

        if prs:    
            ind = 0
            for i in range(int(len(prs) / 2 + 0.5)):
                for j in range(2):
                    try:
                        prs[ind].setFixedWidth(400)
                        prs[ind].setFixedHeight(100)
                        
                        grid_layout.addWidget(prs[ind], i, j, Qt.AlignmentFlag.AlignCenter)
                    except IndexError:
                        break
                    ind += 1
        else:
            no_projects_label = QLabel('Проектов пока нет')
            no_projects_label.setFont(config_font(24))
            
            grid_layout.addWidget(no_projects_label, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
            
    
    # Открытие меню для добавления нового проекта
    #
    # Вызывается на 321 строке
    def addProject(self, board_id, index):
        pr_dialog = ProjectDialog(board_id)
        pr_dialog.exec()
        if pr_dialog.status:
            self.update_tab(self.qTabWidgetInProjects.widget(index))
            
    
    # Открытие меню с информацие о проекте
    #
    # Вызывается на 380 строке 
    def project_menu(self, project):
        print('Проект: ', project)
        ProjectWindow(project)