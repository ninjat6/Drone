import tkinter as tk
from tkinterGUI import tkinterGUI
from CallProcess import CallProcess
from CallProgram import CallProgram
from CallWindow import CallWindow

class TestCaseGUI(tkinterGUI):
    def __init__(self, text):
        self.window = tk.Toplevel()
        self.window_setup(text)
        self.window.title('檢測項目')
        
        # ... Test Case lists definition ...
        self.UAV_TC = ['6.2.3 系統異常流量', '6.5.1 韌體更新安全', '8.1.1 衛星定位系統強化能力', '8.1.2 衛星定位系統干擾處理能力', '8.1.5 韌體已知漏洞檢測', '8.2.3 工程除錯介面']
        self.GCS_TC = ['6.2.1 身分鑑別', '6.2.2 網路服務埠檢測', '6.2.3 系統異常流量', '6.3.1 惡意程式', '6.3.2 弱點掃描', '8.1.3 取得行動應用 App 基本資安標章', '8.2.5 未公開揭露應用程式', '8.2.6 軟體更新安全']
        self.Hybrid_TC = ['6.4.1 無線通訊安全', '8.1.4 無線通訊失效處理能力', '8.2.1 數據儲存安全', '8.2.2 無人機命令連結（command link）之認證機制', '8.2.4 原始碼安全掃描']
        
        # 創建三個 Frame 用於分別放置三種類型的按鈕
        uav_frame = tk.Frame(self.window)
        uav_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        uav_label = tk.Label(uav_frame, text="UAV 測試項目", font=(self.style_font, self.style_fontsize))
        uav_label.pack(side=tk.TOP, pady=5)
        
        gcs_frame = tk.Frame(self.window)
        gcs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        gcs_label = tk.Label(gcs_frame, text="GCS 測試項目", font=(self.style_font, self.style_fontsize))
        gcs_label.pack(side=tk.TOP, pady=5)
        
        hybrid_frame = tk.Frame(self.window)
        hybrid_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        hybrid_label = tk.Label(hybrid_frame, text="混合測試項目", font=(self.style_font, self.style_fontsize))
        hybrid_label.pack(side=tk.TOP, pady=5)
        
        # 按照不同選項創建按鈕
        if text == '6 遙控無人機資安檢測-安全要求':
            self.create_button(uav_frame, self.UAV_TC[:2])
            self.create_button(gcs_frame, self.GCS_TC[:5])
            self.create_button(hybrid_frame, [self.Hybrid_TC[0]])
        elif text == '8.1 遙控無人機資安檢測增項測試-一般安全要求':
            self.create_button(uav_frame, self.UAV_TC[:5])
            self.create_button(gcs_frame, self.GCS_TC[:6])
            self.create_button(hybrid_frame, self.Hybrid_TC[:2])
        elif text == '8.2 遙控無人機資安檢測增項測試-特殊安全要求':
            self.create_button(uav_frame, self.UAV_TC)
            self.create_button(gcs_frame, self.GCS_TC)
            self.create_button(hybrid_frame, self.Hybrid_TC)
            
    def window_setup(self, text):
        try:
            icon = tk.PhotoImage(file='icon.png')
            self.window.iconphoto(False, icon)
        except Exception as e:
            print(f"Error loading icon: {e}")

        self.style_fontsize = 12
        self.style_font = "Microsoft JhengHei"
        # 設定視窗大小
        if text == '6 遙控無人機資安檢測-安全要求':
            width = 660
            height = 290
        elif text == '8.1 遙控無人機資安檢測增項測試-一般安全要求':
            width = 940
            height = 340
        elif text == '8.2 遙控無人機資安檢測增項測試-特殊安全要求':
            width = 1100
            height = 440
        
        # 計算視窗位置使其置中
        screen_width = int(self.window.winfo_screenwidth())
        screen_height = int(self.window.winfo_screenheight())
        left = int((screen_width - width) / 2)
        top = int((screen_height - height) / 2)
        
        # 設定視窗大小和位置
        self.window.geometry(f'{width}x{height}+{left}+{top}')
        self.window.resizable(False, False)
    
    def on_button_press(self, button_text):
        if button_text=='6.2.3 系統異常流量':
            print('6.2.3 系統異常流量')
            CallProgram().launch_wireshark()
        elif button_text=='6.5.1 韌體更新安全':
            print('6.5.1 韌體更新安全')
            CallProcess().generateHash(self.window)


        elif button_text=='8.1.1 衛星定位系統強化能力':
            print('8.1.1 衛星定位系統強化能力')
        elif button_text=='8.1.2 衛星定位系統干擾處理能力':
            print('8.1.2 衛星定位系統干擾處理能力')


        elif button_text=='8.1.5 韌體已知漏洞檢測':
            print('8.1.5 韌體已知漏洞檢測')
            CallProcess().binaryscan()
        elif button_text=='8.2.3 工程除錯介面':
            print('8.2.3 工程除錯介面')
            CallProgram().launch_putty(self.window)
        elif button_text=='6.2.1 身分鑑別':
            print('6.2.1 身分鑑別')
            CallProcess().userfinder()
        elif button_text=='6.2.2 網路服務埠檢測':
            print('6.2.2 網路服務埠檢測')
            CallProgram().launch_zenmap()
        elif button_text=='6.3.1 惡意程式':
            print('6.3.1 惡意程式')
            CallWindow().malwarescan()
        elif button_text=='6.3.2 弱點掃描':
            print('6.3.2 弱點掃描')
            CallProgram().launch_nessus()
        elif button_text=='8.1.3 取得行動應用 App 基本資安標章':
            print('8.1.3 取得行動應用 App 基本資安標章')
            CallWindow().check_MAS_logo()
        elif button_text=='8.2.5 未公開揭露應用程式':
            print('8.2.5 未公開揭露應用程式')
            #SBOM

        elif button_text=='8.2.6 軟體更新安全':
            print('8.2.6 軟體更新安全')
            #逆向工程

        elif button_text=='6.4.1 無線通訊安全':
            print('6.4.1 無線通訊安全')
            CallProcess().launch_aircrack()
        elif button_text=='8.1.4 無線通訊失效處理能力':
            print('8.1.4 無線通訊失效處理能力')
            CallWindow().failsavemechanism()
        elif button_text=='8.2.1 數據儲存安全':
            print('8.2.1 數據儲存安全')
            CallProcess().checkencrypted()
        elif button_text=='8.2.2 無人機命令連結（command link）之認證機制':
            print('8.2.2 無人機命令連結（command link）之認證機制')
            CallProgram().launch_burpsuite(self.window)
        
        elif button_text=='8.2.4 原始碼安全掃描':
            print('8.2.4 原始碼安全掃描')
            