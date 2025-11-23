from src import parsing
from src.LLM.llm_functions import simple_summary_no_tags, summary_with_tags
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import time

# Настройки плагинов qt
if hasattr(QtCore, 'QT_VERSION_STR'):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(QtCore.__file__),
        'Qt5',
        'plugins',
        'platforms'
    )


def magic_function(file_path, selected_tags):
    res = ""
    extracted_text = parsing.text_extract(file_path)
    selected_tags_string = ""
    if extracted_text == "Ошибка при обработке файла":
        return "Ошибка при обработке файла"
    else:
        all_extracted_text = ""
        for i in range(len(extracted_text)):
            all_extracted_text += extracted_text[i][0]
        simple_summary = simple_summary_no_tags(all_extracted_text)
        res += f"Краткое содержание:\n{simple_summary}\n"
        if selected_tags:
            selected_tags_string = ', '.join(selected_tags)
            for i in range(len(selected_tags)):
                tag_text = summary_with_tags(all_extracted_text, selected_tags[i])
                res += f"Тег {selected_tags[i]}:\n{tag_text}\n"
        return res


class Ui_ProcessingWindow(object):
    def setupUi(self, ProcessingWindow):
        ProcessingWindow.setObjectName("ProcessingWindow")
        ProcessingWindow.resize(400, 200)
        ProcessingWindow.setFixedSize(400, 200)

        self.centralwidget = QtWidgets.QWidget(ProcessingWindow)
        self.centralwidget.setObjectName("centralwidget")

        layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Текст с информацией о процессе
        self.label = QtWidgets.QLabel("Идет процесс суммаризации...")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        layout.addWidget(self.label)

        # Индикатор загрузки
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 0)  # Бесконечная анимация
        layout.addWidget(self.progress_bar)

        ProcessingWindow.setCentralWidget(self.centralwidget)


