from email.mime import image
import socket
from tkinter import*
from _thread import *
from PIL import Image, ImageTk
from datetime import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 8950))


def recive_message(l11, send):
    send.place(x=460, y=613)
    while True:
        message = server.recv(1024).decode()
        #message = eval(message)
        l11.insert(END, message)


def send_message(e1, l1):
    message = e1.get()
    Message_To_Send = str(["2", selected_user[-1], message])
    server.send(Message_To_Send.encode())
    e1.delete(0, END)

    now = datetime.now()
    current_time = now.strftime("%H:%M")
    mess_format = f"{current_time} {my_username} > {message}"
    l1.insert(END, mess_format)


def server_close(main):

    server.send(str((["__close__"])).encode())
    server.close()
    main.destroy()


def cursor(l1, l11, send):
    l11.delete(0, END)
    for i in l1.curselection():

        selected_user.append(l1.get(i))
        select = str(["1", l1.get(i)])
        select = select.encode()
        server.send(select)
    t = start_new_thread(recive_message, (l11, send))


def username_window():
    main = Tk()
    main.geometry('535x645')
    main.title('Log in')

    #main.resizable(False, False)

    img = ImageTk.PhotoImage(Image.open("img.png"))
    l4 = Label(main, image=img)
    l4.place(x=0, y=0)

    b1 = Button(main, text='select', font=' Helvetica,7,bold',
                bg='ivory3', fg='black', width=10, command=lambda: cursor(l1, l11, b22)).place(x=0, y=0)
    l11 = Listbox(main, font=' Helvetica,17',
                  bg='cyan', fg='black', height=32, width=50)
    l11.place(x=95, y=0)

    l1 = Listbox(main, font=' Times,40',
                 bg='LightBlue2', fg='black', height=35, width=10)
    l1.place(x=0, y=30)
    names = server.recv(1024).decode()
    names = eval(names)
    for i in names:
        l1.insert(END, i)

    b11 = Button(main, text="close", font=' Helvetica,7,bold',
                 bg='ivory3', fg='black', width=9, command=lambda: server_close(main)).place(x=445, y=0)

    e1 = Entry(main, width=40, bg='seashell2',
               fg='black', font=' Helvetica,15')
    e1.place(x=95, y=620)

    b22 = Button(main, text='send', font=' Helvetiva,7,bold',
                 bg='ivory3', fg='black', width=8, command=lambda: send_message(e1, l11))

    main.mainloop()


def login(e1, e2, main):
    my_username = e1.get()
    details = ["1", my_username, e2.get()]
    details = str(details).encode()
    server.send(details)
    print("sent....")
    recived_code = server.recv(1024).decode()
    if recived_code == "1":
        print("success")
        main.destroy()
        username_window()
    elif recived_code == "2":
        error_label = Label(main, text="Details did'nt match",
                            bg='black', fg='white').place(x=480, y=242)
        print("didnt match")
    else:
        print("some other error")


def signup(main):
    main.destroy()
    new_win = Tk()
    new_win.title('Sign up')

    # new_win.geometry('1500x800')
    new_win.attributes('-fullscreen', True)
    img = ImageTk.PhotoImage(Image.open(
        r"C:\Users\varun jain\Documents\PENDRIVE DOCS\Latest\New folder\img.png"))
    l4 = Label(new_win, image=img)
    l4.pack(side="top", fill="y", expand="yes")

    new_win.configure(bg='black', cursor='arrow blue',)
    new_win.resizable(False, False)
    new_win.title("sign up")
    new_win.geometry('1500x800')

    e1 = Label(new_win, text="USERNAME:", font=' Helvetica,15',
               bg='black', fg='white').place(x=560, y=250)
    l2 = Label(new_win, text='PASSWORD:', font=' Helvetica,15',
               bg='black', fg='white').place(x=560, y=290)
    e1 = Entry(new_win, bg='black', fg='white',
               font=' Helvetica,15')
    e1.place(x=670, y=250)
    e2 = Entry(new_win, bg='black', fg='white',
               font=' Helvetica,15')
    e2.place(x=670, y=290)
    b1 = Button(new_win, text="SIGN UP", font=' Helvetica,8',
                bg='black', fg='white', command=lambda: sign_up_proccess(e1, e2, new_win)).place(x=700, y=350)
    new_win.mainloop()


def sign_up_proccess(e1, e2, new_win):
    details = ["2", e1.get(), e2.get()]
    details = str(details).encode()
    server.send(details)
    recived_code = server.recv(1024).decode()
    if recived_code == "3":
        print("success")
        new_win.destroy()
        login_window()
    elif recived_code == "4":
        print("already used")
    elif recived_code == "5":
        print("Error")


def login_window(app):
    app.destroy()
    main = Tk()
    main.title('chatroom user')
    img = ImageTk.PhotoImage(Image.open(
        r"C:\Users\varun jain\Documents\PENDRIVE DOCS\Latest\New folder\img.png"))
    l4 = Label(main, image=img)
    l4.pack(side="top", fill="y", expand="yes")
    main.resizable(False, False)
    main.attributes('-fullscreen', True)
    l1 = Label(main, text='USERNAME:', font=' Helvetica,15',
               bg='black', fg='white').place(x=560, y=250)
    l2 = Label(main, text='PASSWORD:', font=' Helvetica,15',
               bg='black', fg='white').place(x=560, y=290)
    e1 = Entry(main, bg='black', fg='white', font=' Helvetica,15')
    e1.place(x=670, y=250)
    e2 = Entry(main, bg='black', fg='white', font=' Helvetica,15')
    e2.place(x=670, y=290)
    b1 = Button(main, text="LOG IN", font=' Helvetica,8', bg='black',
                fg='white', command=lambda: login(e1, e2, main)).place(x=705, y=350)
    l3 = Label(main, text="Dont have an account ? create one now :",
               font=' Helvetica,8', bg='black', fg='white').place(x=580, y=400)
    b2 = Button(main, text='SIGN UP', font=' Helvetica,2',
                bg='black', fg='white', command=lambda: signup(main)).place(x=700, y=447)
    main.mainloop()


def welcome():
    main = Tk()
    main.title('chatroom user')
    img = ImageTk.PhotoImage(Image.open(
        r"C:\Users\varun jain\Documents\PENDRIVE DOCS\Latest\New folder\img.png"))
    l4 = Label(main, image=img)
    l4.place(x=0, y=0)
    main.resizable(False, False)
    main.attributes('-fullscreen', True)
    wel = Label(main, text="welcome to chatroom !", font=(
        'Helvetica', 50), bg='black', fg='white').place(x=400, y=300)
    nxt = Button(main, text="continue ->>", bg='black', fg='white',
                 font=('Helvetica', 20), command=lambda: login_window(main)).place(x=650, y=500)
    main.mainloop()


my_username = ""
selected_user = []
welcome()
