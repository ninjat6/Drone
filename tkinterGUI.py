import tkinter as tk

class tkinterGUI:
    def window_setup(self):
        try:
            icon = tk.PhotoImage(file='icon.png')
            self.window.iconphoto(False, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")
            
        self.style_fontsize = 12
        self.style_font = "Microsoft JhengHei"
        
    def create_new_window(self):
        new_window = tk.Toplevel(self.window)
        new_window.title("New Window")
        new_window.geometry("400x400")
        return new_window

    def create_listbox(self, window, items):
        # 依項目長度調整寬度
        width = max(len(item) for item in items) + 2 if items else 20
        listbox = tk.Listbox(
            window,
            font=(self.style_font, self.style_fontsize),
            width=width,
            height=len(items)
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for index, item in enumerate(items, start=1):
            listbox.insert(index, item)
        listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

    def on_listbox_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            value = widget.get(selection[0])
            self.on_button_press(value)

    def create_button(self, window, items):
        for button_text in items:
            button = tk.Button(window, 
                            text=button_text, 
                            font=(self.style_font, self.style_fontsize),
                            anchor='w')  # 文字靠左對齊
            button.pack(side=tk.TOP,    # 靠上對齊
                    fill=tk.X,          # 水平方向填滿
                    padx=10,            # 左右邊距
                    pady=5)             # 上下邊距
            button.bind('<ButtonPress>', lambda event, text=button_text: self.on_button_press(text))