class Ui_WelcomWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Мастер установки")
        MainWindow.setFixedSize(800, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)

        try:
            # Получаем абсолютный путь к директории скрипта
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # image_path = os.path.join(current_dir, "main_picture.jpg")
            image_path = "main_picture.jpg"

            pixmap = QtGui.QPixmap(image_path)
            if pixmap.isNull():
                raise FileNotFoundError
            self.label_3.setPixmap(pixmap.scaled(300, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        except:
            self.label_3.setStyleSheet("background-color: lightgray; border: 1px solid gray;")
            self.label_3.setFixedSize(300, 500)

        left_layout.addWidget(self.label_3)
        left_widget.setFixedWidth(350)

        # Right side - Content
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        # Welcome label
        self.label = QtWidgets.QLabel("Добро пожаловать")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # label
        self.label_2 = QtWidgets.QLabel(
            "Карманный юридичный помощник\n"
            "Просто загрузите файл — получите\n"
            "краткое описание, без юридических сложностей.\n\n\n\n\n"
            "Нажмите Далее, чтобы продолжить, или Отмена, чтобы выйти из мастера установки."
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        button_layout = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton("Далее")
        self.pushButton_3 = QtWidgets.QPushButton("Отмена")

        button_layout.addStretch()
        button_layout.addWidget(self.pushButton)
        button_layout.addWidget(self.pushButton_3)

        right_layout.addStretch(1)
        right_layout.addWidget(self.label)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.label_2)
        right_layout.addStretch(2)
        right_layout.addLayout(button_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Installation Wizard"))


class Ui_AgreementWindow(object):
    def setupUi(self, AgreementWindow):
        AgreementWindow.setObjectName("AgreementWindow")
        AgreementWindow.resize(700, 800)
        AgreementWindow.setFixedSize(700, 800)

        self.centralwidget = QtWidgets.QWidget(AgreementWindow)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.tab_widget = QtWidgets.QTabWidget()

        # Privacy Policy Tab
        self.privacy_tab = QtWidgets.QWidget()
        self.privacy_layout = QtWidgets.QVBoxLayout(self.privacy_tab)
        self.privacy_text = QtWidgets.QTextEdit()
        self.privacy_text.setPlainText(self.get_privacy_text())
        self.privacy_text.setReadOnly(True)
        self.privacy_layout.addWidget(self.privacy_text)

        self.agreement_tab = QtWidgets.QWidget()
        self.agreement_layout = QtWidgets.QVBoxLayout(self.agreement_tab)
        self.agreement_text = QtWidgets.QTextEdit()
        self.agreement_text.setPlainText(self.get_agreement_text())
        self.agreement_text.setReadOnly(True)
        self.agreement_layout.addWidget(self.agreement_text)

        self.tab_widget.addTab(self.privacy_tab, "Политика конфиденциальности")
        self.tab_widget.addTab(self.agreement_tab, "Пользовательское соглашение")

        main_layout.addWidget(self.tab_widget)

        self.checkbox_agreement = QtWidgets.QCheckBox('Я согласен с условиями пользовательского соглашения')
        self.checkbox_privacy = QtWidgets.QCheckBox('Я согласен с условиями политики конфиденциальности')

        main_layout.addWidget(self.checkbox_agreement)
        main_layout.addWidget(self.checkbox_privacy)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()

        self.back_btn = QtWidgets.QPushButton("Назад")
        self.accept_btn = QtWidgets.QPushButton("Принять")

        button_layout.addWidget(self.back_btn)
        button_layout.addWidget(self.accept_btn)

        main_layout.addLayout(button_layout)

        AgreementWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AgreementWindow)
        QtCore.QMetaObject.connectSlotsByName(AgreementWindow)

    def retranslateUi(self, AgreementWindow):
        _translate = QtCore.QCoreApplication.translate
        AgreementWindow.setWindowTitle(_translate("AgreementWindow", "Соглашения"))

    def get_privacy_text(self):
        privacy_text = ""
        with open("src/docs_for_users/privacy.txt", "r", encoding="utf-8", errors='ignore') as file:
            privacy_text = file.read()
        return privacy_text

    def get_agreement_text(self):
        agreement_text = ""
        with open("src/docs_for_users/agreement.txt", "r", encoding="utf-8", errors='ignore') as file:
            agreement_text = file.read()
        return agreement_text


class Ui_AnalysisWindow(object):
    def setupUi(self, AnalysisWindow):
        AnalysisWindow.setObjectName("AnalysisWindow")
        AnalysisWindow.resize(1142, 613)
        self.centralwidget = QtWidgets.QWidget(AnalysisWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Выбор файла
        self.fileselection_button = QtWidgets.QPushButton(self.centralwidget)
        self.fileselection_button.setGeometry(QtCore.QRect(50, 90, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.fileselection_button.setFont(font)
        self.fileselection_button.setObjectName("fileselection_button")

        self.file_label = QtWidgets.QLabel(self.centralwidget)
        self.file_label.setGeometry(QtCore.QRect(70, 150, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_label.setFont(font)
        self.file_label.setObjectName("file_label")

        # Группа для выбора тегов с чекбоксами
        self.tags_group = QtWidgets.QGroupBox("Выберите теги", self.centralwidget)
        self.tags_group.setGeometry(QtCore.QRect(50, 200, 351, 250))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tags_group.setFont(font)

        self.scroll_area = QtWidgets.QScrollArea(self.tags_group)
        self.scroll_area.setGeometry(QtCore.QRect(10, 30, 331, 210))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameStyle(QtWidgets.QFrame.NoFrame)  # Убираем рамку

        self.tags_widget = QtWidgets.QWidget()
        self.tags_widget.setStyleSheet("background-color: transparent;")  # Прозрачный фон
        self.tags_layout = QtWidgets.QVBoxLayout(self.tags_widget)
        self.tags_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        # Список тегов
        self.tags = [
            "Право", "Расторжение", "Оферта", "Срок", "Аренда", "Гарантия", "Регламент",
            "Срок истечения договора и вступления договора в силу",
            "Соглашение о неразглашении",
            "Перечень персональных данных, предоставленных на обработку",
            "Испытательный срок",
            "Основания расторжения договор",
            "Режим труда и отдыха",
            "Права и обязанности сторон",
            "Материальная ответственность"
        ]
        self.checkboxes = []

        for tag in self.tags:
            checkbox = QtWidgets.QCheckBox(tag)
            checkbox.setFont(font)
            checkbox.setStyleSheet("QCheckBox { background-color: transparent; }")  # Прозрачные чекбоксы
            self.tags_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        self.tags_layout.addStretch()
        self.scroll_area.setWidget(self.tags_widget)

        # добавления тегов
        self.add_tags_button = QtWidgets.QPushButton("Добавить теги", self.centralwidget)
        self.add_tags_button.setGeometry(QtCore.QRect(50, 460, 351, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_tags_button.setFont(font)
        self.add_tags_button.setObjectName("add_tags_button")

        # Список выбранных тегов
        self.tags_list = QtWidgets.QListWidget(self.centralwidget)
        self.tags_list.setGeometry(QtCore.QRect(450, 90, 481, 251))
        self.tags_list.setObjectName("tags_list")

        self.tags_list_label = QtWidgets.QLabel("Выбранные теги:", self.centralwidget)
        self.tags_list_label.setGeometry(QtCore.QRect(450, 60, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tags_list_label.setFont(font)

        # информация обработки
        self.info_button = QtWidgets.QPushButton(self.centralwidget)
        self.info_button.setGeometry(QtCore.QRect(1060, 520, 51, 41))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.info_button.setFont(font)
        self.info_button.setObjectName("info_button")

        # Старт
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(450, 420, 191, 111))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")

        self.back_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_button.setGeometry(QtCore.QRect(50, 520, 100, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.back_button.setFont(font)
        self.back_button.setObjectName("back_button")

        AnalysisWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AnalysisWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1142, 26))
        self.menubar.setObjectName("menubar")
        AnalysisWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AnalysisWindow)
        self.statusbar.setObjectName("statusbar")
        AnalysisWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AnalysisWindow)
        QtCore.QMetaObject.connectSlotsByName(AnalysisWindow)

    def retranslateUi(self, AnalysisWindow):
        _translate = QtCore.QCoreApplication.translate
        AnalysisWindow.setWindowTitle(_translate("AnalysisWindow", "Анализ документов"))
        self.fileselection_button.setText(_translate("AnalysisWindow", "Выбрать файл"))
        self.info_button.setText(_translate("AnalysisWindow", "i"))
        self.start_button.setText(_translate("AnalysisWindow", "Старт"))
        self.back_button.setText(_translate("AnalysisWindow", "Назад"))
        self.file_label.setText(_translate("AnalysisWindow", "Файл не выбран"))
        self.add_tags_button.setText(_translate("AnalysisWindow", "Добавить теги"))


class Ui_ResultWindow(object):
    def setupUi(self, ResultWindow):
        ResultWindow.setObjectName("ResultWindow")
        ResultWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(ResultWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(50, 50, 800, 400))
        self.textEdit.setReadOnly(True)  # Делаем только для чтения
        self.textEdit.setObjectName("textEdit")

        # Устанавливаем перенос слов
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.textEdit.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

        # Кнопка сохранения
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(50, 480, 141, 51))
        self.pushButton.setObjectName("pushButton")

        # Кнопка возврата к обработке файлов
        self.back_to_analysis_button = QtWidgets.QPushButton(self.centralwidget)
        self.back_to_analysis_button.setGeometry(QtCore.QRect(550, 480, 300, 51))
        self.back_to_analysis_button.setObjectName("back_to_analysis_button")

        ResultWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ResultWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 26))
        self.menubar.setObjectName("menubar")
        ResultWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ResultWindow)
        self.statusbar.setObjectName("statusbar")
        ResultWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ResultWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

    def retranslateUi(self, ResultWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "Результаты анализа"))
        self.pushButton.setText(_translate("ResultWindow", "Сохранить как"))
        self.back_to_analysis_button.setText(_translate("ResultWindow", "Вернуться к обработке файлов"))


class ProcessingThread(QtCore.QThread):
    """Поток для выполнения обработки файла"""
    finished_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)

    def __init__(self, file_path, selected_tags):
        super().__init__()
        self.file_path = file_path
        self.selected_tags = selected_tags

    def run(self):
        try:
            result = magic_function(self.file_path, self.selected_tags)
            self.finished_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))


