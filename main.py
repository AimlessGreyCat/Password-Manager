import random
from tkinter import *
from tkinter import messagebox
import pyperclip
import json

CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'w', 'x', 'y', 'z']
NUMS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
FILENAME = 'data.json'


def save():
    def clear():
        website_entry.delete(0, END)
        # username_email_entry.delete(0, END)
        password_entry.delete(0, END)

    website = website_entry.get()
    username_email = username_email_entry.get()
    password = password_entry.get()
    new_entry = {
        website:
            {
                "username/email": username_email,
                "password": password,
            }
    }
    if not website or not username_email or not password:
        messagebox.showerror(title="ERROR", message="Please ensure all fields are filled out.")
    else:
        try:
            with open(file=FILENAME, mode='r') as file:
                data = json.load(file)
                data.update(new_entry)
            with open(file=FILENAME, mode='w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(file=FILENAME, mode='w') as file:
                json.dump(new_entry, file, indent=4)
        finally:
            clear()


def find_password():
    def format_message(input_website, input_details):
        return f"Website: {input_website}\nUsername/Email: {input_details['username/email']}\n" \
               f"Password: {input_details['password']}"

    website = website_entry.get()
    try:
        with open(file=FILENAME, mode='r') as file:
            data = json.load(file)[website]
    except (FileNotFoundError, KeyError):
        messagebox.showerror(title="Not found", message=f"Entry for website, {website} does not exist.")
    else:
        will_copy = messagebox.askyesno(title="Details", message=f"{format_message(website, data)}\n\n"
                                                                 f"Would you like to copy password to clipboard?")
        if will_copy:
            pyperclip.copy(data['password'])


def generate_password():
    chars = random.randint(4, 6)
    chars_upper = random.randint(1, 2)
    nums = random.randint(2, 4)
    symbols = random.randint(2, 4)

    password_list = []
    password_list += ([random.choice(CHARS) for _ in range(chars)])
    password_list += ([random.choice(CHARS).upper() for _ in range(chars_upper)])
    password_list += ([random.choice(NUMS) for _ in range(nums)])
    password_list += ([random.choice(SYMBOLS) for _ in range(symbols)])
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(index=0, string=password)
    pyperclip.copy(password)


screen = Tk()
screen.title("Password Manager")
screen.config(padx=50, pady=20)
LOGO_IMG = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
logo = canvas.create_image(100, 100, image=LOGO_IMG)
canvas.grid(sticky=W, column=1, row=1)

LABEL_FONT = ("Arial", 8, "bold")

website_label = Label(text="Website: ", font=LABEL_FONT)
website_label.grid(column=0, row=2)
website_entry = Entry(justify="left", width=24)
website_entry.focus()
website_entry.grid(sticky=W, column=1, row=2, columnspan=2)
website_button = Button(text="Search", width=14, command=find_password)
website_button.grid(sticky=E, column=1, row=2, columnspan=2)

username_email_label = Label(text="Username/Email: ", font=LABEL_FONT)
username_email_label.grid(column=0, row=3)
username_email_entry = Entry(width=35)
username_email_entry.grid(sticky=W, column=1, row=3, columnspan=2)

password_label = Label(text="Password: ", font=LABEL_FONT)
password_label.grid(column=0, row=4)
password_entry = Entry(width=24)
password_entry.grid(sticky=W, column=1, row=4)
password_button = Button(text="Generate Password", width=14, command=generate_password)
password_button.grid(sticky=E, column=1, row=4, columnspan=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(sticky=W, column=1, row=5, columnspan=2)

screen.mainloop()
