import multiprocessing
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pygame import mixer
from PIL import Image, ImageTk
from main import main, Config


if __name__ == '__main__':
    multiprocessing.freeze_support()
    width = 500
    height = 200
    root = Tk()
    root.iconbitmap('favicon.ico')
    root.title("СКАЧАТЬ ВСЕ КАРТИНКИ С ЛУРКА")
    root.geometry(f"{width}x{height}")
    root.resizable(False, False)
    mixer.init()
    mixer.music.load('djeban.mp3')

    mixer.music.play(-1)

    canvas = Canvas(bg="white", width=width, height=height)
    canvas.place(x=0, y=0)
    image = Image.open("bg.png")
    resize_image = image.resize((width, height))
    img = ImageTk.PhotoImage(resize_image)
    canvas.create_image(0, 0, anchor=NW, image=img)

    label = ttk.Label(text=Config.directory_images)
    label.place(x=10, y=50)

    def open_file():
        filepath = filedialog.askdirectory()
        if filepath == '':
            filepath = Config.directory_images
        Config.directory_images = filepath
        label['text'] = filepath

    label_download = ttk.Label(text="Не скачанны")
    label_download.place(x=10, y=80)

    def download_files():
        main(Config.directory_images)
        label_download['text'] = "Скачанны"


    open_button = ttk.Button(text="Выбрать папку для загрузки", command=open_file)
    open_button.place(x=10, y=10)

    start_button = ttk.Button(text="Запустить скачивание изображений", command=download_files)
    start_button.place(x=10, y=110)

    root.mainloop()
