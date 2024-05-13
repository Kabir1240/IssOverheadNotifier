from tkinter import *
from tkinter_widgets import TkinterWidgets
from tkinter import messagebox

FONT = ("Arial", 8, "bold")
FILE_PATH = "data/user_account.json"
import json

class CreateAccount:
    def __init__(self):
        # inform user that their account is being created
        messagebox.showinfo(title="Create Account", message="You don't have an account, create one.")

        # create window
        self.window = Tk()
        self.window.title("Add Account")
        self.window.config(padx=15, pady=15)

        # create widgets and widget data struct
        self.widgets = TkinterWidgets()
        self.create_labels()
        self.create_entries()
        self.create_buttons()

        # main loop for window
        self.window.mainloop()

    def create_labels(self) -> None:
        """
        Creates labels and stores them in widgets
        :return: None
        """

        # 3 labels
        label_1 = Label(text="Name: ", font=FONT)
        label_2 = Label(text="Email: ", font=FONT)
        label_3 = Label(text="Password: ", font=FONT)
        label_4 = Label(text="latitude: ", font=FONT)
        label_5 = Label(text="longitude: ", font=FONT)

        # set label alignment
        label_1.grid(row=0, column=0, pady=5)
        label_2.grid(row=1, column=0, pady=5)
        label_3.grid(row=2, column=0, pady=5)
        label_4.grid(row=3, column=0, pady=5)
        label_5.grid(row=4, column=0, pady=5)

        # store in dict
        label_dict = {
            "name": label_1,
            "email": label_2,
            "password": label_3,
            "lat": label_4,
            "long": label_5,
        }

        # store in widgets
        self.widgets.add_label_dict(label_dict)

    def create_entries(self) -> None:
        """
        Creates entries and stores them in widgets
        :return: None
        """

        # create entries
        entry_1 = Entry(width=20)
        entry_2 = Entry(width=20)
        entry_3 = Entry(width=20)
        entry_4 = Entry(width=20)
        entry_5 = Entry(width=20)

        # align entries
        entry_1.grid(row=0, column=1, columnspan=2, pady=5)
        entry_2.grid(row=1, column=1, columnspan=2, pady=5)
        entry_3.grid(row=2, column=1, columnspan=2, pady=5)
        entry_4.grid(row=3, column=1, columnspan=2, pady=5)
        entry_5.grid(row=4, column=1, columnspan=2, pady=5)

        # store in dict
        entry_dict = {
            "name": entry_1,
            "email": entry_2,
            "password": entry_3,
            "lat": entry_4,
            "long": entry_5,
        }

        # store in widgets
        self.widgets.add_entry_dict(entry_dict)

    def create_buttons(self) -> None:
        """
        creates a button, stores it in widgets
        :return: None
        """

        # create and align button
        button = Button(text="Create", font=FONT, command=self.save_email)
        button.grid(row=5, column=2)

        # store in widgets
        self.widgets.add_button(key="create", button=button)

    def save_email(self) -> None:
        """
        takes information input by user and stores it in a json file
        :return: None
        """

        # gets user info
        name = self.widgets.get_entries("name").get()
        email = self.widgets.get_entries("email").get()
        password = self.widgets.get_entries("password").get()
        lat = self.widgets.get_entries("lat").get()
        long = self.widgets.get_entries("long").get()

        # creates dict
        account = {
            "name": name,
            "email": email,
            "password": password,
            "lat": lat,
            "long": long,
        }

        # stores dict in json file
        with open (FILE_PATH, 'w') as file:
            json.dump(account, file, indent=4)

        # informs user
        messagebox.showinfo(title="Account Created", message="Account created, close the pop ups")
