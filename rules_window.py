import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

# Настройка путей к плагинам Qt
if hasattr(QtCore, 'QT_VERSION_STR'):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(QtCore.__file__),
        'Qt5',
        'plugins',
        'platforms'
    )


class Ui_AgreementWindow(object):
    def setupUi(self, AgreementWindow):
        AgreementWindow.setObjectName("AgreementWindow")
        AgreementWindow.resize(700, 800)
        AgreementWindow.setFixedSize(700, 800)  # Prevent resizing

        self.centralwidget = QtWidgets.QWidget(AgreementWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Tab widget for agreements
        self.tab_widget = QtWidgets.QTabWidget()

        # Privacy Policy Tab
        self.privacy_tab = QtWidgets.QWidget()
        self.privacy_layout = QtWidgets.QVBoxLayout(self.privacy_tab)
        self.privacy_text = QtWidgets.QTextEdit()
        self.privacy_text.setPlainText(self.get_privacy_text())
        self.privacy_text.setReadOnly(True)
        self.privacy_layout.addWidget(self.privacy_text)

        # User Agreement Tab
        self.agreement_tab = QtWidgets.QWidget()
        self.agreement_layout = QtWidgets.QVBoxLayout(self.agreement_tab)
        self.agreement_text = QtWidgets.QTextEdit()
        self.agreement_text.setPlainText(self.get_agreement_text())
        self.agreement_text.setReadOnly(True)
        self.agreement_layout.addWidget(self.agreement_text)

        # Add tabs to tab widget
        self.tab_widget.addTab(self.privacy_tab, "Политика конфиденциальности")
        self.tab_widget.addTab(self.agreement_tab, "Пользовательское соглашение")

        main_layout.addWidget(self.tab_widget)

        # Checkboxes
        self.checkbox_agreement = QtWidgets.QCheckBox('Я согласен с условиями пользовательского соглашения *')
        self.checkbox_privacy = QtWidgets.QCheckBox('Я согласен с условиями политики конфиденциальности *')

        main_layout.addWidget(self.checkbox_agreement)
        main_layout.addWidget(self.checkbox_privacy)

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()  # Push button to the right

        self.accept_btn = QtWidgets.QPushButton("Принять")
        self.cancel_btn = QtWidgets.QPushButton("Отмена")

        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.accept_btn)

        main_layout.addLayout(button_layout)

        AgreementWindow.setCentralWidget(self.centralwidget)

        # Connect signals
        self.retranslateUi(AgreementWindow)
        QtCore.QMetaObject.connectSlotsByName(AgreementWindow)

        # Connect button signals
        self.accept_btn.clicked.connect(self.on_accept)
        self.cancel_btn.clicked.connect(self.on_cancel)

    def retranslateUi(self, AgreementWindow):
        _translate = QtCore.QCoreApplication.translate
        AgreementWindow.setWindowTitle(_translate("AgreementWindow", "Соглашения"))

    def get_privacy_text(self):
        """Return privacy policy text"""
        return ("ТЕКСТ ПОЛИТИКИ КОНФИДЕНЦИАЛЬНОСТИ\n\n")

    def get_agreement_text(self):
        """Return user agreement text"""
        return ("ПОЛЬЗОВАТЕЛЬСКОЕ СОГЛАШЕНИЕ\n\n")

    def on_accept(self):
        """Handle accept button click"""
        if self.checkbox_agreement.isChecked() and self.checkbox_privacy.isChecked():
            QtWidgets.QMessageBox.information(
                None,
                "Успех",
                "Соглашения приняты!"
            )
            # Close the application or proceed to next step
            QtWidgets.QApplication.quit()
        else:
            QtWidgets.QMessageBox.warning(
                None,
                "Внимание",
                "Необходимо принять все условия"
            )

    def on_cancel(self):
        """Handle cancel button click"""
        reply = QtWidgets.QMessageBox.question(
            None,
            'Отмена',
            'Вы уверены, что хотите отменить принятие соглашений?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()


class AgreementWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AgreementWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    try:
        # Create application
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')  # Use Fusion style for consistent look

        # Create and show main window
        window = AgreementWindow()
        window.show()

        # Execute application
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)