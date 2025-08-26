import tkinter as tk
from tkinter import messagebox
from tkinterGUI import tkinterGUI
import config
from runners.program_runner import ProgramRunner
from runners.process_runner import ProcessRunner
from runners.guide_runner import GuideRunner

class TestCaseGUI(tkinterGUI):
    def __init__(self, main_window, chapter_id):
        self.main_window = main_window
        self.window = tk.Toplevel(main_window)
        self.chapter_id = chapter_id

        try:
            # Load all test cases and prepare for lookup
            self.all_test_cases = config.load_test_cases()
            self.test_cases_by_id = {tc['id']: tc for tc in self.all_test_cases}
        except (FileNotFoundError, ValueError) as e:
            messagebox.showerror("設定檔錯誤", f"無法載入測試設定檔:\n{e}", parent=self.window)
            self.window.destroy()
            return

        # Initialize runners, passing the TestCaseGUI window as parent
        self.runners = {
            "Program": ProgramRunner(self.window),
            "Process": ProcessRunner(self.window),
            "Guide": GuideRunner(self.window)
        }

        self.window_setup()
        self.window.title(f'檢測項目: 章節 {self.chapter_id}')

        # Filter tests for the current chapter
        self.chapter_tests = [tc for tc in self.all_test_cases if self.chapter_id in tc['chapters']]

        # Create frames for test categories
        uav_frame = self._create_category_frame("UAV 測試項目")
        gcs_frame = self._create_category_frame("GCS 測試項目")
        hybrid_frame = self._create_category_frame("混合測試項目")

        # Populate frames with buttons
        self._populate_buttons(uav_frame, "UAV")
        self._populate_buttons(gcs_frame, "GCS")
        self._populate_buttons(hybrid_frame, "Hybrid")

        self._adjust_window_size()

    def _create_category_frame(self, text):
        frame = tk.Frame(self.window)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        label = tk.Label(frame, text=text, font=(self.style_font, self.style_fontsize))
        label.pack(side=tk.TOP, pady=5)
        return frame

    def _populate_buttons(self, frame, category):
        # Filter tests for the specific category and create buttons
        category_tests = sorted([tc for tc in self.chapter_tests if tc['category'] == category], key=lambda x: x['name'])
        for test_case in category_tests:
            # The button now passes the test case ID to the command
            button = tk.Button(frame,
                               text=test_case['name'],
                               font=(self.style_font, self.style_fontsize),
                               anchor='w',
                               command=lambda t_id=test_case['id']: self.on_button_press(t_id))
            button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    def on_button_press(self, test_id):
        """
        Handles button presses by dispatching to the correct runner.
        This replaces the old if/elif block.
        """
        test_case = self.test_cases_by_id.get(test_id)
        if not test_case:
            print(f"Error: Test case with ID '{test_id}' not found.")
            return

        runner_name = test_case.get("runner")
        action_name = test_case.get("action")

        runner = self.runners.get(runner_name)

        if runner and hasattr(runner, action_name):
            print(f"Running action '{action_name}' with runner '{runner_name}'...")
            try:
                action_method = getattr(runner, action_name)
                action_method()
            except Exception as e:
                print(f"Error running action {action_name}: {e}")
                messagebox.showerror("執行錯誤", f"執行 '{test_case['name']}' 時發生錯誤:\n{e}", parent=self.window)
        else:
            # This case can be handled by the 'not_implemented' action in the GuideRunner
            print(f"Warning: Runner '{runner_name}' or action '{action_name}' not found. Using fallback.")
            self.runners["Guide"].not_implemented()

    def window_setup(self):
        super().window_setup()
        self.window.resizable(False, False)

    def _adjust_window_size(self):
        """Dynamically adjust window size to fit content."""
        self.window.update_idletasks()

        max_height = 150 # Min height
        total_width = 0

        child_frames = [f for f in self.window.winfo_children() if isinstance(f, tk.Frame)]

        if not child_frames:
            self.window.geometry("300x150")
            return

        for frame in child_frames:
            frame.update_idletasks()
            max_height = max(max_height, frame.winfo_reqheight())
            total_width += frame.winfo_reqwidth()

        width = total_width + (len(child_frames) * 10) # Add padding
        height = max_height + 60 # Add padding for title, labels

        # Center the window
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        left = int((screen_width - width) / 2)
        top = int((screen_height - height) / 2)
        self.window.geometry(f'{width}x{height}+{left}+{top}')
