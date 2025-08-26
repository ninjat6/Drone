from tkinterGUI import tkinterGUI
import pexpect
import tkinter as tk
import threading
import subprocess

class CallProgram(tkinterGUI):
    def __init__(self):
        self.password = 'kali'

    def launch_zenmap(self):
        try:
            child = pexpect.spawn('sudo zenmap')
            child.expect('.*[Pp]assword.*:')
            child.sendline(self.password)
            child.interact()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"啟動 Zenmap 時發生錯誤: {str(e)}")

    def launch_wireshark(self):
        try:
            child = pexpect.spawn('sudo wireshark')
            child.expect('.*[Pp]assword.*:')
            child.sendline(self.password)
            child.interact()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"啟動 Wireshark 時發生錯誤: {str(e)}")

    def launch_putty(self, window):
        try:
            child = pexpect.spawn('sudo putty')
            child.expect('.*[Pp]assword.*:')
            child.sendline(self.password)
            child.interact()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"啟動 Putty 時發生錯誤: {str(e)}", parent=window)
    
    def launch_burpsuite(self, window):
        try:
            child = pexpect.spawn('sudo burpsuite')
            child.expect('.*[Pp]assword.*:')
            child.sendline(self.password)
            child.interact()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"啟動 Burp Suite 時發生錯誤: {str(e)}", parent=window)

    def launch_nessus(self):
            self.window = tk.Toplevel()
            self.window_setup()
            self.window.title("Nessus 弱掃工具")
            self.window.geometry("600x200")

            style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

            label = tk.Label(self.window, text="伺服器網址：", **style)
            label.pack()

            entry = tk.Entry(self.window, width=50)
            entry.insert(0, "192.168.92.132:8834")
            entry.pack(padx=10)

            label = tk.Label(self.window, text="請輸入測試電腦IP", **style)
            label.pack()

            # button = tk.Button(self.window, text="開啟Nessus", command=lambda: self.open_firefox(entry.get(), self.window), **style)
            # button.pack()

    def open_firefox(self, url, window):
        try:
            if not url.startswith("https://"):url = "https://" + url
            threading.Thread(target=subprocess.run, args=(['firefox', url],)).start()
            window.destroy()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"無法打開 Firefox 瀏覽器: {str(e)}", parent=self.window)