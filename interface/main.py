import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import colorchooser

class WebcamApp:
    def __init__(self, window, window_title, image_processor, model):
        self.image_processor = image_processor
        self.model = model
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

        self.aspect_ratio = self.width / self.height
        self.canvas_width = 800
        self.canvas_height = int(self.canvas_width / self.aspect_ratio)


        # Tkinter setup
        self.canvas = tk.Canvas(window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.RIGHT)

        # Color selection buttons
        colors = {
            "Azul": "#596E7F",
            "Vermelho": "#660B1C",
            "Roxo": "#5400ab",
            "Verde": "#799F63",
            "Lilas": "#baa3bd"
        }
        
        # Create color selection buttons with colored squares
        self.color_btns = []

        btn_size = 20

        for color_name, hex_code in colors.items():
            button_frame = tk.Frame(window)

            color_square = tk.Canvas(button_frame, width=btn_size, height=btn_size, background=hex_code, highlightthickness=0)
            color_square.pack(side=tk.LEFT)

            button = tk.Button(button_frame, text=color_name, width=int(btn_size/2), command=lambda h=hex_code: self.set_color(h))
            button.pack(side=tk.LEFT)

            self.color_btns.append(button_frame)
            button_frame.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=10)

        choose_button_frame = tk.Frame(window)
        self.choose_color_square = tk.Canvas(choose_button_frame, width=btn_size, height=btn_size, background='white', highlightthickness=0)
        self.choose_color_square.pack(side=tk.LEFT)

        # Place the "Choose Color" and "Quit" buttons
        self.btn_choose_color = tk.Button(choose_button_frame, text="Choose Color", width=int(btn_size/2), command=self.choose_color)
        self.btn_choose_color.pack(side=tk.LEFT)
        choose_button_frame.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=10)

        self.btn_quit = tk.Button(window, text="Quit", width=int(btn_size/2), command=self.quit)
        self.btn_quit.pack(side=tk.BOTTOM, anchor=tk.W, padx=5, pady=10)

        self.window.update_idletasks()

        self.current_color = "#799F63"

        # After setting up the Tkinter window, start the webcam capture
        self.update()
        self.window.mainloop()


    def quit(self):
        print('Quitting...')
        self.window.quit()


    def set_color(self, hex_code):
        self.current_color = hex_code


    def choose_color(self):
        color = colorchooser.askcolor(title="Choose Color")
        if color[1] is not None:
            self.set_color(color[1])
            self.choose_color_square.config(background=color[1])
        else:
            self.set_color(None)
            self.choose_color_square.config(background='white')


    def update(self):
        ret, frame = self.vid.read()
        if ret:

            resized_frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))
            # Call the process_image function on the webcam frame
            processed_frame = self.image_processor(resized_frame, self.model, self.current_color)
            
            # Convert the frame from OpenCV's BGR format to RGB format
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            # Draw a rectangle with the selected color
            # cv2.rectangle(processed_frame, (50, 50), (200, 200), tuple(int(self.current_color[i:i+2], 16) for i in (1, 3, 5)), -1)
            
            # Convert the frame to a PIL image
            image = Image.fromarray(processed_frame)
            # Convert the PIL image to a Tkinter PhotoImage
            self.photo = ImageTk.PhotoImage(image=image)
            # Show the new frame on the canvas
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)            
        self.window.after(10, self.update)

if __name__ == "__main__":
    def mocked_processor(frame, model, current_color):
        return frame

    root = tk.Tk()
    app = WebcamApp(root, "Webcam Capture", mocked_processor, None)
