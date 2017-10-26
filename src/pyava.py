from tkinter import messagebox
import configparser
import os
import subprocess
import tkinter


class Pyava:
    """
    The main window of a simple emulator launcher.
    """
    def __init__(self, master):
        self.main_window = master
        self.main_window_design()
        self.set_main_window_bindings()
        self.load_from_ini()

    def main_window_design(self):
        """
        Design the main window.
        """
        # Create the main window
        self.main_window.geometry("{}x{}".format(900, 600))
        self.main_window.minsize(width=300, height=200)
        self.main_window.iconbitmap("icon.ico")
        self.main_window.title("Pyava")

        # Set rows and columns weight
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(2, weight=3)
        self.main_window.rowconfigure(1, weight=1)

        # Create labels and lists
        self.platforms_label = tkinter.Label(
            self.main_window,
            text="Platforms"
        )
        self.platforms_label.grid(row=0, column=0)
        self.platforms_list = tkinter.Listbox(
            self.main_window,
            activestyle="none",
            exportselection=0
        )
        self.platforms_list.grid(row=1, column=0, sticky="nsew")

        self.games_label = tkinter.Label(self.main_window, text="Games")
        self.games_label.grid(row=0, column=2)
        self.games_list = tkinter.Listbox(
            self.main_window,
            activestyle="none",
            exportselection=0
        )
        self.games_list.grid(row=1, column=2, sticky="nsew")

        # Set the initial focus on the platforms list
        self.platforms_list.focus_set()

        # Create the scrollbars and attach them to the lists
        self.platforms_scrollbar = tkinter.Scrollbar(self.main_window)
        self.platforms_scrollbar.grid(row=1, column=1, sticky="nsew")
        self.games_scrollbar = tkinter.Scrollbar(self.main_window)
        self.games_scrollbar.grid(row=1, column=3, sticky="nsew")

        self.platforms_list.config(yscrollcommand=self.platforms_scrollbar.set)
        self.platforms_scrollbar.config(command=self.platforms_list.yview)
        self.games_list.config(yscrollcommand=self.games_scrollbar.set)
        self.games_scrollbar.config(command=self.games_list.yview)

    def set_main_window_bindings(self):
        """
        Set the bindings of the main window.
        """
        self.main_window.bind("<Control-r>", self.reload_from_ini)
        self.main_window.bind("<Control-a>", self.about_program)
        self.main_window.bind(
            "<Control-s>",
            self.set_custom_separator
        )
        self.main_window.bind("<Escape>", self.quit_program)

    def load_from_ini(self):
        """
        Check if config.ini exists and if it's not empty,
        then load the program.
        """
        # Check if confing.ini exists
        if not os.path.isfile("config.ini"):
            self.show_error(0)
        else:
            # Get the sections from config.ini
            self.config = configparser.ConfigParser()
            self.config.read("config.ini")
            self.sections = self.config.sections()

            # Check if config.ini is empty
            if not self.sections:
                self.show_error(1)
            else:
                self.set_lists_bindings()
                self.display_platforms()
                self.default_platform_selection()

    def set_lists_bindings(self):
        """
        Set the bindings of the platforms list and of the games list.
        """
        self.platforms_list.bind(
            "<<ListboxSelect>>",
            self.on_platform_selection
        )
        self.games_list.bind("<Double-Button-1>", self.on_game_selection)
        self.games_list.bind("<Return>", self.on_game_selection)

    def display_platforms(self):
        """
        Display the platforms.
        """
        for i in self.sections:
            self.platforms_list.insert("end", i)

        # Select the first platform in the list
        self.platforms_list.select_set(0)

    def default_platform_selection(self):
        """
        Show the games of the default platform.
        """
        self.platform = self.sections[0]

        self.parameters_separator = ","
        self.parameters_already_splitted = False

        self.check_options()

    def get_required_options_from_ini(self):
        """
        Get the options from config.ini.
        """
        self.games_folder = self.config.get(self.platform, "games")
        self.executable = self.config.get(self.platform, "executable")
        self.extensions = self.config.get(self.platform, "extensions")

    def check_options(self):
        """
        Check if required options are present
        """
        # Check if required options are present
        if self.config.has_option(self.platform, "games") is False:
            self.show_error(2)
        elif self.config.has_option(self.platform, "executable") is False:
            self.show_error(3)
        elif self.config.has_option(self.platform, "extensions") is False:
            self.show_error(4)
        else:
            self.get_required_options_from_ini()

            if not self.games_folder:
                self.show_error(2)
            elif not self.executable:
                self.show_error(3)
            elif not self.extensions:
                self.show_error(4)
            else:
                # Split the extensions
                self.extensions = [
                    i.strip() for i in self.extensions.split(",")
                ]

                self.display_games()

    def display_games(self):
        """
        Show the games in the games list.
        """
        for i in os.listdir(self.games_folder):
            # Get the name and the extension of the game
            game_name, game_extension = os.path.splitext(i)

            if game_extension in self.extensions:
                self.games_list.insert("end", i)

        # Select the first game in the list
        self.games_list.select_set(0)

    def on_platform_selection(self, platform_event):
        """
        Show the games of the selected platform.
        """
        # Clear the games list
        self.games_list.delete(0, "end")

        # Get the platform selection from the platforms list
        self.platform_selection = platform_event.widget.curselection()
        self.platform = platform_event.widget.get(self.platform_selection[0])

        self.parameters_separator = ","
        self.parameters_already_splitted = False

        self.check_options()

    def on_game_selection(self, game_event):
        """
        Launch the emulator.
        """
        # Get the game selection from the games list
        self.game_selection = game_event.widget.curselection()
        self.game = game_event.widget.get(self.game_selection[0])

        # Create the full path
        self.full_path = self.games_folder + self.game

        self.get_parameters_from_ini()

        # Launch the emulator
        subprocess.run(
            [
                r"%s" % (self.executable),
                r"%s" % (self.full_path),
            ] + self.parameters
        )

    def set_custom_separator(self, key_pressed):
        """
        Let the user insert a custom separator for splitting parameters.
        """
        self.set_separator = SetSeparator(self.main_window)

        # Open the pop-up
        self.main_window.wait_window(self.set_separator.separator_pop_up)

        # Check if the separator has benn inserted correctly
        try:
            self.set_separator.custom_separator
        except AttributeError:
            pass
        else:
            self.parameters_separator = self.set_separator.custom_separator

            if self.parameters_separator == "":
                self.parameters_separator = ","

        self.parameters_already_splitted = False

    def get_parameters_from_ini(self):
        """
        Get the parameters from config.ini.
        """
        if self.parameters_already_splitted is False:
            if self.config.has_option(self.platform, "parameters") is False:
                self.parameters = ""
            else:
                self.parameters = self.config.get(self.platform, "parameters")

            self.split_parameters()

    def split_parameters(self):
        """
        Split the parameters.
        """
        self.parameters = [
            j.strip() for j in self.parameters.split(self.parameters_separator)
        ]
        self.parameters_already_splitted = True

    def reload_from_ini(self, key_pressed):
        """
        Reload information from config.ini.
        """
        # Clear the platforms list and the games list
        self.platforms_list.delete(0, "end")
        self.games_list.delete(0, "end")

        # Set the focus on the platforms list
        self.platforms_list.focus_set()

        self.load_from_ini()

    def quit_program(self, key_pressed):
        """
        Quit the program.
        """
        self.main_window.quit()
        self.main_window.destroy()
        exit()

    def about_program(self, key_pressed):
        """
        Show an information message.
        """
        messagebox.showinfo(
            "About",
            "Pyava\n" +
            "A simple emulator launcher written in Python.\n" +
            "Made with ❤ by Giacomo Poggi.\n" +
            "Version: 1.0\n" +
            "Website: github.com/giacomopoggi/pyava"
        )

    def show_error(self, type_of_error):
        """
        Show an error.
        """
        self.error_message = {
            0: "Your config.ini is missing.",
            1: "Your config.ini is empty.",
            2: "The selected platform is missing the \"games\" option.",
            3: "The selected platform is missing the \"executable\" option.",
            4: "The selected platform is missing the \"extensions\" option.",
        }

        messagebox.showerror("Error", self.error_message[type_of_error])


