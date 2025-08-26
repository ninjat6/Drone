import tkinter as tk
import threading
import subprocess
import platform
import shutil
from . import Runner

class ProgramRunner(Runner):
    """
    Runs test cases that involve launching an external GUI program.
    """
    def __init__(self, window=None):
        super().__init__(window)
        # The hardcoded password will be addressed in a later step.
        self.password = "kali"

    def _run_program(self, program, args=None, require_sudo=False):
        """
        Execute program if available.
        Uses self.main_window as the parent for error dialogs.
        """
        exe = shutil.which(program)
        if not exe:
            tk.messagebox.showerror("錯誤", f"找不到 {program} 指令", parent=self.main_window)
            return

        cmd = [exe]
        if args:
            cmd.extend(args)
        if require_sudo and platform.system() != "Windows":
            # This is the hardcoded password issue. We will address it later.
            # For now, we keep the old behavior. A better way would be to prompt the user.
            cmd.insert(0, "sudo")

        # Run in a separate thread to avoid blocking the GUI
        threading.Thread(target=subprocess.run, args=(cmd,), kwargs={"check": False, "capture_output": True}).start()

    def launch_zenmap(self):
        self._run_program("zenmap", require_sudo=True)

    def launch_wireshark(self):
        self._run_program("wireshark", require_sudo=True)

    def launch_putty(self):
        self._run_program("putty") # Putty usually doesn't require sudo to launch

    def launch_burpsuite(self):
        self._run_program("burpsuite") # Burp Suite doesn't require sudo

    def launch_nessus(self):
        self.window = tk.Toplevel(self.main_window)
        self.window.transient(self.main_window)
        self.window_setup()
        self.window.title("Nessus 弱掃工具")
        self.window.geometry("600x200")

        style = {"font": (self.style_font, self.style_fontsize), "padx": 10, "pady": 10}

        label = tk.Label(self.window, text="伺服器網址：", **style)
        label.pack()

        entry = tk.Entry(self.window, width=50)
        entry.insert(0, "https://127.0.0.1:8834")
        entry.pack(padx=10)

        button = tk.Button(self.window, text="開啟 Nessus in Firefox", command=lambda: self.open_firefox(entry.get()), **style)
        button.pack()

        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()


    def open_firefox(self, url):
        try:
            if not url.startswith("https://") and not url.startswith("http://"):
                url = "https://" + url
            self._run_program("firefox", args=[url])
            if hasattr(self, 'window') and self.window.winfo_exists():
                self.window.destroy()
        except Exception as e:
            tk.messagebox.showerror("錯誤", f"無法打開 Firefox 瀏覽器: {str(e)}", parent=self.main_window)
