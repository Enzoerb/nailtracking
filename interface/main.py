import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import colorchooser

class WebcamApp:
    def __init__(self, window, window_title, image_processor):
        self.image_processor = image_processor
        self.window = window
        self.window.title(window_title)
        
        # OpenCV setup
        self.video_source = 0  # Use the default webcam (you can change this to a video file path if needed)
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)
        
        # Get the dimensions of the video frame
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Tkinter setup
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()

        # Color selection buttons
        colors = {
            "Cyan": "#00FFFF",
            "Red": "#FF0000",
            "Black": "#000000",
            "Aspargus": "#799f63",
            "Lilac": "#C8A2C8"
        }
        
        self.color_btns = []
        for color_name, hex_code in colors.items():
            button = tk.Button(window, text=color_name, width=10, command=lambda h=hex_code: self.set_color(h))
            self.color_btns.append(button)
            button.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.btn_choose_color = tk.Button(window, text="Choose Color", width=12, command=self.choose_color)
        self.btn_choose_color.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.btn_quit = tk.Button(window, text="Quit", width=10, command=self.quit)
        self.btn_quit.pack(pady=10)
       
        self.current_color = "#00FFFF"
 
        # After setting up the Tkinter window, start the webcam capture
        self.update()
        self.window.mainloop()
    
    def quit(self):
        self.window.quit()

    def set_color(self, hex_code):
        self.current_color = hex_code

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Color")
        if color[1] is not None:
            self.current_color = color[1]
    
    def update2(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert the frame from OpenCV's BGR format to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the frame to a PIL image
            image = Image.fromarray(frame)
            # Convert the PIL image to a Tkinter PhotoImage
            self.photo = ImageTk.PhotoImage(image=image)
            # Show the new frame on the canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Call the process_image function on the webcam frame
            processed_frame = self.image_processor(frame)
            
            # Convert the frame from OpenCV's BGR format to RGB format
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            # Draw a rectangle with the selected color
            cv2.rectangle(processed_frame, (50, 50), (200, 200), tuple(int(self.current_color[i:i+2], 16) for i in (1, 3, 5)), -1)
            
            # Convert the frame to a PIL image
            image = Image.fromarray(processed_frame)
            # Convert the PIL image to a Tkinter PhotoImage
            self.photo = ImageTk.PhotoImage(image=image)
            # Show the new frame on the canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

if __name__ == "__main__":
    def mocked_processor(frame):
        return frame

    root = tk.Tk()
    app = WebcamApp(root, "Webcam Capture", mocked_processor)

