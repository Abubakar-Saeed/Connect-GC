import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage

HOST = "127.0.0.1"
PORT = 1234

WHITE = "white"
FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 12)
DARK_BLUE = "#02093d"
DEEP_BLUE = "#2b3595"
BLACK = "black"
DARK_GREY = "#181410"

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)
    message_box.yview(tk.END)  # Adjust the scrollbar to show the latest message


def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("Connect GC >> Welcome to Connect GC! Where connections came alive😁😁")
    except ConnectionError:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        formatted_name = ""
        for i in range(len(username)):
            if i == 0 or username[i - 1].isspace():
                formatted_name += username[i].upper()
            else:
                formatted_name += username[i].lower()
        client.sendall(formatted_name.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)


def clear_chat():
    message_box.config(state=tk.NORMAL)
    message_box.delete(1.0, tk.END)
    message_box.config(state=tk.DISABLED)


def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")


def on_entry_click(event):
    if username_textbox.get() == "Enter your username":
        username_textbox.delete(0, tk.END)
        username_textbox.config(fg='black')
    if message_textbox.get() == "Enter your message":
        message_textbox.delete(0, tk.END)
        message_textbox.config(fg='black')


def on_focus_out(event):
    if not username_textbox.get():
        username_textbox.insert(0, "Enter your username")
        username_textbox.config(fg='grey')
    if not message_textbox.get():
        message_textbox.insert(0, "Enter your message")
        message_textbox.config(fg='grey')


def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]
                add_message(f"{username} >> {content}")
        except ConnectionError:
            # Handle disconnection
            print("Server closed or connection lost.")
            messagebox.showinfo("Connection Closed", "The connection to the server has been closed.")
            window.destroy()
            break


# -----------------------------------------------User Interface----------------------------------------------------

window = tk.Tk()
window.geometry("625x700")
window.title("Connect GC")
window.resizable(False, False)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)

# ------------------------------------------------Logo Frame---------------------------------------------------------

logo_frame = tk.Frame(window, width=600, height=100, bg=DARK_BLUE)
logo_frame.grid(row=0, column=0, sticky=tk.NSEW)
logo_image = PhotoImage(file="Logo.png")
logo = tk.Label(logo_frame, bg=DARK_BLUE, image=logo_image)
logo.pack(side=tk.LEFT)

# ------------------------------------------------Top Frame----------------------------------------------------------

top_frame = tk.Frame(window, width=600, height=100, bg=DEEP_BLUE)
top_frame.grid(row=1, column=0, sticky=tk.NSEW)
username_label = tk.Label(top_frame, text="Enter username", font=FONT, bg=DEEP_BLUE, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)
username_textbox = tk.Entry(top_frame, font=("Helvetica", 15), bg=WHITE, fg=DARK_GREY, width=27)
username_textbox.pack(side=tk.LEFT, padx=15)
username_textbox.insert(0, "Enter your username")
username_textbox.bind("<FocusIn>", on_entry_click)
username_textbox.bind("<FocusOut>", on_focus_out)
username_textbox.bind("<Return>", lambda event=None: connect())
join_image = PhotoImage(file="join.png")
username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=DEEP_BLUE, image=join_image, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=30)

# ------------------------------------------------Middle Frame----------------------------------------------------------

middle_frame = tk.Frame(window, width=600, height=400, bg=BLACK)
middle_frame.grid(row=2, column=0, sticky=tk.NSEW)
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=BLACK, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.grid(row=0, column=0, sticky=tk.NSEW)

# ------------------------------------------------Bottom Frame----------------------------------------------------------

bottom_frame = tk.Frame(window, width=600, height=100, bg=DEEP_BLUE)
bottom_frame.grid(row=3, column=0, sticky=tk.NSEW)
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=WHITE, fg=DARK_GREY, width=40)
message_textbox.pack(side=tk.LEFT, padx=10)
message_textbox.bind("<Return>", lambda event=None: send_message())
message_textbox.insert(0, "Enter your message")
message_textbox.bind("<FocusIn>", on_entry_click)
message_textbox.bind("<FocusOut>", on_focus_out)
send_image = PhotoImage(file="send.png")
message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=DEEP_BLUE ,image=send_image, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=20)
clear_image = PhotoImage(file="clear.png")
clear_button = tk.Button(bottom_frame, text="Clear Chat", font=BUTTON_FONT, fg=WHITE, bg=DEEP_BLUE, image=clear_image, command=clear_chat)
clear_button.pack(side=tk.LEFT)

# ------------------------------------------------Footer Frame----------------------------------------------------------

footer_frame = tk.Frame(window, width=600, height=30, bg=DARK_BLUE)
footer_frame.grid(row=4, column=0, sticky=tk.NSEW)
footer_lable = tk.Label(footer_frame, text="Developed by Abubakar Saeed 😎", fg=WHITE, bg=DARK_BLUE, font=("Sans-serif", 11))
footer_lable.pack()


def main():
    window.mainloop()


if __name__ == '__main__':
    main()
