from pynput import keyboard, mouse

class EventLogger:
    def __init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)

    def on_key_press(self, key):
        print(f"Key pressed: {key}")

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            print(f"Mouse clicked at ({x}, {y}) with {button}")

    def start(self):
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

if __name__ == "__main__":
    logger = EventLogger()
    logger.start()
    input("Press Enter to stop logging...")
    logger.stop()
