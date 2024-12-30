import threading

from config.settings import DATABASE_PATH
from PyQt5.QtWidgets import QApplication
from src.monitoring.event_logger import EventLogger
from src.storage.database import FpDatabase
from src.ui.main_window import MainWindow


def start_event_logging(db_path):
    """
    Function to start the EventLogger and log events into the database.
    Runs in a separate thread to keep the UI responsive.
    """
    db = FpDatabase(db_path)
    db.connect()

    def log_event(event_type, details):
        db.insert_log(event_type, details)

    # Instantiate and customize the event logger
    event_logger = EventLogger()
    
    # Update methods in EventLogger to log events into the database
    original_on_key_press = event_logger.on_key_press
    original_on_mouse_click = event_logger.on_mouse_click

    def on_key_press(key):
        original_on_key_press(key)
        log_event("keyboard", str(key))

    def on_mouse_click(x, y, button, pressed):
        original_on_mouse_click(x, y, button, pressed)
        if pressed:
            log_event("mouse", f"Clicked at ({x}, {y}) with {button}")

    event_logger.on_key_press = on_key_press
    event_logger.on_mouse_click = on_mouse_click

    # Start event logging
    event_logger.start()


def main():
    # Initialize the application
    app = QApplication([])

    # Initialize and display the main UI
    main_window = MainWindow()
    main_window.show()

    # Start the event logger in a separate thread
    event_logger_thread = threading.Thread(
        target=start_event_logging, args=(DATABASE_PATH,), daemon=True
    )
    event_logger_thread.start()

    # Start the event loop
    app.exec_()


if __name__ == "__main__":
    main()




# import sys
# from PyQt5.QtWidgets import QApplication
# from threading import Thread
# import time

# # Import modules from the project structure
# from src.ui.main_window import MainWindow
# from src.monitoring.event_logger import start_mouse_monitor, start_keyboard_monitor
# from src.reporting import generate_report
# from scripts.setup_database import setup_database

# def main():
#     # Initialize the SQLite database
#     setup_database()

#     # Start monitoring in background threads
#     Thread(target=start_mouse_monitor, daemon=True).start()
#     Thread(target=start_keyboard_monitor, daemon=True).start()

#     # Start the PyQt5 GUI application
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()

#     # Example: Generate a report automatically after 10 seconds
#     Thread(target=lambda: (time.sleep(10), generate_report()), daemon=True).start()

#     # Run the application event loop
#     sys.exit(app.exec_())


# if __name__ == "__main__":
#     main()
