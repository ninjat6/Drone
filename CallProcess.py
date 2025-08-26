# import pages as pg
from tkinterGUI import tkinterGUI
import subprocess
import threading
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import platform
import shutil

class CallProcess(tkinterGUI):
    def __init__(self):
        self.password = 'kali'

    def userfinder(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title("使用者列舉")
        self.window.geometry("600x200")

        # 設定按鈕，統一樣式
        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}
        
        self.label = tk.Label(self.window, text="請依GCS系統類型點擊按鈕，列舉使用者", **style)
        self.label.pack()

        # 創建框架容納 MD5 和 SHA1 按鈕
        button_frame = tk.Frame(self.window)
        button_frame.pack(padx=10, pady=10)

        #按鈕並排
        button_win = tk.Button(button_frame, text="Windows", command=lambda: self.userfinder_win(), **style)
        button_win.pack(side=tk.LEFT, padx=5)

        button_linux = tk.Button(button_frame, text="Linux", command=lambda: self.userfinder_linux(), **style)
        button_linux.pack(side=tk.LEFT, padx=5)

    def userfinder_win(self):
        exe = shutil.which('net')
        if not exe:
            tk.messagebox.showerror("錯誤", "找不到 net 指令", parent=self.window)
            return None
        users = subprocess.run([exe, 'user'], capture_output=True, text=True)
        file_address = self.outputfile(users.stdout)
        return file_address
    
    def userfinder_linux(self):
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
        print("施工中")
        pass

    def source_code_scan(self):
        self.window = tk.Toplevel()
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
        except Exception as e:
            tk.messagebox.showerror("錯誤", str(e), parent=self.window)

    def checkencrypted(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title("Hexdump 工具")
        self.window.geometry("600x400")

        # 取得檔案路徑
        entry = tk.Entry(self.window, width=50)
        entry.pack(padx=10, pady=10)
        style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

        button_chose = tk.Button(self.window, text="選擇檔案", command=lambda: self.browse_file(entry), **style)
        button_chose.pack(padx=10, pady=10)
        
        label = tk.Label(self.window, text="以hexdump讀取檔案並開啟，請確認開啟檔案是否為明文顯示", **style)
        label.pack(pady=10)

        button_read = tk.Button(self.window, text="讀取",command=lambda: self.readfilewith_hexdump(entry), **style)
        button_read.pack(padx=10, pady=10) 

    def readfilewith_hexdump(self, entry):
        file_address = entry.get()
        exe = shutil.which('hexdump')
        if not exe:
            tk.messagebox.showerror("錯誤", "找不到 hexdump 指令", parent=self.window)
            return
        plaintext = subprocess.run([exe, '-C', file_address],
                                   capture_output=True,
                                   text=True)
        file_address = self.outputfile(plaintext.stdout)
        self.open_file(file_address)

    def outputfile(self, plaintext):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="儲存檔案"
        )
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    if isinstance(plaintext, str):
                        f.write(plaintext)
                    else:
                        f.write(plaintext.stdout)
                tk.messagebox.showinfo("完成", f"檔案已儲存至: {file_path}")
            except Exception as e:
                tk.messagebox.showerror("錯誤", f"無法儲存檔案: {e}", parent=self.window)
                file_path = ""
        return file_path

    def openfilewith_code(self, file_address):
        exe = shutil.which('code')
        if not exe:
            raise RuntimeError("找不到 VS Code 指令")
        try:
            process = subprocess.Popen(
                [exe, file_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            _, stderr = process.communicate()
            if process.returncode != 0:
                raise RuntimeError(f"無法開啟 VS Code: {stderr.decode()}")
        except Exception as e:
            raise RuntimeError(f"啟動 VS Code 失敗: {e}")

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
                    raise RuntimeError('找不到可用的程式開啟檔案')
                subprocess.Popen([opener, file_address])
        except Exception as e:
            raise RuntimeError(f"無法開啟: {e}")

    def binaryscan(self):
        try:
            self.window = tk.Toplevel()
            self.window_setup()
            self.window.title("CVE-bin-tool")
            self.window.geometry("600x300")
            # 設定輸入框
            entry = tk.Entry(self.window, width=50)
            entry.pack(padx=10, pady=10)

            # 設定按鈕，統一樣式
            style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

            selectfile = tk.Button(self.window, text="選擇檔案", command=lambda: self.browse_file(entry), **style)
            selectfile.pack(padx=10, pady=10)

            selectdir = tk.Button(self.window, text="選擇資料夾", command=lambda: self.browse_dir(entry), **style)
            selectdir.pack(padx=10, pady=10)

            scan = tk.Button(self.window, text="開始掃描", 
                              command=lambda: self.scanfirmware(entry, self.window), **style)
            scan.pack(padx=10, pady=10)

            # button3 = tk.Button(self.window, text="更新CVE資料庫", command=lambda: threading.Thread(target=lambda:self.update_cve_bin_tool(self.window)).start(), **style)
            # button3.pack(padx=10, pady=10)
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"{str(e)}", parent=self.window)

    def scanfirmware(self, input, window):
        # try:
            payload = input.get()

            output_file = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("Html files", "*.html"), ("All files", "*.*")],
                parent=window
            )
            print("scan")
            exe = shutil.which('cve-bin-tool')
            if not exe:
                tk.messagebox.showerror("錯誤", "找不到 cve-bin-tool 指令", parent=window)
                return
            cmd = [exe, payload, '-f', 'html', '-o', output_file]
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            print("scan done")
        
            # if output_file:
            #     # 建立進度視窗
            #     progress_window = tk.Toplevel(window)
            #     progress_window.title("掃描進度")
            #     progress_window.geometry("400x150")
            #     progress_window.transient(window)
                
            #     # 進度標籤
            #     status_label = tk.Label(progress_window, 
            #                         text="準備掃描...", 
            #                         font=(self.style_font, self.style_fontsize))
            #     status_label.pack(pady=10)
                
            #     # 視窗置中
            #     progress_window.geometry("+%d+%d" % (
            #     window.winfo_rootx() + 50,
            #     window.winfo_rooty() + 50))

            #     # 進度條
            #     progress_var = tk.DoubleVar()
            #     progress_bar = ttk.Progressbar(progress_window, 
            #                                 variable=progress_var,
            #                                 maximum=100,
            #                                 length=300)
            #     progress_bar.pack(pady=10)
                
            #     # 細節標籤
            #     detail_label = tk.Label(progress_window, 
            #                         text="", 
            #                         font=(self.style_font, self.style_fontsize-2))
            #     detail_label.pack(pady=5)
                
            #     def update_progress(value, status, detail=""):
            #         if progress_window.winfo_exists():
            #             progress_var.set(value)
            #             status_label.config(text=status)
            #             detail_label.config(text=detail)
            #             progress_window.update()

            #     def cleanup():
            #         """清理資源"""
            #         if progress_window.winfo_exists():
            #             progress_window.destroy()
                
                # def run_scan():
                    # try:
                        # cmd = f'cve-bin-tool "{payload}" -f html -o "{output_file}"'
                        # process = subprocess.Popen(
                        #     cmd,
                        #     shell=True,
                        #     stdout=subprocess.PIPE,
                        #     stderr=subprocess.PIPE,
                        #     text=True,
                        #     bufsize=1
                        # )
                        
                        # total_steps = 0
                        # current_step = 0

                        # # 監控掃描進度
                        # while True:
                        #     line = process.stdout.readline()
                        #     if not line and process.poll() is not None:
                        #         break
                                
                        #     if "Scanning" in line:
                        #         current_step += 1
                        #         progress = min((current_step / max(total_steps, 1)) * 100, 95)
                        #         update_progress(progress, "掃描中...", line.strip())
                        #     elif "found" in line:
                        #         total_steps += 1
                        #         update_progress(50, "分析中...", line.strip())
                            
                        # if process.returncode == 0:
                        #     update_progress(100, "掃描完成!")
                        #     progress_window.after(1000, cleanup)
                        #     tk.messagebox.showinfo("完成", 
                        #         f"掃描完成\n結果已儲存至: {output_file}", parent=window)
                        # else:
                        #     stderr = process.stderr.read()
                        #     raise RuntimeError(f"掃描失敗: {stderr}")
                            
                    # except Exception as e:
                    #     cleanup()
                    #     tk.messagebox.showerror("錯誤", str(e), parent=window)
                
                # 設定關閉處理
                # run_scan()
                # progress_window.protocol("WM_DELETE_WINDOW", cleanup)
                # threading.Thread(target=run_scan, daemon=True).start()
        # except Exception as e:
        #     tk.messagebox.showerror("錯誤", str(e), parent=window)

    def launch_cve_bin_tool(self, entry, window):
        try:
            dirpath = entry.get()
            if not dirpath:
                raise ValueError("請選擇要掃描的目錄")
                
            if not os.path.exists(dirpath):
                raise FileNotFoundError("找不到指定的目錄")
            
            # 取得所有檔案清單
            files_to_scan = []
            for root, _, files in os.walk(dirpath):
                for file in files:
                    files_to_scan.append(os.path.join(root, file))
            
            if not files_to_scan:
                raise ValueError("所選目錄中沒有檔案")
                        
            output_file = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("Html files", "*.html"), ("All files", "*.*")],
                parent=window
            )
            
            if output_file:
                progress_window = tk.Toplevel(window)
                progress_window.title("掃描進度")
                progress_window.geometry("500x200")
                
                # 檔案進度
                file_label = tk.Label(progress_window, 
                                    text=f"掃描檔案 (0/{len(files_to_scan)})", 
                                    font=(self.style_font, self.style_fontsize))
                file_label.pack(pady=5)
                
                # 總進度條
                total_progress = tk.DoubleVar()
                total_bar = ttk.Progressbar(progress_window, 
                                        variable=total_progress,
                                        maximum=100,
                                        length=400)
                total_bar.pack(pady=5)
                
                # 當前檔案標籤
                current_file = tk.Label(progress_window, 
                                    text="", 
                                    font=(self.style_font, self.style_fontsize-2))
                current_file.pack(pady=5)
                
                # 狀態訊息
                status_label = tk.Label(progress_window, 
                                    text="", 
                                    font=(self.style_font, self.style_fontsize-2))
                status_label.pack(pady=5)
                
                def update_progress(file_count, current, status=""):
                    if progress_window.winfo_exists():
                        progress = (file_count / len(files_to_scan)) * 100
                        total_progress.set(progress)
                        file_label.config(text=f"掃描檔案 ({file_count}/{len(files_to_scan)})")
                        current_file.config(text=f"當前: {current}")
                        status_label.config(text=status)
                        progress_window.update()
                
                def run_scan():
                    try:
                        exe = shutil.which('cve-bin-tool')
                        if not exe:
                            raise RuntimeError('找不到 cve-bin-tool 指令')
                        # 建立暫存目錄存放各檔案的掃描結果
                        temp_dir = os.path.join(os.path.dirname(output_file), "temp_results")
                        os.makedirs(temp_dir, exist_ok=True)

                        results = []
                        for i, file in enumerate(files_to_scan, 1):
                            update_progress(i, os.path.basename(file), "掃描中...")
                            temp_output = os.path.join(temp_dir, f"result_{i}.html")

                            cmd = [exe, file, '-f', 'html', '-o', temp_output]
                            process = subprocess.run(cmd, capture_output=True, text=True)

                            if process.returncode == 0 and os.path.exists(temp_output):
                                with open(temp_output, 'r') as f:
                                    results.append(f.read())
                        
                        # 合併結果
                        update_progress(len(files_to_scan), "", "合併報告中...")
                        with open(output_file, 'w') as f:
                            f.write("\n".join(results))
                        
                        # 清理暫存檔案
                        import shutil
                        shutil.rmtree(temp_dir)
                        
                        progress_window.destroy()
                        tk.messagebox.showinfo("完成", 
                            f"掃描完成\n結果已儲存至: {output_file}", 
                            parent=window)
                        
                    except Exception as e:
                        if progress_window.winfo_exists():
                            progress_window.destroy()
                        tk.messagebox.showerror("錯誤", str(e), parent=window)
                
                threading.Thread(target=run_scan, daemon=True).start()
                
        except Exception as e:
            tk.messagebox.showerror("錯誤", str(e), parent=window)

    def generateHash(self, window):
        try:
            self.window = tk.Toplevel()
            self.window_setup()
            self.window.title("檔案 Hash 值")
            self.window.geometry("600x200")
            # 設定輸入框
            entry = tk.Entry(self.window, width=50)
            entry.pack(padx=10, pady=10)

            # 設定按鈕，統一樣式
            style = {'font': (self.style_font, self.style_fontsize), 'padx': 10, 'pady': 10}

            button1 = tk.Button(self.window, text="選擇檔案", command=lambda: self.browse_file(entry), **style)
            button1.pack(padx=10, pady=10)

            # 創建框架容納 MD5 和 SHA1 按鈕
            button_frame = tk.Frame(self.window)
            button_frame.pack(padx=10, pady=10)

            # MD5 和 SHA1 按鈕並排
            button2 = tk.Button(button_frame, text="MD5", command=lambda: self.display_md5_hash(entry.get()), **style)
            button2.pack(side=tk.LEFT, padx=5)

            button3 = tk.Button(button_frame, text="SHA1", command=lambda: self.display_sha1_hash(entry.get()), **style)
            button3.pack(side=tk.LEFT, padx=5)

            self.label = tk.Label(self.window, text="", **style)
            self.label.pack()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"{str(e)}", parent=window)

    def display_md5_hash(self, file_name):
        try:
            if not os.path.exists(file_name):
                raise FileNotFoundError("檔案不存在")
            with open(file_name, 'rb') as file:
                hashvalue = hashlib.md5(file.read()).hexdigest()
            self.label.config(text=f"MD5: {hashvalue}")
        except FileNotFoundError as e:
            tk.messagebox.showerror("錯誤", f"找不到檔案: {str(e)}", parent=self.window)
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"計算 MD5 時發生錯誤: {str(e)}", parent=self.window)

    def display_sha1_hash(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                hashvalue = hashlib.sha1(file.read()).hexdigest()
            self.label.config(text=f"SHA1: {hashvalue}")
        except FileNotFoundError as e:
            tk.messagebox.showerror("錯誤", f"找不到檔案: {str(e)}", parent=self.window)
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"計算 SHA1 時發生錯誤: {str(e)}", parent=self.window)
    
    def browse_dir(self, entry):
        # 打開文件對話框，讓使用者選擇文件
        dir_path = filedialog.askdirectory()
        if dir_path:
            # 如果使用者選擇了文件，將文件路徑顯示在文字框中
            entry.delete(0, tk.END)  # 清空文字框
            entry.insert(0, dir_path)
            # 將視窗提到最前方
            self.window.lift()
            self.window.focus_force()

    def browse_file(self, entry):
        # 打開文件對話框，讓使用者選擇文件
        file_path = filedialog.askopenfilename()
        if file_path:
            # 如果使用者選擇了文件，將文件路徑顯示在文字框中
            entry.delete(0, tk.END)  # 清空文字框
            entry.insert(0, file_path)
            # 將視窗提到最前方
            self.window.lift()
            self.window.focus_force()
