import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

if hasattr(QtCore, 'QT_VERSION_STR'):
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
        os.path.dirname(QtCore.__file__),
        'Qt5',
        'plugins',
        'platforms'
    )


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Set window properties
        MainWindow.setWindowTitle("Installation Wizard")
        MainWindow.setFixedSize(800, 600)  # Prevent resizing

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Use layouts for better responsiveness
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        # Left side - Image
        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)

        # Load image with proper error handling
        self.load_image()

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

        # Description label
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

        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        self.pushButton_2 = QtWidgets.QPushButton("Back")
        self.pushButton = QtWidgets.QPushButton("Next")
        self.pushButton_3 = QtWidgets.QPushButton("Cancel")

        # Add stretch to push buttons to the right
        button_layout.addStretch()
        button_layout.addWidget(self.pushButton_2)
        button_layout.addWidget(self.pushButton)
        button_layout.addWidget(self.pushButton_3)

        # Add widgets to right layout
        right_layout.addStretch(1)
        right_layout.addWidget(self.label)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.label_2)
        right_layout.addStretch(2)
        right_layout.addLayout(button_layout)

        # Add left and right widgets to main layout
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)

        MainWindow.setCentralWidget(self.centralwidget)

        # Connect signals
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect button signals
        self.pushButton_3.clicked.connect(self.cancel_installation)
        self.pushButton_2.clicked.connect(self.go_back)
        self.pushButton.clicked.connect(self.go_next)

    def load_image(self):
        """Load image with proper error handling and user feedback"""
        image_path = "main.jpg"

        # Check if file exists
        if not os.path.exists(image_path):
            self.show_image_not_found_message()
            return

        # Try to load the image
        pixmap = QtGui.QPixmap(image_path)
        if pixmap.isNull():
            self.show_image_not_found_message()
            return

        # Successfully loaded image
        self.label_3.setPixmap(pixmap.scaled(300, 500, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        print(f"Image '{image_path}' successfully loaded")

    def show_image_not_found_message(self):
        """Show message that image was not found and create placeholder"""
        # Create informative placeholder
        self.label_3.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 2px dashed #cccccc;
                border-radius: 5px;
                color: #666666;
                font-size: 14px;
            }
        """)
        self.label_3.setFixedSize(300, 500)
        self.label_3.setText("Изображение не найдено\n\nmain.jpg")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)

        # Show warning message to user
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Файл не найден")
        msg.setText(f"Изображение 'main.jpg' не найдено.")
        msg.setInformativeText("Пожалуйста, убедитесь, что файл находится в правильной директории.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

        print("Warning: Image 'main.jpg' not found. Using placeholder.")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Installation Wizard"))

    def cancel_installation(self):
        """Handle cancel button click"""
        reply = QtWidgets.QMessageBox.question(
            None,
            'Cancel Installation',
            'Are you sure you want to cancel the installation?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.QApplication.quit()

    def go_back(self):
        """Handle back button click"""
        print("Back button clicked - implement navigation logic")

    def go_next(self):
        """Handle next button click"""
        print("Next button clicked - implement navigation logic")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())