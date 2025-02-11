import sqlite3
import os
import random
from PIL import Image


class FileManager:

    def __init__(self, initial_directory, initial_seconds):

        self.directory = initial_directory
        self.seconds = initial_seconds

        self.all_images = self._update_all_images()
        self.used_images = []

    def random_image(self):
        if not self.all_images:
            return None
        
        cold_storage = list(set(self.all_images) - set(self.used_images))

        image = random.choice(cold_storage)
        return image

    def update_directory(self, new_directory):

        if not os.path.isdir(new_directory):
            raise ValueError(f"Invalid directory: {new_directory}")
        
        if self._are_directories_different(self.directory, new_directory):
            print(f"updated dir from {self.directory} to {new_directory}")
            self.directory = new_directory
            self._update_all_images()

    def update_seconds(self, new_seconds):
        
        if not new_seconds.isdigit():
            raise ValueError(f"Invalid integer: {new_seconds}")
        
        print(f"updated seconds from {self.seconds} to {new_seconds}")
        self.seconds = new_seconds

    def _update_all_images(self): 
        return [entry.name for entry in os.scandir(self.directory)
                if entry.is_file() and self._is_openable_image(entry.path)]

    def _is_openable_image(self, filepath):
        try:
            with Image.open(filepath) as img:
                img.verify()
                return True
        except Exception:
            return False

    def _are_directories_different(self, dir1, dir2):
        try: 
            return not os.path.samefile(dir1, dir2)
        except FileNotFoundError:
            return True