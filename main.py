import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class HomeTheaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Домашний кинотеатр")
        self.root.geometry("800x600")
        self.root.configure(bg='#2E1A47')

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Домашний кинотеатр", font=('Helvetica', 20), bg='#2E1A47', fg='white')
        title_label.pack(pady=10)

        movie_label = tk.Label(self.root, text="Выберите фильм:", font=('Helvetica', 12), bg='#2E1A47', fg='white')
        movie_label.pack(pady=5)

        movies = [
            "C:\\Users\\aidar\\movies\\Паразиты.mp4",
            "C:\\Users\\aidar\\movies\\Побег из шоушенка.mp4",
            "C:\\Users\\aidar\\movies\\Бэтмен.mp4"
        ]

        movie_names = [self.extract_movie_name(path) for path in movies]

        self.movie_combobox = ttk.Combobox(self.root, values=movie_names)
        self.movie_combobox.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(pady=10, expand=True, fill=tk.BOTH)

        control_frame = tk.Frame(self.root, bg='#2E1A47')
        control_frame.pack(pady=10)

        play_button = tk.Button(control_frame, text="Воспроизвести", command=self.start_playback, bg='#654EA3', fg='white')
        play_button.grid(row=0, column=0, padx=5)

        pause_resume_button = tk.Button(control_frame, text="Пауза/Возобновить", command=self.pause_resume_playback, bg='#654EA3', fg='white')
        pause_resume_button.grid(row=0, column=1, padx=5)

        rewind_forward_button = tk.Button(control_frame, text="Перемотать вперед", command=self.rewind_forward, bg='#654EA3', fg='white')
        rewind_forward_button.grid(row=0, column=2, padx=5)

        rewind_backward_button = tk.Button(control_frame, text="Перемотать назад", command=self.rewind_backward, bg='#654EA3', fg='white')
        rewind_backward_button.grid(row=0, column=3, padx=5)

        fullscreen_button = tk.Button(control_frame, text="Полноэкранный режим", command=self.toggle_fullscreen, bg='#654EA3', fg='white')
        fullscreen_button.grid(row=0, column=4, padx=5)

        self.paused = True
        self.cap = None
        self.fullscreen = False

    def extract_movie_name(self, file_path):
        return file_path.split('\\')[-1].split('.')[0]

    def start_playback(self):
        selected_movie_name = self.movie_combobox.get()
        movie_name_to_path = {
            "Паразиты": "C:\\Users\\aidar\\movies\\Паразиты.mp4",
            "Побег из шоушенка": "C:\\Users\\aidar\\movies\\Побег из шоушенка.mp4",
            "Бэтмен": "C:\\Users\\aidar\\movies\\Бэтмен.mp4"
        }
        selected_movie_path = movie_name_to_path.get(selected_movie_name, "")

        self.cap = cv2.VideoCapture(selected_movie_path)

        if not self.cap.isOpened():
            print(f"Не удалось открыть видеофайл: {selected_movie_path}")
            return

        self.playback()

    def playback(self):
        ret, frame = self.cap.read()
        if ret:
            image = ImageTk.PhotoImage(Image.fromarray(cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (1600, 600))))
            self.canvas.config(width=image.width(), height=image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image

            if not self.paused:
                self.root.after(25, self.playback)

    def pause_resume_playback(self):
        self.paused = not self.paused
        if not self.paused:
            self.playback()

    def rewind_forward(self):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_frame = current_frame + 10
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        self.playback()

    def rewind_backward(self):
        current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        new_frame = max(current_frame - 10, 0)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
        self.playback()

    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.root.attributes('-fullscreen', True)
            self.fullscreen = True
        else:
            self.root.attributes('-fullscreen', False)
            self.fullscreen = False


if __name__ == "__main__":
    root = tk.Tk()
    app = HomeTheaterApp(root)
    root.mainloop()
