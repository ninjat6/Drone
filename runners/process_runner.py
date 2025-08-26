import subprocess
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import platform
import shutil
from . import Runner

class ProcessRunner(Runner):
    """
    Runs test cases that involve command-line processes.
    """
    def __init__(self, window=None):
        super().__init__(window)
        self.password = 'kali'

    def userfinder(self):
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title("使用者列舉")
        self.window.geometry("600x200")

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

        label = tk.Label(self.window, text="請依GCS系統類型點擊按鈕，列舉使用者", **style)
        label.pack()

        button_frame = tk.Frame(self.window)
        button_frame.pack(padx=10, pady=10)

        button_win = tk.Button(button_frame, text="Windows", command=self.userfinder_win, **style)
        button_win.pack(side=tk.LEFT, padx=5)

        button_linux = tk.Button(button_frame, text="Linux", command=self.userfinder_linux, **style)
        button_linux.pack(side=tk.LEFT, padx=5)

        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()

    def userfinder_win(self):
        if platform.system() != "Windows":
            tk.messagebox.showerror("錯誤", "此功能僅適用於 Windows", parent=self.window)
            return None

        exe = shutil.which('net')
        if not exe:
            tk.messagebox.showerror("錯誤", "找不到 net 指令", parent=self.window)
            return None
        users = subprocess.run([exe, 'user'], capture_output=True, text=True, check=False)
        file_address = self.outputfile(users.stdout)
        if file_address:
            self.open_file(file_address)
        return file_address

    def userfinder_linux(self):
        if platform.system() == "Windows":
            tk.messagebox.showerror("錯誤", "此功能不適用於 Windows", parent=self.window)
            return None
        try:
            file_path = self.dump_passwd()
            if file_path:
                self.open_file(file_path)
        except Exception as e:
            tk.messagebox.showerror("錯誤", str(e), parent=self.window)

    def dump_passwd(self):
        try:
            with open('/etc/passwd', 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return self.outputfile(content)
        except Exception as e:
            tk.messagebox.showerror("錯誤", str(e), parent=self.window)
            return None

    def launch_aircrack(self):
        tk.messagebox.showinfo("資訊", "此功能 (Aircrack-ng) 施工中", parent=self.main_window)

    def source_code_scan(self):
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title("原始碼安全掃描")
        self.window.geometry("600x200")

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

        label = tk.Label(self.window, text="選擇程式碼目錄並執行 cve-bin-tool", **style)
        label.pack(pady=10)

        entry = tk.Entry(self.window, width=50)
        entry.pack(padx=10, pady=5)

        button_dir = tk.Button(self.window, text="選擇目錄", command=lambda: self.browse_dir(entry), **style)
        button_dir.pack()

        button_scan = tk.Button(self.window, text="開始掃描", command=lambda: self.run_cve_scan(entry.get()), **style)
        button_scan.pack(pady=5)

        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()

    def run_cve_scan(self, directory):
        if not directory:
            tk.messagebox.showwarning("警告", "請先選擇目錄", parent=self.window)
            return
        exe = shutil.which('cve-bin-tool')
        if not exe:
            tk.messagebox.showerror("錯誤", "找不到 cve-bin-tool 指令", parent=self.window)
            return
        try:
            subprocess.Popen([exe, directory])
            tk.messagebox.showinfo("資訊", f"cve-bin-tool 正在掃描目錄:\n{directory}\n請查看終端機/命令提示字元獲取輸出。", parent=self.window)
        except Exception as e:
            tk.messagebox.showerror("錯誤", str(e), parent=self.window)

    def checkencrypted(self):
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title("Hexdump 工具")
        self.window.geometry("600x400")

        entry = tk.Entry(self.window, width=50)
        entry.pack(padx=10, pady=10)
        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

        button_chose = tk.Button(self.window, text="選擇檔案", command=lambda: self.browse_file(entry), **style)
        button_chose.pack(padx=10, pady=10)

        label = tk.Label(self.window, text="以hexdump讀取檔案並開啟，請確認開啟檔案是否為明文顯示", **style)
        label.pack(pady=10)

        button_read = tk.Button(self.window, text="讀取",command=lambda: self.readfilewith_hexdump(entry), **style)
        button_read.pack(padx=10, pady=10)

        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()

    def readfilewith_hexdump(self, entry):
        file_address = entry.get()
        if not file_address:
            tk.messagebox.showwarning("警告", "請先選擇檔案", parent=self.window)
            return

        exe = shutil.which('hexdump')
        if not exe:
            tk.messagebox.showerror("錯誤", "找不到 hexdump 指令", parent=self.window)
            return
        plaintext = subprocess.run([exe, '-C', file_address],
                                   capture_output=True,
                                   text=True, check=False)
        output_file = self.outputfile(plaintext.stdout)
        if output_file:
            self.open_file(output_file)

    def outputfile(self, plaintext):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="儲存檔案",
            parent=self.window
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(plaintext)
                tk.messagebox.showinfo("完成", f"檔案已儲存至: {file_path}", parent=self.window)
                return file_path
            except Exception as e:
                tk.messagebox.showerror("錯誤", f"無法儲存檔案: {e}", parent=self.window)
        return None

    def open_file(self, file_address):
        system = platform.system()
        try:
            if system == 'Windows':
                os.startfile(file_address)
            elif system == 'Darwin':
                subprocess.Popen(['open', file_address])
            else:
                opener = shutil.which('xdg-open') or shutil.which('mousepad')
                if not opener:
                    tk.messagebox.showerror('錯誤', '找不到可用的程式開啟檔案', parent=self.window)
                    return
                subprocess.Popen([opener, file_address])
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"無法開啟檔案: {e}", parent=self.window)

    def binaryscan(self):
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title("韌體掃描 (cve-bin-tool)")
        self.window.geometry("600x300")
        entry = tk.Entry(self.window, width=50)
        entry.pack(padx=10, pady=10)

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

        button_frame = tk.Frame(self.window)
        button_frame.pack(padx=10, pady=10)

        selectfile = tk.Button(button_frame, text="選擇檔案", command=lambda: self.browse_file(entry), **style)
        selectfile.pack(side=tk.LEFT, padx=5)

        selectdir = tk.Button(button_frame, text="選擇資料夾", command=lambda: self.browse_dir(entry), **style)
        selectdir.pack(side=tk.LEFT, padx=5)

        scan = tk.Button(self.window, text="開始掃描",
                          command=lambda: self.scanfirmware(entry.get()), **style)
        scan.pack(padx=10, pady=10)

        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()

    def scanfirmware(self, payload):
        if not payload:
            tk.messagebox.showwarning("警告", "請先選擇檔案或資料夾", parent=self.window)
            return

        output_file = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("Html files", "*.html"), ("All files", "*.*")],
            parent=self.window
        )
        if not output_file:
            return

        exe = shutil.which('cve-bin-tool')
        if not exe:
            tk.messagebox.showerror("錯誤", "找不到 cve-bin-tool 指令", parent=self.window)
            return

        cmd = [exe, payload, '-f', 'html', '-o', output_file]

        try:
            subprocess.Popen(cmd)
            tk.messagebox.showinfo("資訊", f"cve-bin-tool 正在掃描:\n{payload}\n掃描完成後報告將儲存至:\n{output_file}", parent=self.window)
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"無法啟動掃描: {e}", parent=self.window)


    def generateHash(self):
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title("檔案 Hash 值")
        self.window.geometry("600x250")

        entry = tk.Entry(self.window, width=50)
        entry.pack(padx=10, pady=10)

        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

        button1 = tk.Button(self.window, text="選擇檔案", command=lambda: self.browse_file(entry), **style)
        button1.pack(pady=5)

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)

        self.hash_label = tk.Label(self.window, text="", **style)
        self.hash_label.pack(pady=10)

        button2 = tk.Button(button_frame, text="MD5", command=lambda: self.display_md5_hash(entry.get()), **style)
        button2.pack(side=tk.LEFT, padx=5)

        button3 = tk.Button(button_frame, text="SHA1", command=lambda: self.display_sha1_hash(entry.get()), **style)
        button3.pack(side=tk.LEFT, padx=5)

        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()

    def display_md5_hash(self, file_name):
        self._display_hash(file_name, 'md5')

    def display_sha1_hash(self, file_name):
        self._display_hash(file_name, 'sha1')

    def _display_hash(self, file_name, hash_alg):
        if not file_name or not os.path.exists(file_name):
            tk.messagebox.showerror("錯誤", f"找不到檔案: {file_name}", parent=self.window)
            return
        try:
            hasher = hashlib.new(hash_alg)
            with open(file_name, 'rb') as f:
                buf = f.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = f.read(65536)
            hashvalue = hasher.hexdigest()
            self.hash_label.config(text=f"{hash_alg.upper()}: {hashvalue}")
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"計算 {hash_alg.upper()} 時發生錯誤: {str(e)}", parent=self.window)

    def browse_dir(self, entry):
        dir_path = filedialog.askdirectory(parent=self.window)
        if dir_path:
            entry.delete(0, tk.END)
            entry.insert(0, dir_path)
            self.window.lift()

    def browse_file(self, entry):
        file_path = filedialog.askopenfilename(parent=self.window)
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
            self.window.lift()
