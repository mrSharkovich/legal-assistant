from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os

if hasattr(QtCore, 'QT_VERSION_STR'):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = (os.path.join(
        os.path.dirname(QtCore.__file__),
        'Qt5',
        'plugins',
        'platforms'
    ))

class MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1142, 613)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # ComboBox для тегов
        self.tags_button = QtWidgets.QComboBox(self.centralwidget)
        self.tags_button.setGeometry(QtCore.QRect(50, 250 , 351, 81))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.tags_button.setFont(font)
        self.tags_button.setObjectName("tags_button")

        # добавление элементов теги
        self.tags_button.addItem("Выберите теги")
        self.tags_button.addItem("Право")
        self.tags_button.addItem("Расторжение")
        self.tags_button.addItem("Оферта")
        self.tags_button.addItem("Срок")
        self.tags_button.addItem("Аренда")
        self.tags_button.addItem("Гарантия")
        self.tags_button.addItem("Регламент")

        # выбор файла
        self.fileselection_button = QtWidgets.QPushButton(self.centralwidget)
        self.fileselection_button.setGeometry(QtCore.QRect(50, 90, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.fileselection_button.setFont(font)
        self.fileselection_button.setObjectName("fileselection_button")

        # Информация обработки файла
        self.info_button = QtWidgets.QPushButton(self.centralwidget)
        self.info_button.setGeometry(QtCore.QRect(1060, 520, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.info_button.setFont(font)
        self.info_button.setObjectName("info_button")

        # список выбранных тегов
        self.tags_list = QtWidgets.QListWidget(self.centralwidget)
        self.tags_list.setGeometry(QtCore.QRect(590, 90, 481, 251))
        self.tags_list.setObjectName("tags_list")

        # старт
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(430, 420, 191, 111))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")

        #
        self.file_label = QtWidgets.QLabel(self.centralwidget)
        self.file_label.setGeometry(QtCore.QRect(70, 150, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_label.setFont(font)
        self.file_label.setObjectName("file_label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1142, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow) # установка заголовков
        QtCore.QMetaObject.connectSlotsByName(MainWindow) # подключение сигналов к слотам

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Анализ документов"))
        self.fileselection_button.setText(_translate("MainWindow", "Выбрать файл"))
        self.info_button.setText(_translate("MainWindow", "i"))
        self.start_button.setText(_translate("MainWindow", "Старт"))
        self.file_label.setText(_translate("MainWindow", "Файл не выбран"))


class MainApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)

        # Подключаем обработчики событий
        self.ui.fileselection_button.clicked.connect(self.select_file)
        self.ui.tags_button.currentTextChanged.connect(self.add_tag)
        self.ui.start_button.clicked.connect(self.start_processing)
        self.ui.info_button.clicked.connect(self.show_info)

        # Блокировка старта пока не выбран файл
        self.ui.start_button.setEnabled(False)
        self.selected_file = None

    def select_file(self):
        # Выбор файла для анализа
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Все файлы (*);;Текстовые файлы (*.txt);;Документы (*.doc *.docx);;PDF (*.pdf)"
        )

        if file_path:
            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.ui.file_label.setText(f"Выбран: {file_name}")
            self.ui.start_button.setEnabled(True)

    def add_tag(self, tag):
        # Добавление тега в список
        if tag != "Выберите теги":
            # Проверяем, нет ли уже такого тега в списке
            existing_items = [self.ui.tags_list.item(i).text() for i in range(self.ui.tags_list.count())]
            if tag not in existing_items:
                self.ui.tags_list.addItem(tag)

    def start_processing(self):
        # Запуск обработки
        if not self.selected_file:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала выберите файл!")
            return

        selected_tags = [self.ui.tags_list.item(i).text() for i in range(self.ui.tags_list.count())]

        if not selected_tags:
            QtWidgets.QMessageBox.information(
                self, "Информация","Выбранных тегов нет! Файл будет обработан без тегов.")

        QtWidgets.QMessageBox.information(
            self,
            "Обработка",
            f"Файл: {os.path.basename(self.selected_file)}\n"
            f"Теги: {', '.join(selected_tags) if selected_tags else 'выбранных тегов нет'}"
        )

    def show_info(self):
        QtWidgets.QMessageBox.information(
            self,
            "Информация",
            "Объяснение логики обработки файла для пользователя"
        )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()
    sys.exit(app.exec_())