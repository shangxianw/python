import tkinter as tk

win = tk.Tk()
win.geometry("400x300")

listbox = tk.Listbox(win)
listbox.place(x=0, y=0)

listbox.insert(tk.END, "aaa")
listbox.insert(tk.END, "bbb")

text = tk.Label(win, text="Hello RUNOOB!")
listbox.insert(tk.END, text)

win.mainloop()