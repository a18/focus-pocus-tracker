from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QLabel,
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from src.storage.database import FpDatabase


class MainWindow(QMainWindow):

    STATUS_BAR_UPDATE_SECONDS = 1.0

    def __init__(self, fp_db: FpDatabase):
        super().__init__()
        self._fp_db = fp_db
        self.setWindowTitle("User Activity Supervisor")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Welcome to the User Activity Supervisor")
        layout.addWidget(label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Create a status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Create a timer to update the status bar
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_bar)
        self.timer.start(self.STATUS_BAR_UPDATE_SECONDS * 1000.0)  # Update every N seconds   

    def update_status_bar(self):

        # Execute a query to count the number of records
        query = 'SELECT COUNT(*) FROM activity_logs'
        cursor = self._fp_db.conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]

        # Update the status bar
        self.status_bar.showMessage(f"Records: {count}")
