import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter

class PhotoEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Photo Editor")
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Blur", command=self.apply_blur)
        self.edit_menu.add_command(label="Rotate", command=self.rotate_image)
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()

    def open_image(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.image = Image.open(self.file_path)
            self.update_canvas()

    def update_canvas(self):
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.tk_image)

    def save_image(self):
        if hasattr(self, 'file_path') and self.file_path:
            save_file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            self.image.save(save_file_path)
        else:
            messagebox.showwarning("Error", "No image to save")

    def apply_blur(self):
        if hasattr(self, 'image') and self.image:
            self.image = self.image.filter(ImageFilter.BLUR)
            self.update_canvas()
        else:
            messagebox.showwarning("Error", "No image to apply blur")

    def rotate_image(self):
        if hasattr(self, 'image') and self.image:
            self.image = self.image.rotate(90)
            self.update_canvas()
        else:
            messagebox.showwarning("Error", "No image to rotate")

if __name__ == "__main__":
    root = tk.Tk()
    photo_editor = PhotoEditor(root)
    root.mainloop()