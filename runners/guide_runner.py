import tkinter as tk
from . import Runner

class GuideRunner(Runner):
    """
    Runs test cases that are manual guides for the user.
    """
    def __init__(self, window=None):
        super().__init__(window)

    def _create_guide_window(self, title, geometry="400x200"):
        """Helper to create a consistent modal guide window."""
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title(title)
        self.window.geometry(geometry)
        self.style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        return self.window

    def _clear_window_widgets(self):
        """Clears all widgets from the current window."""
        for widget in self.window.winfo_children():
            widget.destroy()

    def failsavemechanism(self):
        """A multi-step guide for testing failsafe mechanisms."""
        self._create_guide_window('失效通訊機制')
        self._failsafe_step1_connect()
        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()

    def _failsafe_step1_connect(self):
        self._clear_window_widgets()
        self.window.title('步驟1: 連線無人機')
        label = tk.Label(self.window, text="請先連線無人機", **self.style)
        label.pack(side=tk.TOP, pady=5)

        checkbox_var = tk.BooleanVar()
        check = tk.Checkbutton(self.window,
                            text="連線成功",
                            command=self._failsafe_step2_disconnect,
                            variable=checkbox_var, **self.style)
        check.pack(pady=10)

    def _failsafe_step2_disconnect(self):
        self._clear_window_widgets()
        self.window.title('步驟2: 中斷連線')
        label = tk.Label(self.window, text="請中斷無人機連線", **self.style)
        label.pack(side=tk.TOP, pady=5)

        checkbox_var = tk.BooleanVar()
        check = tk.Checkbutton(self.window,
                            text="已中斷連線",
                            command=self._failsafe_step3_verify,
                            variable=checkbox_var, **self.style)
        check.pack(pady=10)

    def _failsafe_step3_verify(self):
        self._clear_window_widgets()
        self.window.title('步驟3: 檢查機制')
        self.window.geometry("400x300")
        label = tk.Label(self.window, text="請確認通訊失效機制並紀錄於報告內", **self.style)
        label.pack(side=tk.TOP, pady=5)

        tk.Checkbutton(self.window, text="返航", variable=tk.BooleanVar(), **self.style).pack(anchor='w', padx=20)
        tk.Checkbutton(self.window, text="迫降", variable=tk.BooleanVar(), **self.style).pack(anchor='w', padx=20)
        tk.Checkbutton(self.window, text="依原計畫執行", variable=tk.BooleanVar(), **self.style).pack(anchor='w', padx=20)

        button_close = tk.Button(self.window, text="完成", command=self.window.destroy, **self.style)
        button_close.pack(pady=10)

    def malwarescan(self):
        win = self._create_guide_window("惡意程式掃描")
        label = tk.Label(win, text="請使用防毒軟體進行整機掃描，並將結果截圖", **self.style)
        label.pack()

        check_var = tk.BooleanVar()
        check = tk.Checkbutton(win, text="已完成掃描並截圖", variable=check_var, **self.style)
        check.pack(pady=10)

        button_close = tk.Button(win, text="完成", command=win.destroy, **self.style)
        button_close.pack(pady=10)

        win.grab_set()
        win.focus_force()
        win.wait_window()

    def check_MAS_logo(self):
        win = self._create_guide_window("檢查 MAS Logo")
        label = tk.Label(win, text="請確認APP是否已取得MAS標章", **self.style)
        label.pack()

        check_var = tk.BooleanVar()
        check = tk.Checkbutton(win, text="已取得MAS標章", variable=check_var, **self.style)
        check.pack(pady=10)

        button_close = tk.Button(win, text="完成", command=win.destroy, **self.style)
        button_close.pack(pady=10)

        win.grab_set()
        win.focus_force()
        win.wait_window()
