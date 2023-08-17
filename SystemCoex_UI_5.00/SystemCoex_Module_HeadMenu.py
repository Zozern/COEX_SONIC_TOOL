import tkinter as tk

class systemcoex_head_menu_module():
    def __init__(self, window):
        self.main_window = window


    def create_head_menu(self):
        top = self.main_window.winfo_toplevel()        




    def add_quit_button(self, menu_widget):
        menu_widget.add_command(label='Quit', command=self.main_window.quit)
