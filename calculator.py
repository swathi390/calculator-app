import tkinter as tk
from tkinter import messagebox
import winsound  # For sound on button click (Windows only)


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("It's Ultimate Calculator")
        self.geometry("500x500")
        self.resizable(False, False)

        self.dark_theme = False
        self.history_visible = True
        self.history_data = []

        self.last_key_pressed = None

        self.create_widgets()
        self.configure_theme()

        # Bind keyboard keys
        self.bind("<Key>", self.key_press)
        self.bind("<KeyRelease>", self.key_release)
        self.bind("<Return>", lambda event: self.on_button_click('='))
        self.bind("<BackSpace>", lambda event: self.on_button_click('⌫'))
        self.bind("<Escape>", lambda event: self.on_button_click('C'))

    def create_widgets(self):
        self.entry = tk.Entry(self, font=('Arial', 20), bd=2, relief=tk.RIDGE, justify="right")
        self.entry.pack(padx=10, pady=10, fill=tk.X)

        control_frame = tk.Frame(self)
        control_frame.pack(pady=5)

        self.theme_btn = tk.Button(control_frame, text="🌞 Theme", command=self.toggle_theme)
        self.theme_btn.grid(row=0, column=0, padx=5)

        self.show_history_btn = tk.Button(control_frame, text="Hide History", command=self.toggle_history)
        self.show_history_btn.grid(row=0, column=1, padx=5)

        self.clear_history_btn = tk.Button(control_frame, text="Clear History", command=self.clear_history)
        self.clear_history_btn.grid(row=0, column=2, padx=5)

        button_frame = tk.Frame(self)
        button_frame.pack()

        buttons = [
            ('7', '8', '9', '/', 'C'),
            ('4', '5', '6', '*', '('),
            ('1', '2', '3', '-', ')'),
            ('0', '.', '=', '+', '⌫')
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                action = lambda ch=char: self.on_button_click(ch)
                font_size = 14 if char not in '+-*/' else 18
                b = tk.Button(button_frame, text=char, width=5, height=2, font=('Arial', font_size), command=action)
                b.grid(row=r, column=c, padx=3, pady=3)

        self.history_frame = tk.Frame(self)
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.history_label = tk.Label(self.history_frame, text="History", font=('Arial', 12, 'bold'))
        self.history_label.pack(anchor="w")

        self.history_list = tk.Listbox(self.history_frame, height=5)
        self.history_list.pack(fill=tk.BOTH, expand=True)

    def play_click_sound(self):
        winsound.Beep(1000, 100)

    def on_button_click(self, char):
        if char in '0123456789+-*/().':
            self.play_click_sound()

        if char == 'C':
            self.entry.delete(0, tk.END)
        elif char == '=':
            try:
                expr = self.entry.get()
                result = eval(expr)
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
                self.add_to_history(expr, result)
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
        elif char == '⌫':
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, current[:-1])
        else:
            self.entry.insert(tk.END, char)

    def add_to_history(self, expr, result):
        item = f"{expr} = {result}"
        self.history_data.append(item)
        self.update_history_list()

    def update_history_list(self):
        self.history_list.delete(0, tk.END)
        for item in self.history_data:
            self.history_list.insert(tk.END, item)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.configure_theme()

    def configure_theme(self):
        bg = "#333" if self.dark_theme else "#fff"
        fg = "#fff" if self.dark_theme else "#000"
        btn_bg = "#555" if self.dark_theme else "#ddd"

        self.configure(bg=bg)
        self.entry.configure(bg=bg, fg=fg, insertbackground=fg)

        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=bg)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.configure(bg=btn_bg, fg=fg, activebackground=bg, activeforeground=fg)
                    elif isinstance(child, tk.Label):
                        child.configure(bg=bg, fg=fg)
                    elif isinstance(child, tk.Listbox):
                        child.configure(bg=bg, fg=fg)

        self.theme_btn.config(text="🌚 Theme" if self.dark_theme else "🌞 Theme")

    def toggle_history(self):
        self.history_visible = not self.history_visible
        if self.history_visible:
            self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.show_history_btn.config(text="Hide History")
        else:
            self.history_frame.pack_forget()
            self.show_history_btn.config(text="Show History")

    def clear_history(self):
        self.history_data.clear()
        self.update_history_list()

    def key_press(self, event):
        key = event.char
        if key in "0123456789+-*/().":
            if self.last_key_pressed != key:
                self.play_click_sound()
                self.last_key_pressed = key
        # Characters are automatically added to the entry by Tkinter

    def key_release(self, event):
        self.last_key_pressed = None


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
s