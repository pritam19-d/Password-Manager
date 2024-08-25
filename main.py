from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generated_pwd():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    pwd_letter = [choice(letters) for i in range(randint(8,10))]
    pwd_symbol = [choice(symbols) for i in range(randint(3,5))]
    pwd_number = [choice(numbers) for i in range(randint(2,4))]

    pwd_list = pwd_letter + pwd_symbol + pwd_number
    shuffle(pwd_list)
    return "".join(pwd_list)

def generate_handler():
    password_input.delete(0, END)
    new_pwd = generated_pwd()
    password_input.insert(END, f"{new_pwd}")
    pyperclip.copy(new_pwd)

# ---------------------------- SEARCH ALGORITHM ------------------------------- #

def search_handler():
    search_item = website_input.get().title()
    try:
        with open("PasswordManager.json", "r") as password_manager:
            manager_list = json.load(password_manager)
    except FileNotFoundError:
        messagebox.showwarning(title="No File", message="There's no previous record present in our local database")
    else:
        if search_item in manager_list:
            messagebox.showinfo(title=search_item,
                                message=f"Email / ID: {manager_list[search_item]["email"]}\n"
                                        f"Password: {manager_list[search_item]["password"]}"
                                )
        else:
            messagebox.showinfo(title="No Data", message="The enterd data doesn't exists our database, please try to add one.")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    input_data = [website_input.get().title(), username_input.get().lower(), password_input.get()]
    json_data = {
        input_data[0]: {
            "email": input_data[1],
            "password": input_data[2]
        }
    }
    if len(input_data[0]) == 0 or len(input_data[1]) == 0 or len(input_data[2]) == 0:
        messagebox.showwarning(title="Warning", message="Please fill all the fields before saving.")
    else:
        if messagebox.askokcancel(title="Confirm?", message=f"Website: {input_data[0]},\nUserID: {input_data[1]},\nPassword: {input_data[2]}.\nAre you sure to save the above data?"):
            try:
                with open("PasswordManager.json", "r") as password_manager:
                    data = json.load(password_manager)
            except FileNotFoundError:
                with open("PasswordManager.json", "w") as password_manager:
                    json.dump(json_data, password_manager, indent=4)
            else:
                data.update(json_data)
                with open("PasswordManager.json", "w") as password_manager:
                    json.dump(data, password_manager, indent=4)
            finally:
                with open("PasswordManager.csv", "a") as pwd_manager:
                    pwd_manager.write(f"{input_data[0]},{input_data[1]},{input_data[2]}\n")
                website_input.delete(0, END)
                password_input.delete(0, END)
                website_input.focus()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")

window.config(padx=20, pady=20)
canvas = Canvas(width=180, height= 180, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")

canvas.create_image(90, 90, image=logo_img)
website_label = Label(text="Website :", font=("Arial", 10))
username_label = Label(text="Email / Username :", font=("Arial", 10))
password_label = Label(text="Password :", font=("Arial",10))

website_input = Entry(width=29)
username_input = Entry(width=48)
password_input = Entry(width=29)

search_button = Button(text="Search", font=("Arial", 8), width=17, command=search_handler)
generate_button = Button(text="Generate Password", font=("Arial", 8), width=17, command=generate_handler)


canvas.grid(column="1", row="0")
website_label.grid(column="0", row="1")
website_input.grid(column="1", row="1")
website_input.focus()
username_label.grid(column="0", row="2")
username_input.grid(column="1", row="2", columnspan=2)
username_input.insert(END, "pritam.das19@gmail.com")
password_label.grid(column="0", row="3")
password_input.grid(column="1", row="3")

search_button.grid(column="2", row="1")
generate_button.grid(column="2", row="3")

add_button = Button(text="Save",font=("Arial", 10, "bold"), width=50, command=save_data)
add_button.grid(column="0", row="4", columnspan=3)

window.mainloop()