from ui import MekuGesture
import os
import argparse

from file_manager import FileManager

def main():

    parser = argparse.ArgumentParser()
    #TODO: implement CLI

    initial_directory = os.path.dirname(os.path.abspath(__file__))
    file_manager = FileManager(initial_directory, 60)
    app = MekuGesture(file_manager)

    app.mainloop()


if __name__ == "__main__":
    main()