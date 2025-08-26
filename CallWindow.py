from tkinterGUI import tkinterGUI
import tkinter as tk

class CallWindow(tkinterGUI):
    def __init__(self):
        pass

    def failsavemechanism(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title('失效通訊機制')
        self.window.geometry("400x200")
        
        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        label = tk.Label(self.window, text="請先連線無人機", **style)
        label.pack(side=tk.TOP, pady=5)
        
        self.checkbox = tk.BooleanVar()
        
        # 建立核取方塊
        check = tk.Checkbutton(self.window,
                            text="連線成功",
                            command=self.connect_success,
                            variable=self.checkbox,**style)
        check.pack(pady=10)


    def connect_success(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title('連線成功')
        self.window.geometry("400x200")
        
        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        label = tk.Label(self.window, text="請中斷連線", **style)
        label.pack(side=tk.TOP, pady=5)
        
        self.checkbox = tk.BooleanVar()
        
        # 建立核取方塊
        check = tk.Checkbutton(self.window, 
                            text="已中斷連線",
                            command=self.check_mechanism,
                            variable=self.checkbox,**style)
        check.pack(pady=10)
        
    def check_mechanism(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title('檢查失效通訊機制')
        self.window.geometry("400x300")

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        label = tk.Label(self.window, text="請確認通訊失效機制並紀錄於報告內", **style)
        label.pack(side=tk.TOP, pady=5)

        self.back = tk.BooleanVar()
        check = tk.Checkbutton(self.window, 
                            text="返航",
                            variable=self.back,**style)
        check.pack(pady=10)
        self.landing = tk.BooleanVar()
        check = tk.Checkbutton(self.window, 
                            text="迫降",
                            variable=self.landing,**style)
        check.pack(pady=10)
        self.plan = tk.BooleanVar()
        check = tk.Checkbutton(self.window, 
                            text="依原計畫執行",
                            variable=self.plan,**style)
        check.pack(pady=10)

    def malwarescan(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title("惡意程式掃描")
        self.window.geometry("400x200")

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        
        self.label = tk.Label(self.window, text="請使用防毒軟體進行整機掃描，並將結果截圖", **style)
        self.label.pack()
        # 建立核取方塊變數
        self.scan_complete = tk.BooleanVar()
        
        # 建立核取方塊
        check = tk.Checkbutton(self.window, 
                            text="已完成掃描並截圖",
                            variable=self.scan_complete,**style)
        check.pack(pady=10)

    def check_MAS_logo(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title("檢查 MAS Logo")
        self.window.geometry("400x200")

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        
        self.label = tk.Label(self.window, text="請確認APP是否已取得MAS標章", **style)
        self.label.pack()
        # 建立核取方塊變數
        self.logo_correct = tk.BooleanVar()
        
        # 建立核取方塊
        check = tk.Checkbutton(self.window, 
                            text="已取得MAS標章",
                            variable=self.logo_correct,**style)
        check.pack(pady=10)
