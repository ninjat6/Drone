import tkinter as tk
from tkinterGUI import tkinterGUI
from TestCaseGUI import TestCaseGUI

class AutoScriptGUI(tkinterGUI):
    
    def __init__(self):
        self.window = tk.Tk()
        self.window_setup()
        self.window.title("遙控無人機資安檢測工具包")
        
        test_chapter = ['6 遙控無人機資安檢測-安全要求', '8.1 遙控無人機資安檢測增項測試-一般安全要求', '8.2 遙控無人機資安檢測增項測試-特殊安全要求']
        # 計算最長文字的像素寬度
        temp_label = tk.Label(self.window, text=max(test_chapter, key=len), font=(self.style_font, self.style_fontsize))
        temp_label.pack()
        max_width = temp_label.winfo_reqwidth()
        temp_label.destroy()
        
        # 設定視窗寬度（加上左右邊距）
        width = max_width + 40  # 左右各預留20像素邊距
        height = 400
        
        # 計算視窗位置使其置中
        screen_width = int(self.window.winfo_screenwidth())
        screen_height = int(self.window.winfo_screenheight())
        left = int((screen_width - width) / 2)
        top = int((screen_height - height) / 2)
        
        # 設定視窗大小和位置
        self.window.geometry(f'{width}x{height}+{left}+{top}')
        self.window.resizable(False, False)
        
        # 建立按鈕
        self.create_button(self.window, test_chapter)
        self.window.mainloop()
        
    def on_button_press(self, button_text):
        # Hide current window
        self.window.withdraw()
    
        # Create new window and get reference
        test_case_window = TestCaseGUI(button_text)
    
        # Add callback for when child window closes
        test_case_window.window.protocol("WM_DELETE_WINDOW", 
        lambda: [test_case_window.window.destroy(), self.window.deiconify()])
        # TestCaseGUI(button_text)

if __name__ == "__main__":
    gui = AutoScriptGUI()