import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#  настройки плагинов qt
if hasattr(QtCore, 'QT_VERSION_STR'):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(QtCore.__file__),
        'Qt5',
        'plugins',
        'platforms'
    )


class Ui_WelcomWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("Installation Wizard")
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
            image_path = os.path.join(current_dir, "main.jpg")

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
        self.label = QtWidgets.QLabel("Welcome")
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # label
        self.label_2 = QtWidgets.QLabel(
            "The installation wizard allows you\n"
            "to change how the components are installed\n"
            "on your computer or remove them from your computer.\n"
            "Click Next to continue, or Cancel to exit the Installation Wizard."
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)

        button_layout = QtWidgets.QHBoxLayout()
        self.pushButton = QtWidgets.QPushButton("Next")
        self.pushButton_3 = QtWidgets.QPushButton("Cancel")

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
        return """Политика конфиденциальности для сервиса «Юридический ассистент»

Последнее обновление: 19.10.2025

1. Введение

1.1. Настоящая Политика конфиденциальности (далее – «Политика») описывает, как сервис «Юридический ассистент» (далее – «Сервис», «Мы») собирает, использует, хранит и защищает информацию, полученную от пользователей (далее – «Пользователь», «Вы»).

1.2. Используя Сервис, Вы добровольно и осознанно соглашаетесь на обработку ваших данных, включая потенциально конфиденциальные, в соответствии с условиями настоящей Политики.

2. Какие данные мы обрабатываем

2.1. Загружаемые Документы (Входные данные): Это основной тип данных, который мы обрабатываем. Когда Вы загружаете PDF-файл, мы извлекаем из него текстовую информацию. Этот текст может содержать:
    *   Персональные данные: ФИО, паспортные данные, адреса, ИНН, контактные телефоны, подписи сторон договора.
    *   Конфиденциальная и коммерческая тайна: Условия договоров, финансовые обязательства, коммерческие предложения, иная информация, составляющая тайну.

2.2. Результаты Анализа (Выходные данные): Текст, сгенерированный нашей системой на основе обработки Вашего документа с помощью ИИ (краткое содержание, права и обязанности сторон и т.д.).

2.3. Техническая информация: Для обеспечения функционирования Сервиса мы можем автоматически собирать данные о Вашем сеансе: IP-адрес, тип браузера, время и дата запроса, а также анонимный идентификатор сессии, необходимый для корректной обработки Вашего документа.

3. Цели обработки данных

Мы обрабатываем Ваши данные исключительно для следующих целей:
*   Для предоставления основной функции Сервиса – анализа загруженного Вами документа и генерации упрощенного изложения его содержания.
*   Для обеспечения технической работоспособности и безопасности Сервиса.
*   Для соблюдения требований применимого законодательства.

ВАЖНО: Мы НЕ используем Ваши документы и результаты их анализа для:
*   Обучения или улучшения наших или сторонних AI-моделей без Вашего явного и отдельного согласия.
*   Проведения маркетинговых исследований или таргетированной рекламы.
*   Передачи любым третьим лицам в рекламных или коммерческих целях.

4. Как мы используем и храним данные

4.1. Обработка данных: Текст, извлеченный из Вашего PDF-файла, передается для обработки крупной языковой модели (LLM). Обработка происходит на защищенных серверах.

4.2. Политика хранения – Ключевой принцип:
    *   Загруженные PDF-файлы удаляются с наших серверов сразу после извлечения из них текста.
    *   Извлеченный текст и результаты Анализа автоматически и безвозвратно удаляются с наших серверов в течение 24 часов после завершения обработки Вашего запроса.
    *   Мы не создаем архивных копий Ваших данных и не храним их дольше указанного срока, необходимого исключительно для технической возможности предоставить Вам услугу.

5. Передача данных третьим лицам

5.1. Мы НЕ продаем и НЕ передаем Ваши личные данные, документы или результаты анализа третьим лицам для их маркетинговых или иных коммерческих целей.

5.2. Мы можем передавать извлеченный текст документа для обработки сторонним поставщикам услуг (а именно – провайдерам больших языковых моделей, таких как OpenAI, Yandex GPT и т.д.), которые необходимы для функционирования Сервиса. Такие провайдеры действуют в качестве наших обработчиков данных и обязаны соблюдать конфиденциальность на основании договоров.

5.3. Мы можем раскрыть информацию в случаях, когда это требуется по закону, или для защиты наших прав и безопасности, а также прав и безопасности других пользователей.

6. Безопасность данных

6.1. Мы принимаем разумные технические и организационные меры для защиты Ваших данных от несанкционированного доступа, изменения, раскрытия или уничтожения. Эти меры включают шифрование передаваемых данных и контроль доступа к серверам.

6.2. Несмотря на наши усилия, ни один метод передачи данных через Интернет или метод электронного хранения не является абсолютно безопасным. Мы не можем гарантировать абсолютную безопасность Ваших данных, но обязуемся прилагать все разумные усилия для их защиты.

7. Ваши права

В соответствии с применимым законодательностью Вы имеете право:
*   На доступ к Вашим персональным данным.
*   На исправление или удаление Ваших данных.
*   На отзыв согласия на обработку данных.

Поскольку мы не храним Ваши данные после завершения сеанса (п. 4.2), для реализации этих прав Вам необходимо обратиться к нам в течение срока хранения Ваших данных.

8. Изменения в Политике конфиденциальности

8.1. Мы оставляем за собой право вносить изменения в настоящую Политику. Все изменения вступают в силу с момента их публикации на этой странице с указанием даты последнего обновления.

8.2. Продолжение использования Вами Сервиса после внесения изменений означает Ваше согласие с новой редакцией Политики.

9. Контактная информация

Если у Вас есть любые вопросы или запросы, касающиеся настоящей Политики конфиденциальности или обработки Ваших данных, пожалуйста, свяжитесь с нами по электронной почте: fname.lname@mail.ru."""

    def get_agreement_text(self):
        return """Пользовательское соглашение для сервиса «Юридический ассистент»

1. Общие положения

1.1. Настоящее Пользовательское соглашение (далее – «Соглашение») регулирует отношения между владельцем сервиса «Юридический ассистент» (далее – «Администрация», «Мы») и пользователем (далее – «Пользователь», «Вы») по поводу использования сервиса.

1.2. Сервис «Юридический ассистент» представляет собой программный комплекс, который с использованием технологий искусственного интеллекта (больших языковых моделей, LLM) анализирует загруженные Пользователем документы в формате PDF и предоставляет их краткое, упрощенное изложение, включая идентификацию сторон, их прав и обязанностей (далее – «Анализ»).

1.3. Начиная использование Сервиса (путем загрузки документа), Вы подтверждаете, что полностью ознакомились и согласны со всеми условиями настоящего Соглашения. Если Вы не согласны с каким-либо условием, Вы не имеете права использовать Сервис.

2. Характер услуги и ключевое ограничение

2.1. Сервис НЕ ЯВЛЯЕТСЯ профессиональным юристом или юридической консультацией. Предоставляемый Анализ носит исключительно информационно-справочный, технический характер и представляет собой результат автоматической обработки текста.

2.2. Анализ НЕ СЛЕДУЕТ рассматривать как юридическую консультацию, рекомендацию, заключение или толкование закона. Администрация НЕ ГАРАНТИРУЕТ и НЕ НЕСЕТ ОТВЕТСТВЕННОСТИ за точность, полноту, актуальность или применимость Анализа к Вашей конкретной ситуации.

2.3. Вы обязуетесь НЕ ПРИНИМАТЬ юридически значимых решений (таких как подписание, изменение, оспаривание договора, обращение в суд и т.д.) на основании Анализа, предоставленного Сервисом. Для принятия таких решений Вы должны обратиться к квалифицированному юристу.

3. Условия использования

3.1. Для использования Сервиса регистрация не требуется. Факт загрузки файла является акцептом настоящего Соглашения.

3.2. Вы гарантируете, что:
    *   Достигли возраста, с которого можете заключать подобные соглашения, и являетесь дееспособным.
    *   Обладаете всеми необходимыми правами на загружаемый PDF-документ.
    *   Документ не содержит конфиденциальной информации, которую Вы не имеете права раскрывать, или раскрытие которой может нанести ущерб Вам или третьим лицам.

3.3. Запрещается загружать файлы, содержащие вредоносный код, а также документы, распространение которых запрещено законодательством.

4. Интеллектуальная собственность и обработка данных

4.1. Все права на Сервис, его дизайн, исходный код и технологии принадлежат Администрации.

4.2. Загружая документ, Вы сохраняете все права на него. Одновременно Вы предоставляете Администрации право на обработку текстовой информации из этого документа с помощью LLM исключительно в целях предоставления Вам Анализа.

4.3. Права на сгенерированный Анализ принадлежат Администрации, которая предоставляет Вам неисключительную лицензию на его использование.

4.4. Обработка Ваших данных, включая персональные данные, которые могут содержаться в документах, регулируется [Ссылка на Политику конфиденциальности].

5. Конфиденциальность и безопасность данных

5.1. Мы принимаем коммерчески обоснованные меры для защиты загружаемых документов и сгенерированного Анализа от несанкционированного доступа.

5.2. Политика хранения данных: Загруженные PDF-файлы и результаты их Анализа автоматически удаляются с наших серверов в течение 24 часов после обработки. Мы не храним Ваши документы и их анализ вечно.

5.3. Ни один метод передачи данных через Интернет не является абсолютно безопасным. Используя Сервис, Вы осознаёте и принимаете связанные с этим риски.

6. Ответственность

6.1. Администрация НЕ НЕСЕТ ОТВЕТСТВЕННОСТИ:
    *   За любые убытки, прямые или косвенные, возникшие в результате использования или невозможности использования Сервиса, включая убытки, понесенные из-за принятия Вами решений на основании Анализа.
    *   За содержание и юридические последствия загруженных Вами документов.
    *   За временную недоступность Сервиса, вызванную техническими неполадками или работами по обслуживанию.
    *   За действия третьих лиц, направленные на нарушение безопасности Сервиса.

6.2. Вся ответственность Администрации в любом случае ограничивается суммой в 100 (сто) рублей.

7. Заключительные положения

7.1. Администрация оставляет за собой право в одностороннем порядке изменять настоящее Соглашение. Новая редакция вступает в силу с момента ее публикации. Продолжение использования Сервиса после изменений означает Ваше согласие с новой редакцией.

7.2. Настоящее Соглашение регулируется законодательством Российской Федерации.

7.3. Все споры подлежат разрешению в суде по месту нахождения Администрации.

7.4. Если у Вас есть вопросы относительно настоящего Соглашения, Вы можете связаться с нами по адресу: fname.lname@mail.ru.

Дата последнего обновления: 19.10.2025"""


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

        # список для результатов
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(50, 50, 800, 400))
        self.listView.setObjectName("listView")

        # Кнопка сохранения (перенесена влево)
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

        self.connect_signals()

        self.setup_result_data()

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

    def setup_result_data(self):
        self.result_model = QtGui.QStandardItemModel()
        self.result_ui.listView.setModel(self.result_model)

    def show_welcome_window(self):
        self.hide_all_windows()
        self.welcome_window.show()

    def show_agreement_window(self):
        self.hide_all_windows()
        self.agreement_window.show()

    def show_analysis_window(self):
        self.hide_all_windows()
        self.analysis_window.show()

    def show_result_window(self):
        self.hide_all_windows()
        self.result_window.show()

    def hide_all_windows(self):
        self.welcome_window.hide()
        self.agreement_window.hide()
        self.analysis_window.hide()
        self.result_window.hide()

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

        # Добавляем результаты в result window
        self.result_model.clear()
        results = [
            f"Обработанный файл: {os.path.basename(self.selected_file)}",
            f"Выбранные теги: {', '.join(selected_tags) if selected_tags else 'теги не выбраны'}"
        ]

        for result in results:
            item = QtGui.QStandardItem(result)
            self.result_model.appendRow(item)

        self.show_result_window()

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
                data = []
                for row in range(self.result_model.rowCount()):
                    item = self.result_model.item(row)
                    data.append(item.text())
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(data))
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