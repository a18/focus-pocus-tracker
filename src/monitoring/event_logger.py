# focus-pocus-tracker/src/monitoring/event_logging.py
from datetime import datetime

from pynput import keyboard, mouse

from src.storage.database import FpDatabase


class EventLogger:
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self._mouse_listener = mouse.Listener(on_click=self.on_mouse_click)

    def on_key_press(self, key):
        print(f"Key pressed: {key}")
        timestamp = datetime.now()
        # Put to DB (separate thread)
        db = FpDatabase(db_path=self._db_path)
        db.connect()
        db.insert_log(timestamp, "keyboard", str(key))
        db.close()
        

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")
            timestamp = datetime.now()
            # Put to DB (separate thread)
            db = FpDatabase(db_path=self._db_path)
            db.connect()
            db.insert_log(timestamp, "mouse", f"Clicked at ({x}, {y}) with {button}")
            db.close()

    def start(self):
        self._keyboard_listener.start()
        self._mouse_listener.start()

    def stop(self):
        self._keyboard_listener.stop()
        self._mouse_listener.stop()
