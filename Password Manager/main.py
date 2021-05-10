import tkinter as tk
from tkinter import messagebox
from password_generator import generate
import json
# import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password = generate()
    password_input.insert(0, password)
    # pyperclip.copy(pasword)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():

    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if not website or not email or not password:
        messagebox.showinfo(title='Oops', message="Please don't leave any fields empty!")

    else:
        try:
            with open("data.json", 'r') as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", 'w') as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, 'end')
            password_input.delete(0, 'end')


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_input.get()
    email = email_input.get()

    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title=website, message="No Data File Found")
    else:
        if website in data and email in data[website]["email"]:
            messagebox.showinfo(
                title=website,
                message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}"
            )
        else:
            messagebox.showinfo(title="Error", message=f"No details for the {website} exits")

# ---------------------------- UI SETUP ------------------------------- #


window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = tk.Canvas(width=200, height=200)
logo_img = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_input = tk.Entry(width=21)
website_input.grid(row=1, column=1, sticky="EW")
website_input.focus()

email_input = tk.Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2, sticky="EW")
email_input.insert(0, 'email@gmail.com')

password_input = tk.Entry(width=21, show="*")
password_input.grid(row=3, column=1, sticky='EW')

# Buttons
search_btn = tk.Button(text='Search', width=13, command=find_password)
search_btn.grid(row=1, column=2)

generate_btn = tk.Button(text='Generate Password', command=generate_password)
generate_btn.grid(row=3, column=2, sticky='EW')

add_btn = tk.Button(text='Add', width=36, command=save_password)
add_btn.grid(row=4, column=1, columnspan=2, sticky='EW')

window.mainloop()
