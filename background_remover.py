import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
import io
REMOVE_BG_API_KEY = 'A5gNSwRhZm7P1VzNDPL7rXUS' API key

root = tk.Tk()
root.withdraw()

window = tk.Toplevel()
window.title("🪄 Background Remover")
window.geometry("800x600")
window.configure(bg="#f0f8ff")
input_path = None
original_img = None
removed_bg_img = None

IMAGE_SIZE = (300, 300)

title = tk.Label(window, text="Background Remover",
                 font=("Arial", 20, "bold"), bg="#f0f8ff", fg="#333")
title.pack(pady=15)

preview_frame = tk.Frame(window, bg="#f0f8ff")
preview_frame.pack(pady=10)

# Original Image Frame
original_frame = tk.Frame(preview_frame, bg="white",
                          relief="solid", bd=1, width=320, height=340)
original_frame.grid(row=0, column=0, padx=20)
original_frame.pack_propagate(False)

tk.Label(original_frame, text="Original Image",
         font=("Arial", 12), bg="white").pack(pady=5)
original_preview = tk.Label(original_frame, bg="white")
original_preview.pack()

# Output Image Frame
output_frame = tk.Frame(preview_frame, bg="white", 
                        relief="solid", bd=1, width=320, height=340)
output_frame.grid(row=0, column=1, padx=20)
output_frame.pack_propagate(False)

tk.Label(output_frame, text="Image without Background",
         font=("Arial", 12), bg="white").pack(pady=5)
output_preview = tk.Label(output_frame, bg="white")
output_preview.pack()
def open_image():
    global input_path, original_img
    input_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if input_path:
        original_img = Image.open(input_path).resize(IMAGE_SIZE)
        tk_img = ImageTk.PhotoImage(original_img)
        original_preview.config(image=tk_img)
        original_preview.image = tk_img
        remove_btn.config(state="normal")

def remove_background():
    global removed_bg_img
    if not REMOVE_BG_API_KEY or REMOVE_BG_API_KEY == 'YOUR_REMOVE_BG_API_KEY':
        messagebox.showwarning("API Key Missing", "Please set your API key in the code.")
        return

    try:
        with open(input_path, 'rb') as image_file:
            response = requests.post(
                "https://api.remove.bg/v1.0/removebg",
                files={"image_file": image_file},
                data={"size": "auto"},
                headers={"X-Api-Key": REMOVE_BG_API_KEY}
            )

        if response.status_code == requests.codes.ok:
            removed_bg_img = Image.open(io.BytesIO(response.content)).resize(IMAGE_SIZE)
            tk_img = ImageTk.PhotoImage(removed_bg_img)
            output_preview.config(image=tk_img)
            output_preview.image = tk_img
            save_btn.config(state="normal")
        else:
            messagebox.showerror("API Error", response.text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_image():
    if removed_bg_img:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png")])
        if file_path:
            removed_bg_img.save(file_path)
            messagebox.showinfo("Success", f"Image saved at:\n{file_path}")

btn_frame = tk.Frame(window, bg="#f0f8ff")
btn_frame.pack(pady=25)

select_btn = tk.Button(btn_frame, text="📂 Select Image", 
                       font=("Arial", 12), command=open_image, bg="#6fa8dc", fg="white", width=20)
select_btn.grid(row=0, column=0, padx=10)

remove_btn = tk.Button(btn_frame, text="🧼 Remove Background",
                       font=("Arial", 12), command=remove_background, bg="#93c47d", 
                       fg="white", width=20, state="disabled")
remove_btn.grid(row=0, column=1, padx=10)

save_btn = tk.Button(window, text="💾 Save Output Image", font=("Arial", 12), 
                     command=save_image, bg="#f6b26b", fg="white", width=25, state="disabled")
save_btn.pack(pady=10)

window.mainloop()
