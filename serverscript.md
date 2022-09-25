# Chat-Application
# A simple chat application using Python and MySql 
# server script
import socket
import mysql.connector as mys
from tkinter import *
from _thread import *
from datetime import datetime
import random
def proccess(none):
    username_list = []
    details = a.recv(1024)
    details = details.decode()
    details = eval(details)

    is_active.append(details[1])
    mc.execute("SELECT * FROM loginid")
    content = mc.fetchall()
    users = []

    if details[0] == '1':
        for i in content:

            if details[1] == i[1] and details[2] == i[2]:
                a.send("1".encode())
                is_active.append(details[1])

                for i in content:
                    users.append((i[0], i[1]))

                for i in users:
                    if i[1] != details[1]:
                        username_list.append(i[1])

                a.send(str(username_list).encode())
                start_new_thread(send_message_live, (details[1],))

                while True:
                    what_to_do = eval(a.recv(1024).decode())
                    if what_to_do[0] == "1":
                        selected_user = what_to_do[1]
                        selected_user_chat(selected_user, details[1])

                    elif what_to_do[0] == '2':
                        recive_messages(
                            details[1], what_to_do[1], what_to_do[2])

                    elif what_to_do[0] == "__close__":
                        a.close
                        print("closed")
        else:
            a.send("2".encode())
            proccess(None)

    elif details[0] == '2':
        mc.execute(
            f"insert into loginid values('{1}','{details[1]}','{details[2]}');")
        mydb.commit()
        a.send("3".encode())
        proccess(None)


def user_seection(username_list, current_user):
    selected_user = a.recv(1024)
    selected_user = selected_user.decode()
    selected_user_chat(selected_user, current_user)
    return selected_user


def selected_user_chat(selected_user, current_user):
    print(selected_user, current_user)
    mc.execute("select * from message_file")
    file_name = mc.fetchall()
    for i in file_name:

        if (i[0] == current_user and i[1] == selected_user) or (i[0] == selected_user and i[1] == current_user):

            with open(
                    f"C:\\pycharm\\pythonProject\\chat_room\\chat_record\\{i[2]}.txt", "r") as text_file:
                old_messages = text_file.readlines()
                # a.send(str(old_messages).encode())
                for i in old_messages:
                    a.send(str(i).encode())


def recive_messages(current_user, selected_user, message):
    Recived_message = message

    if selected_user in is_active:
        print("user is online")
        recive_message_live(selected_user, message)

    if Recived_message:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        mc.execute("select * from message_file")
        file_name = mc.fetchall()

        status = "false"

        for i in file_name:

            if(i[0] == current_user and i[1] == selected_user) or (i[0] == selected_user and i[1] == current_user):

                with open(
                        f"C:\\pycharm\\pythonProject\\chat_room\\chat_record\\{i[2]}.txt", "a") as text_file:
                    text_file.write("\n")
                    text_file.write(
                        f"{current_time} {current_user}  >  {Recived_message}")
                    status = "true"

        if status == "false":

            file_characters = "1234567890qwertyuiopasdfghjklzxcvbnm"
            file_name = []
            for i in range(5):
                file_name.append(random.choice(file_characters))
            name = "".join(file_name)

            st = f"insert into message_file values ('{selected_user}','{current_user}','{name}')"

            mc.execute(st)
            mydb.commit()

            with open(f"C:\\pycharm\\pythonProject\\chat_room\\chat_record\\{name}.txt", "a") as text_file:
                text_file.write("\n")
                message_str = f"{current_time} {current_user}  >  {Recived_message}"
                text_file.write(message_str
                                )


def recive_message_live(selected_user, message):
    incoming_message.append([selected_user, message])
    print("message appended")


def send_message_live(current_user):

    while True:

        for i in incoming_message:

            if i[0] == current_user:
                print("current user found")
                a.send(str(i[1]).encode())
                incoming_message.remove(i)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 8950))
print("Server running...")
server.listen(10)
mydb = mys.connect(host='localhost', user='root',
                   password='mysqlrootpassword', database='login')
mc = mydb.cursor()

is_active = []
incoming_message = []

while True:
    a, addrs = server.accept()
    print(f"connected with {addrs} !")

    try:
        thread = start_new_thread(proccess, (None,))
    except:
        continue
