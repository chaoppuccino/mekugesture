import tkinter as tk
from tkinter import ttk, filedialog
import os

from session import Session
from file_manager import FileManager

class MekuGesture(tk.Tk):

    def __init__(self, file_manager):
        super().__init__()

        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.app_path, "graphics", "icon.ico")
        self.themes_path = os.path.join(self.app_path, "themes")

        self.file_manager = file_manager

        # directory for reference images
        self.directory = tk.StringVar()
        self.directory.set(file_manager.directory)
        self.directory_prev = self.directory.get()

        # time interval
        self.seconds = tk.StringVar()
        self.seconds.set(file_manager.seconds)
        self.seconds_prev = self.seconds.get()

        self._setup_window()
        self._setup_ui()


    def _setup_window(self):

        # push window to the front
        self.attributes('-topmost', 1)
        self.update_idletasks()
        self.wait_visibility(self)
        self.attributes('-topmost', 0)

        self.title('MekuGesture')

        # window size and screen position
        width = 600
        height = 400
        x_pos = self.winfo_screenwidth() // 2 - width // 2
        y_pos = self.winfo_screenheight() // 2 - height // 2
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.minsize(int(width//1.5), int(height//1.5))

        # window icon
        try:
            self.iconbitmap(self.icon_path)
        except Exception:
            pass

        # theme and bg color
        theme_name = 'awdark'
        self.tk.call('lappend', 'auto_path', self.themes_path)
        self.tk.call('package', 'require', theme_name)
        style = ttk.Style(self)
        style.theme_use(theme_name)
        self.configure(bg=style.lookup("TLabel", "background"))


    def _setup_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._create_dir_frame()
        self._create_time_frame()
        self._create_session_frame()


    def _create_dir_frame(self):

        frame = ttk.Frame(self, borderwidth = 5, relief='sunken')
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="nswe")

        label = ttk.Label(frame, text="Folder with references")
        label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, sticky="w")

        vcmd = (self.register(self._validate_directory), '%P')
        entry = ttk.Entry(frame, textvariable=self.directory, validate='focusout', validatecommand=vcmd)
        entry.bind("<Return>", self._unfocus_widget)
        entry.grid(row=1, column=0, padx=5, pady=5, ipadx=5, sticky="ew")

        button = ttk.Button(frame, text='Browse', command=self._submit_directory)
        button.grid(row=1, column=2, padx=5, pady=5, ipadx=5)


    def _create_time_frame(self):

        frame = ttk.Frame(self, width=100, height=100, borderwidth = 5, relief='sunken')
        frame.grid(row=1, column=0, sticky="nswe")

        label = ttk.Label(frame, text="Time per image (in seconds)")
        label.grid(row=0, column=0, padx=5, pady=5, ipadx=5, sticky="w")

        vcmd = (self.register(self._validate_spinbox), '%P')
        spinbox = ttk.Spinbox(frame, width=20, from_=0, to_=99999, textvariable=self.seconds, validate='focusout', validatecommand=vcmd, command=self._spinbox_change)
        spinbox.bind("<Return>", self._unfocus_widget)
        spinbox.config(state="normal", cursor="hand2", wrap=True)
        spinbox.grid(row=1,column=0,padx=5, pady=5, ipadx=5, sticky="ew")
    

    def _create_session_frame(self):

        frame = ttk.Frame(self, borderwidth = 5, relief='sunken')
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid(row=2, column=0, sticky="nswe")

        button = ttk.Button(frame, text='Start session', command=self._start_session)
        button.grid(row=1, column=1, padx=5, pady=5, ipadx=5, sticky="nswe")


    def _submit_directory(self):
        directory = filedialog.askdirectory()
        if directory:

            self.directory.set(os.path.normpath(directory))
            self.directory_prev = self.directory.get()

            # update directory in file manager
            self.file_manager.update_directory(self.directory.get())


    def _validate_directory(self, value):
        if os.path.isdir(value):
            self.directory_prev = value

            # update directory in file manager
            self.file_manager.update_directory(self.directory.get())

            return True
        else:
            self.directory.set(self.directory_prev)
            return False


    def _spinbox_change(self):
        self.seconds_prev = self.seconds.get()

        # update seconds in file manager
        self.file_manager.update_seconds(self.seconds.get())


    def _validate_spinbox(self, value):
        if value.isdigit():
            self.seconds_prev = value

            # update seconds in file manager
            self.file_manager.update_seconds(self.seconds.get())

            return True
        else:
            self.seconds.set(self.seconds_prev)
            return False


    def _unfocus_widget(self, event):
        self.focus_set()


    def _start_session(self):

        print("session started")

        self.withdraw()
        Session(self, self.file_manager, self.seconds.get())
