import tkinter as tk
import os
from tkinter import ttk
from PIL import ImageTk, Image

from file_manager import FileManager
class Session(tk.Toplevel):

    def __init__(self, parent, file_manager, seconds):
        super().__init__(parent)

        self.parent = parent
        self.file_manager = file_manager
        self.seconds = int(seconds)

        self.seconds_left = self.seconds
        self.timer_running = True

        self.image_history = [] # history of images visited this session TODO: expand this into heat mechanic
        self.history_index = 0 # used for cycling through image history

        # session control keys
        self.bind("<Right>", self._cycle_next)
        self.bind("<Left>", self._cycle_previous)
        self.bind("<space>", self._toggle_pause)
        self.bind("<Escape>", self._exit_fullscreen)

        self._enter_fullscreen()
        self._setup_timer()

        # first image
        self.current_image = self.file_manager.random_image()
        self._draw_image(os.path.join(self.file_manager.directory, self.current_image))
        self.image_history.append(self.current_image)

        # start timer
        self._run_timer()

    def _run_timer(self):
        if self.timer_running:
            self._update_timer_label()
    
            if self.seconds_left >= 0:
                self.seconds_left -= 1
                self.timer_job = self.after(1000, self._run_timer)
            else:
                self._cycle_next(args=None)


    def _update_timer_label(self):
            m, s = divmod(self.seconds_left, 60) 
            self.timer_label.config(text=f"{m:02}:{s:02}")

    def _cycle_next(self, args):
        if self.history_index < len(self.image_history)-1:
            self.history_index = self.history_index + 1
            self._draw_image(os.path.join(self.file_manager.directory, self.image_history[self.history_index]))
            self._reset_timer()

            #print(f"old, len:{len(self.image_history)} i:{self.history_index}")

        else:
            self.current_image = self.file_manager.random_image()
            self._draw_image(os.path.join(self.file_manager.directory, self.current_image))

            if self.current_image:
                self.history_index = self.history_index + 1
                self._reset_timer()
                self.image_history.append(self.current_image)

                #print(f"NEW, len:{len(self.image_history)} i:{self.history_index}")

    def _cycle_previous(self, args):
        self.history_index = self.history_index - 1
        if self.history_index < 0:
            self.history_index = 0

        elif self.image_history:
            self._draw_image(os.path.join(self.file_manager.directory, self.image_history[self.history_index]))
            self._reset_timer()
            
            #print(f"len:{len(self.image_history)} i:{self.history_index}")

    def _reset_timer(self):
            self.seconds_left = self.seconds
            self.after_cancel(self.timer_job)
            self._update_timer_label()
            self._run_timer()

    def _toggle_pause(self, args):
        print("pause/unpause")

    def _setup_timer(self):
        style = ttk.Style()
        bg_color = style.lookup("TEntry", "fieldbackground")
        self.timer_label = tk.Label(self, text="04:20", fg="#eeeeee", bg=bg_color, font=("Courier New", 26), borderwidth=2, relief="ridge")
        self.timer_label.place(relx=1, rely=1, anchor="se", x=-20, y=-20)

    def _enter_fullscreen(self):
        
        self.attributes('-fullscreen', True)

        # push fullscreen to the front
        self.attributes('-topmost', 1)
        self.update_idletasks()
        self.wait_visibility(self)
        self.attributes('-topmost', 0)

        self.focus_force()

        style = ttk.Style()
        bg_color = style.lookup("TEntry", "fieldbackground")
        self.canvas = tk.Canvas(self, highlightthickness=0, bg = bg_color)
        self.canvas.pack(fill="both", expand=True)

    def _exit_fullscreen(self, args):
        self.destroy()
        self.parent.deiconify()

    def _image_queue(self):

        image = self.file_manager.random_image()
        self.image_history.append(image)

        self._draw_image(os.path.join(self.file_manager.directory, image))
        """
        if not image:
            raise ValueError(f"Directory has no images: {self.file_manager.directory}")
        """

    def _draw_image(self, image_path):
        image = Image.open(image_path)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        image.thumbnail((screen_width, screen_height), Image.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(image)

        self.canvas.create_image(screen_width//2, screen_height//2, image=self.tk_image, anchor="center")

    def _clear_canvas(self):
        self.canvas.delete("all")

