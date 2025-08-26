from tkinterGUI import tkinterGUI
import tkinter as tk

class Runner(tkinterGUI):
    """Base class for all test case runners."""

    def __init__(self, window=None):
        """
        Initializes the runner.

        Args:
            window: The parent tkinter window.
        """
        self.main_window = window

    def run(self, action, **kwargs):
        """
        Runs a specific action (test case).

        Args:
            action (str): The name of the method to run.
            **kwargs: Additional arguments for the action method.
        """
        if not hasattr(self, action):
            # Fallback for methods that might still be on the old Call* classes
            # This is a temporary measure during refactoring.
            if hasattr(self.legacy_runner, action):
                method = getattr(self.legacy_runner, action)
                return method(**kwargs)
            raise NotImplementedError(f"Action '{action}' is not implemented in {self.__class__.__name__}")

        method = getattr(self, action)
        method(**kwargs)

    def not_implemented(self):
        """Placeholder for actions that are not yet implemented."""
        self.window = tk.Toplevel(self.main_window)
        self.window_setup()
        self.window.title("功能尚未實作")
        self.window.geometry("300x100")
        style = {'font': (self.style_font, self.style_fontsize)}
        label = tk.Label(self.window, text="此功能尚未實作", **style)
        label.pack(pady=20)
        self.window.transient(self.main_window)
        self.window.grab_set()
        self.window.focus_force()
        self.window.wait_window()
