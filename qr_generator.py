'''
import segno
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

def generate_qr():
    data = data_entry.get()
    scale = scale_var.get()
    dark = dark_entry.get()
    light = light_entry.get()
    error = error_var.get()
    logo_path = logo_path_var.get() if logo_path_var.get() else None

    # File save dialog with format choices
    filetypes = [
        ("PNG Image", "*.png"),
        ("SVG Vector", "*.svg"),
        ("JPEG Image", "*.jpg"),
        ("BMP Image", "*.bmp"),
        ("All Files", "*.*"),
    ]
    filename = filedialog.asksaveasfilename(
        title="Save QR Code",
        defaultextension=".png",
        filetypes=filetypes,
        initialfile="my_qr"
    )
    if not filename:
        return  # Cancelled

    try:
        ext = filename.split('.')[-1].lower()
        qr = segno.make_qr(data, error=error)
        if ext == "svg":
            qr.save(filename, scale=scale, dark=dark, light=light)
        else:
            temp_file = 'temp_qr.png'
            qr.save(temp_file, scale=scale, dark=dark, light=light)
            if logo_path and ext in ["png", "jpg", "jpeg", "bmp"]:
                qr_img = Image.open(temp_file)
                logo = Image.open(logo_path)
                qr_width, qr_height = qr_img.size
                logo_size = int(qr_width * 0.2)
                logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
                qr_img.save(filename)
            else:
                img = Image.open(temp_file)
                img.save(filename)
        messagebox.showinfo("Success", f"QR code saved as {filename}")
        show_qr(filename)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_logo():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
    logo_path_var.set(path)

def show_qr(path):
    try:
        img = Image.open(path)
        img = img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        qr_label.config(image=img_tk)
        qr_label.image = img_tk
    except Exception:
        qr_label.config(image='')

root = tk.Tk()
root.title("Dynamic QR Code Generator")

tk.Label(root, text="Data/URL:").grid(row=0, column=0, sticky="e")
data_entry = tk.Entry(root, width=40)
data_entry.grid(row=0, column=1, columnspan=2, pady=2)

tk.Label(root, text="Scale:").grid(row=1, column=0, sticky="e")
scale_var = tk.IntVar(value=10)
scale_slider = tk.Scale(root, from_=2, to=20, orient=tk.HORIZONTAL, variable=scale_var)
scale_slider.grid(row=1, column=1, columnspan=2, sticky="we", pady=2)

tk.Label(root, text="Foreground:").grid(row=2, column=0, sticky="e")
dark_entry = tk.Entry(root, width=10)
dark_entry.insert(0, "black")
dark_entry.grid(row=2, column=1, sticky="w", pady=2)

tk.Label(root, text="Background:").grid(row=3, column=0, sticky="e")
light_entry = tk.Entry(root, width=10)
light_entry.insert(0, "white")
light_entry.grid(row=3, column=1, sticky="w", pady=2)

tk.Label(root, text="Error Correction:").grid(row=4, column=0, sticky="e")
error_var = tk.StringVar(value="H")
error_menu = tk.OptionMenu(root, error_var, "L", "M", "Q", "H")
error_menu.grid(row=4, column=1, sticky="w", pady=2)

tk.Label(root, text="Logo (optional):").grid(row=5, column=0, sticky="e")
logo_path_var = tk.StringVar()
logo_entry = tk.Entry(root, textvariable=logo_path_var, width=20)
logo_entry.grid(row=5, column=1, pady=2)
browse_btn = tk.Button(root, text="Browse", command=browse_logo)
browse_btn.grid(row=5, column=2, pady=2)

generate_btn = tk.Button(root, text="Generate QR Code", command=generate_qr)
generate_btn.grid(row=6, column=0, columnspan=3, pady=10)

qr_label = tk.Label(root)
qr_label.grid(row=7, column=0, columnspan=3, pady=10)

root.mainloop()
'''