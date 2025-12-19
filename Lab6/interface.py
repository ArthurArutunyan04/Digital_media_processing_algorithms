import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import os
from tensorflow.keras.models import load_model

model_path_mlp = "MLP_optimized.keras"
model_path_cnn = "CNN.keras"

model = None
model_type = "MLP"
predict = None

if not os.path.exists(model_path_mlp):
    messagebox.showerror("Ошибка", f"Файл модели не найден: {model_path_mlp}")
    exit()

model = load_model(model_path_mlp)
predict = None

def predict_mlp(img):
    img = img.resize((28, 28), Image.LANCZOS).convert('L')
    arr = np.array(img).astype('float32') / 255.0
    arr = arr.reshape(1, 784)
    pred = model.predict(arr, verbose=0)[0]
    digit = int(np.argmax(pred))
    confidence = float(pred[digit])
    return digit, confidence

def predict_cnn(img):
    img = img.resize((28, 28), Image.LANCZOS).convert('L')
    arr = np.array(img).astype('float32') / 255.0
    arr = arr.reshape(1, 28, 28, 1)
    pred = model.predict(arr, verbose=0)[0]
    digit = int(np.argmax(pred))
    confidence = float(pred[digit])
    return digit, confidence

def switch_to_mlp():
    global model, model_type, predict
    try:
        model = load_model(model_path_mlp)
        model_type = "MLP"
        predict = predict_mlp
        status_label.config(text="Текущая модель: MLP", fg="green")
        messagebox.showinfo("Успех", "Переключено на MLP модель")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить MLP:\n{e}")

def switch_to_cnn():
    global model, model_type, predict
    if not os.path.exists(model_path_cnn):
        messagebox.showerror("Ошибка", f"Файл CNN модели не найден:\n{model_path_cnn}")
        return
    try:
        model = load_model(model_path_cnn)
        model_type = "CNN"
        predict = predict_cnn
        status_label.config(text="Текущая модель: CNN", fg="blue")
        messagebox.showinfo("Успех", "Переключено на CNN модель")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить CNN модель:\n{e}")

predict = predict_mlp

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Распознавание цифр")
        self.root.geometry("1000x550")
        self.root.resizable(False, False)

        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        tk.Button(top_frame, text="MLP модель", command=switch_to_mlp, width=15, bg="lightgreen").pack(side=tk.LEFT, padx=10)
        tk.Button(top_frame, text="CNN модель", command=switch_to_cnn, width=15, bg="lightblue").pack(side=tk.LEFT, padx=10)

        global status_label
        status_label = tk.Label(top_frame, text="Текущая модель: MLP", font=("Arial", 10), fg="green")
        status_label.pack(side=tk.LEFT, padx=20)

        self.image = Image.new("L", (280, 280), 0)
        self.draw = ImageDraw.Draw(self.image)
        self.last_x = self.last_y = None

        self.canvas = tk.Canvas(root, width=280, height=280, bg='black')
        self.canvas.pack(pady=10)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Очистить", command=self.clear, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Распознать", command=self.recognize, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Сохранить", command=self.save_image, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Загрузить", command=self.load_image, width=12).pack(side=tk.LEFT, padx=5)

        self.label = tk.Label(root, text="", font=("Arial", 12))
        self.label.pack(pady=20)

    def paint(self, event):
        x, y = event.x, event.y
        r = 10
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, x, y, width=r*2, fill="white", capstyle=tk.ROUND, smooth=True)
            self.draw.line([self.last_x, self.last_y, x, y], fill=255, width=r*2)
        else:
            self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="white", outline="")
            self.draw.ellipse([x-r, y-r, x+r, y+r], fill=255)
        self.last_x, self.last_y = x, y

    def reset(self, _=None):
        self.last_x = self.last_y = None

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (280, 280), 0)
        self.draw = ImageDraw.Draw(self.image)
        self.label.config(text="Холст очищен")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg"), ("BMP files", "*.bmp")]
        )
        if file_path:
            self.image.resize((28, 28), Image.LANCZOS).save(file_path)
            self.label.config(text=f"Сохранено: {os.path.basename(file_path)}")

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                img = Image.open(file_path).convert('L')
                self.image = img.resize((280, 280), Image.LANCZOS)
                self.draw = ImageDraw.Draw(self.image)
                self.render_canvas()
                self.label.config(text="Изображение загружено")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{e}")

    def render_canvas(self):
        self.canvas.delete("all")
        photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def recognize(self):
        digit, conf = predict(self.image)
        self.label.config(text=f"Цифра: {digit}, уверенность: {conf:.2%}")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()