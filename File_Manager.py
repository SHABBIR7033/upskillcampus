import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil


def categorize_extension(extension: str) -> str:
	ext = (extension or "").lower()
	if ext in ("jpg", "jpeg", "png", "gif", "bmp"):
		return "Images"
	if ext in ("pdf", "docx", "doc", "txt", "pptx", "xlsx"):
		return "Documents"
	if ext in ("mp4", "mkv", "avi", "mov"):
		return "Videos"
	if ext in ("mp3", "wav"):
		return "Music"
	if ext in ("exe", "msi"):
		return "Programs"
	if ext in ("zip", "rar", "7z"):
		return "Archives"
	return "no_extension"


def organize(path: str):
	files = os.listdir(path)
	for i in files:
		filename, extension = os.path.splitext(i)
		extension_1 = extension[1:]
		if extension_1 == "jpg" or extension_1 == "jpeg" or extension_1 == "png" or extension_1 == "gif" or extension_1 == "bmp":
			extension_1 = "Images"
		elif extension_1 == "pdf" or extension_1 == "docx" or extension_1 == "doc" or extension_1 == "txt" or extension_1 == "pptx" or extension_1 == "xlsx":
			extension_1 = "Documents"
		elif extension_1 == "mp4" or extension_1 == "mkv" or extension_1 == "avi" or extension_1 == "mov":
			extension_1 = "Videos"
		elif extension_1 == "mp3" or extension_1 == "wav":
			extension_1 = "Music"
		elif extension_1 == "exe" or extension_1 == "msi":
			extension_1 = "Programs"
		elif extension_1 == "zip" or extension_1 == "rar" or extension_1 == "7z":
			extension_1 = "Archives"
		else:
			extension_1 = "no_extension"
		folder_path = os.path.join(path, extension_1)
		if os.path.exists(folder_path):
			shutil.move(os.path.join(path, i), os.path.join(folder_path, i))
		else :
			os.makedirs(folder_path)
			shutil.move(os.path.join(path, i), os.path.join(folder_path, i))


def browse_folder():
	d = filedialog.askdirectory()
	if d:
		path_var.set(d)


def on_organize():
	p = path_var.get().strip()
	if not p:
		messagebox.showerror("Error", "Please enter a path")
		return
	if not os.path.isdir(p):
		messagebox.showerror("Error", "Please enter a valid directory")
		return
	try:
		organize(p)
		messagebox.showinfo("Success", "Files Organized Successfully!")
	except Exception as e:
		messagebox.showerror("Error", f"Failed to organize: {e}")


window = tk.Tk()
window.title("File Manager")
window.geometry("500x140")

path_var = tk.StringVar()

top = tk.Frame(window)
top.pack(fill='x', padx=8, pady=8)
tk.Label(top, text="Path:").pack(side='left')
entry = tk.Entry(top, textvariable=path_var)
entry.pack(side='left', fill='x', expand=True, padx=6)
tk.Button(top, text="Browse", command=browse_folder).pack(side='left')

buttons = tk.Frame(window)
buttons.pack(fill='x', padx=8)
tk.Button(buttons, text="Organize", command=on_organize).pack(side='left', padx=4)
tk.Button(buttons, text="Exit", command=window.destroy).pack(side='right', padx=4)

window.mainloop()