class SetSeparator:
    """
    A pop-up window to set a custom separator for splitting parameters.
    """
    def __init__(self, master):
        self.separator_pop_up = tkinter.Toplevel(master)
        self.separator_pop_up_design()
        self.separator_pop_up_bindings()

    def separator_pop_up_design(self):
        """
        Design the pop-up.
        """
        self.separator_pop_up.iconbitmap("icon.ico")

        self.separator_pop_up.columnconfigure(0, weight=0)
        self.separator_pop_up.columnconfigure(1, weight=1)
        self.separator_pop_up.rowconfigure(1, weight=1)

        self.insert_label = tkinter.Label(
            self.separator_pop_up,
            text="Insert your custom separator:"
        )
        self.insert_label.grid(row=0, column=0, sticky="nsew")

        self.separator_entry = tkinter.Entry(self.separator_pop_up)
        self.separator_entry.grid(row=0, column=1, sticky="nsew")
        self.separator_entry.focus_set()

    def separator_pop_up_bindings(self):
        """
        Set the bindings of the pop-up.
        """
        self.separator_entry.bind("<Return>", self.get_separator_value)

    def get_separator_value(self, key_pressed):
        """
        Get the value of the custom separator.
        """
        self.custom_separator = self.separator_entry.get()

        self.separator_pop_up.destroy()

tk_gui = tkinter.Tk()
start_gui = Pyava(tk_gui)
tk_gui.mainloop()
