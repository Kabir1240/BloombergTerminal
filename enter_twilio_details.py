from tkinter import *
from tkinter import messagebox
from tkinter_widgets import TkinterWidgets
import json

FONT = ("Arial", 8, "bold")
TWILIO_CRED_PATH = "twilio_credentials.json"


class EnterTwilioCredentials:
    def __init__(self):
        # inform user that their account is being created
        messagebox.showinfo(title="Create Account", message="Could not find twilio_credentials.json, Please create "
                                                            "an account and enter the details here. Make sure to copy "
                                                            "them exactly")

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

        label_3 = Label(text="Account SID: ", font=FONT)
        label_4 = Label(text="Auth Token: ", font=FONT)
        label_5 = Label(text="From (Phone Number): ", font=FONT)
        label_6 = Label(text="To (Phone Number): ", font=FONT)

        # set label alignment
        label_3.grid(row=0, column=0, pady=5)
        label_4.grid(row=1, column=0, pady=5)
        label_5.grid(row=2, column=0, pady=5)
        label_6.grid(row=3, column=0, pady=5)

        # store in dict
        label_dict = {
            "account_sid": label_3,
            "auth_token": label_4,
            "from": label_5,
            "to": label_6,
        }

        # store in widgets
        self.widgets.add_label_dict(label_dict)

    def create_entries(self) -> None:
        """
        Creates entries and stores them in widgets
        :return: None
        """

        # create entries
        entry_3 = Entry(width=20)
        entry_4 = Entry(width=20)
        entry_5 = Entry(width=20)
        entry_6 = Entry(width=20)

        # align entries
        entry_3.grid(row=0, column=1, columnspan=2, pady=5)
        entry_4.grid(row=1, column=1, columnspan=2, pady=5)
        entry_5.grid(row=2, column=1, columnspan=2, pady=5)
        entry_6.grid(row=3, column=1, columnspan=2, pady=5)

        # store in dict
        entry_dict = {
            "account_sid": entry_3,
            "auth_token": entry_4,
            "from": entry_5,
            "to": entry_6,
        }

        # store in widgets
        self.widgets.add_entry_dict(entry_dict)

    def create_buttons(self) -> None:
        """
        creates a button, stores it in widgets
        :return: None
        """

        # create and align button
        button = Button(text="Create", font=FONT, command=self.save_account)
        button.grid(row=4, column=2)

        # store in widgets
        self.widgets.add_button(key="create", button=button)

    def save_account(self) -> None:
        """
        takes information input by user and stores it in json files
        :return: None
        """

        # gets user info
        account_sid = self.widgets.get_entries("account_sid").get()
        auth_token = self.widgets.get_entries("auth_token").get()
        from_number = self.widgets.get_entries("from").get()
        to_number = self.widgets.get_entries("to").get()

        # creates dictionary
        twilio_account = {
            "account_sid": account_sid,
            "auth_token": auth_token,
            "from_number": from_number,
            "to_number": to_number,
        }

        # stores dict in json file
        with open (TWILIO_CRED_PATH, 'w') as file:
            json.dump(twilio_account, file, indent=4)

        # informs user
        messagebox.showinfo(title="Account Created", message="Twilio credentials stored, close the pop ups")
