# focus-pocus-tracker/main.py
import threading

from config.settings import DATABASE_PATH
from PyQt5.QtWidgets import QApplication
from src.monitoring.event_logger import EventLogger
from src.storage.database import FpDatabase
from src.ui.main_window import MainWindow


def _start_event_logging(db_path: str):
    """
    Function to start the EventLogger and log events into the database.
    Runs in a separate thread to keep the UI responsive.
    """

    # Instantiate event logger and start it
    event_logger = EventLogger(db_path=db_path)
    event_logger.start()


def main():
    """
    Main entry point for the application.
    """

    # Initialize the SQLite database
    db = FpDatabase(DATABASE_PATH)
    try:
        db.connect()

        # Initialize the application
        app = QApplication([])

        # Initialize and display the main UI
        main_window = MainWindow(fp_db=db)
        main_window.show()

        # Start the event logger in a separate thread
        event_logger_thread = threading.Thread(
            target=_start_event_logging, args=(DATABASE_PATH, ), daemon=True
        )
        event_logger_thread.start()

        # Start the event loop (until the application is closed)
        app.exec_()

    finally:
        # Close db connection
        db.close() 


if __name__ == "__main__":
    main()
