import tkinter as tk
from interface.main import WebcamApp

if __name__ == "__main__":
    def mocked_processor(frame):
        return frame

    root = tk.Tk()
    app = WebcamApp(root, "Webcam Capture", mocked_processor)