class MainApplication:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setStyle('Fusion')

        self.welcome_window = QtWidgets.QMainWindow()
        self.welcome_ui = Ui_WelcomWindow()
        self.welcome_ui.setupUi(self.welcome_window)

        self.agreement_window = QtWidgets.QMainWindow()
        self.agreement_ui = Ui_AgreementWindow()
        self.agreement_ui.setupUi(self.agreement_window)

        self.analysis_window = QtWidgets.QMainWindow()
        self.analysis_ui = Ui_AnalysisWindow()
        self.analysis_ui.setupUi(self.analysis_window)

        self.result_window = QtWidgets.QMainWindow()
        self.result_ui = Ui_ResultWindow()
        self.result_ui.setupUi(self.result_window)

        # Добавляем окно обработки
        self.processing_window = QtWidgets.QMainWindow()
        self.processing_ui = Ui_ProcessingWindow()
        self.processing_ui.setupUi(self.processing_window)

        self.connect_signals()
        self.setup_result_data()

        # Переменная для хранения потока обработки
        self.processing_thread = None

    def setup_result_data(self):
        pass

    def connect_signals(self):
        self.welcome_ui.pushButton_3.clicked.connect(self.cancel_installation)
        self.welcome_ui.pushButton.clicked.connect(self.show_agreement_window)

        self.agreement_ui.back_btn.clicked.connect(self.show_welcome_window)
        self.agreement_ui.accept_btn.clicked.connect(self.accept_agreements)

        self.analysis_ui.back_button.clicked.connect(self.show_agreement_window)
        self.analysis_ui.fileselection_button.clicked.connect(self.select_file)
        self.analysis_ui.add_tags_button.clicked.connect(self.add_selected_tags)
        self.analysis_ui.start_button.clicked.connect(self.start_processing)
        self.analysis_ui.info_button.clicked.connect(self.show_info)

        self.result_ui.pushButton.clicked.connect(self.save_file)
        self.result_ui.back_to_analysis_button.clicked.connect(self.show_analysis_window)

        self.analysis_ui.start_button.setEnabled(False)
        self.selected_file = None

    def show_welcome_window(self):
        self.hide_all_windows()
        self.welcome_window.show()

    def show_agreement_window(self):
        self.hide_all_windows()
        self.agreement_window.show()

    def show_analysis_window(self):
        self.hide_all_windows()
        self.analysis_window.show()

    def show_processing_window(self):
        self.hide_all_windows()
        self.processing_window.show()

    def show_result_window(self):
        self.hide_all_windows()
        self.result_window.show()

    def hide_all_windows(self):
        self.welcome_window.hide()
        self.agreement_window.hide()
        self.analysis_window.hide()
        self.result_window.hide()
        self.processing_window.hide()

    def cancel_installation(self):
        reply = QtWidgets.QMessageBox.question(
            None,
            'Cancel Installation',
            'Are you sure you want to cancel the installation?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.app.quit()

    def accept_agreements(self):
        if (self.agreement_ui.checkbox_agreement.isChecked() and
                self.agreement_ui.checkbox_privacy.isChecked()):
            self.show_analysis_window()
        else:
            QtWidgets.QMessageBox.warning(
                None,
                "Внимание",
                "Необходимо принять все условия"
            )

    def select_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.analysis_window,
            "Выберите PDF файл",
            "",
            "PDF файлы (*.pdf)"
        )
        if file_path:
            # Проверка расширения файла
            if not file_path.lower().endswith('.pdf'):
                QtWidgets.QMessageBox.warning(
                    self.analysis_window,
                    "Ошибка",
                    "Пожалуйста, выберите файл в формате PDF!"
                )
                return

            self.selected_file = file_path
            file_name = os.path.basename(file_path)
            self.analysis_ui.file_label.setText(f"Выбран: {file_name}")
            self.analysis_ui.start_button.setEnabled(True)

    def add_selected_tags(self):
        selected_tags = []
        for checkbox in self.analysis_ui.checkboxes:
            if checkbox.isChecked():
                selected_tags.append(checkbox.text())

        self.analysis_ui.tags_list.clear()
        for tag in selected_tags:
            self.analysis_ui.tags_list.addItem(tag)

    def start_processing(self):
        if not self.selected_file:
            QtWidgets.QMessageBox.warning(self.analysis_window, "Ошибка", "Сначала выберите файл!")
            return

        selected_tags = [self.analysis_ui.tags_list.item(i).text()
                         for i in range(self.analysis_ui.tags_list.count())]

        # Показываем окно обработки
        self.show_processing_window()

        # Запускаем обработку в отдельном потоке
        self.processing_thread = ProcessingThread(self.selected_file, selected_tags)
        self.processing_thread.finished_signal.connect(self.on_processing_finished)
        self.processing_thread.error_signal.connect(self.on_processing_error)
        self.processing_thread.start()

    def on_processing_finished(self, result):
        # Отображаем результаты
        self.result_ui.textEdit.clear()
        self.result_ui.textEdit.setText(result)
        self.show_result_window()

        # Очищаем поток
        self.processing_thread = None

    def on_processing_error(self, error_msg):
        # Скрываем окно обработки и показываем ошибку
        self.hide_all_windows()
        QtWidgets.QMessageBox.critical(
            self.analysis_window,
            "Ошибка обработки",
            f"Произошла ошибка при обработке файла: {error_msg}"
        )
        self.show_analysis_window()

        # Очищаем поток
        self.processing_thread = None

    def show_info(self):
        QtWidgets.QMessageBox.information(
            self.analysis_window,
            "Правила пользования",
            "Требуется загрузить файл в формате PDF, выбор тегов для обработки необязателен"
        )

    def save_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.result_window,
            "Сохранить файл",
            "",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )
        if file_name:
            try:
                # Получаем текст из QTextEdit
                text_content = self.result_ui.textEdit.toPlainText()
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(text_content)
                QtWidgets.QMessageBox.information(
                    self.result_window,
                    "Успех",
                    f"Файл успешно сохранен: {file_name}"
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self.result_window,
                    "Ошибка",
                    f"Не удалось сохранить файл: {str(e)}"
                )

    def run(self):
        self.welcome_window.show()
        return self.app.exec_()


if __name__ == "__main__":
    try:
        application = MainApplication()
        sys.exit(application.run())
    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)