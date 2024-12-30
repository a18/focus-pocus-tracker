from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Activity Supervisor")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Welcome to the User Activity Supervisor")
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
