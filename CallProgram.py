from tkinterGUI import tkinterGUI
import tkinter as tk
import threading
import subprocess
import platform
import shutil

class CallProgram(tkinterGUI):
    """Launch external security tools in a cross‑platform manner."""

    def __init__(self):
        self.password = "kali"

    def _run_program(self, program, args=None, require_sudo=False, window=None):
        """Execute program if available.

        Args:
            program: Name of executable.
            args: Optional list of additional arguments.
            require_sudo: Prepend sudo on non‑Windows systems.
            window: Parent window for error dialogs.
        """
        exe = shutil.which(program)
        if not exe:
            tk.messagebox.showerror("錯誤", f"找不到 {program} 指令", parent=window)
            return

        cmd = [exe]
        if args:
            cmd.extend(args)
        if require_sudo and platform.system() != "Windows":
            cmd.insert(0, "sudo")

        def runner():
            try:
                subprocess.run(cmd, check=False)
            except Exception as e:
                tk.messagebox.showerror(
                    "錯誤",
                    f"執行 {program} 失敗: {e}",
                    parent=window,
                )

        threading.Thread(target=runner, daemon=True).start()

    def launch_zenmap(self):
        self._run_program("zenmap", require_sudo=True)

    def launch_wireshark(self):
        self._run_program("wireshark", require_sudo=True)

    def launch_putty(self, window):
        self._run_program("putty", require_sudo=True, window=window)

    def launch_burpsuite(self, window):
        self._run_program("burpsuite", require_sudo=True, window=window)

    def launch_nessus(self):
        self.window = tk.Toplevel()
        self.window_setup()
        self.window.title("Nessus 弱掃工具")
        self.window.geometry("600x200")

        style = {"font": (self.style_font, self.style_fontsize), "padx": 10, "pady": 10}

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
            if not url.startswith("https://"):
                url = "https://" + url
            self._run_program("firefox", args=[url])
            window.destroy()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"無法打開 Firefox 瀏覽器: {str(e)}", parent=self.window)

