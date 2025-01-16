import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import decoder as d
import encoder as e


class GUI: 
    def __init__(self, root, FLAG_NUMBER):
            self.root = root
            self.root.title("Steganography")
            self.root.geometry("600x600")
            self.FLAG_NUMBER = FLAG_NUMBER

            # Button to select file
            self.upload_button = tk.Button(root, text="Upload image", command=self.upload_image)
            self.upload_button.pack(pady=10)

            # Canvas to display image
            self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
            self.canvas.pack(pady=10)
            self.image_label = tk.Label(root, text="No image uploaded", fg="gray")
            self.image_label.pack()

            #adding image to canvas
            self.default_image_path = "uploadIcon.jpg"
            self.image = Image.open(self.default_image_path)
            self.image.thumbnail((400, 300))
            self.image_display = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(200, 150, image = self.image_display)

            # Text Entry for Encoding
            tk.Label(root, text="Text to Encode:").pack()
            self.text_entry = tk.Entry(root, width=50)
            self.text_entry.pack(pady=10)

            # Buttons for encoding and decoding
            self.encode_button = tk.Button(root, text="Encode", command = self.encode)
            self.encode_button.pack()
            self.decode_button  =tk.Button(root, text = "Decode", command = self.decode)
            self.decode_button.pack(pady=5)
            self.save_button = tk.Button(root, text = "Save Image", command = self.save_image)
            self.save_button.pack(pady=10)

            self.modified_image = None
            self.d = d.Decoder()
            self.e = e.Encoder()

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes = [("Image Files", "*.png")])

        if self.image_path:
            if not self.image_path.endswith(".png"):
                tk.messagebox.showwarning("Error", "Choose a png file")
                return
            else:
                self.image_label.config(text=f"Uploaded: {self.image_path}")
        else:
            self.image_path = self.default_image_path
            self.image_label.config(text="No image uploaded")
            tk.messagebox.showwarning("Error", "No image selected")

        image = Image.open(self.image_path)
        image.thumbnail((400, 300))
        self.image_display = ImageTk.PhotoImage(image)
        self.canvas.create_image(200, 150, image=self.image_display)

    def encode(self):
        if not self.image_path:
            tk.messagebox.showerror("Error", "Please upload an image first")
            return

        text = self.text_entry.get().strip()
        if not text:
            tk.messagebox.showerror("Error", "Please enter some text to encode")
            return

        try:
            self.modified_image = self.e.encode(self.image_path, self.FLAG_NUMBER, text=text)
            tk.messagebox.showinfo("Succes", "Text successfully encoded in the image")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred during encoding:\n{e}")

    def decode(self):
        if not self.image_path:
            tk.messagebox.showerror("Error", "Please upload an image first")
            return

        try:
            hidden_text = self.d.decode(self.image_path, self.FLAG_NUMBER)
            tk.messagebox.showinfo("Decoded Message", f"The hidden message is:\n{hidden_text}")

        except Exception as e:
            tk.messagebox.showerror("Error", f"{e}")

    def save_image(self):
        if not self.modified_image:
            tk.messagebox.showerror("Error", "No modified image to save. Please encode a message first")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if save_path:
            self.modified_image.save(save_path)
            self.modified_image = None
            tk.messagebox.showinfo("Success", f"Image saved at: {save_path}")
        else:
            tk.messagebox.showwarning("Error", "No file path selected")