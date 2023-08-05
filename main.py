import tkinter as tk
from interface.main import WebcamApp
from src.main import nailTracking

if __name__ == "__main__":
    def mocked_processor(frame):
        return frame

    root = tk.Tk()
    app = WebcamApp(root, "Webcam Capture", nailTracking)

