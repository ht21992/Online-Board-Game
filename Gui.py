from socket import *
from threading import *
from tkinter import *
import tkinter.scrolledtext as tkscrolled
from tkinter import simpledialog
import random
import time
import os
from PIL import Image, ImageTk
import pickle
from suspects import sus_info

suspects, main_sus, hints, used_positions = sus_info()




# Socket Information
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
hostIp = "127.0.0.1"
portNumber = 7500
clientSocket.connect((hostIp, portNumber))


# Prepare question numbers
def load_question_numbers():
    with open("question_numbers", 'rb') as f:
        question_numbers = pickle.load(f)
    return question_numbers


question_numbers = load_question_numbers()


# Dice Images
dice_images = []
path = "dice/"
valid_images = [".jpg"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    dice_images.append(Image.open(os.path.join(path, f)).resize((50, 50)))


# Suspect Images
sus_images = []
path = "suspects_img/"
valid_images = [".jpg"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    sus_images.append(Image.open(os.path.join(path, f)).resize((60, 60)))

# Widget Information
widgets = {"ovals": []}


# Information about the game
signals = {}
player_info = {'currentPosition': 1, 'opponentCurrentPosition': 1}


class Main:

    def __init__(self, main_window):
        self.window = main_window
        self.nickname = "No Name"
        self.nickname_popup_window()
        self.window.withdraw()
        # Creating left and right Frame
        self.left_frame = Frame(main_window, width=750, height=500, cursor="circle")
        self.left_frame.grid(row=1, column=0, padx=10, pady=5)
        self.right_frame = Frame(main_window, width=300, height=550)
        self.right_frame.grid(row=1, column=1, padx=10, pady=5)




        # Content inside left frame
        # Label(self.left_frame, text="Example Text").grid(row=0, column=0, padx=5, pady=5)

        counter = 0
        for j in range(1, 7):
            for i in range(0, 10):
                c = Canvas(self.left_frame, width=80, height=100)
                # Draw an Oval in the canvas
                c.create_oval(50, 50, 80, 80, fill="yellow")
                if i + counter + 1 in question_numbers:
                    c.create_text((65, 60), text='?')
                else:
                    c.create_text((65, 60), text=str(i + counter + 1))
                c.grid(row=j, column=i, ipadx=10, ipady=10)
                widgets['ovals'].append([c, i + counter + 1])
            counter += 10

        # Content inside right frame

        Label(self.right_frame, text="Chat With Friend",font='Helvetica 8 bold').grid(row=0, column=0, padx=5, pady=5)
        self.txtMessages = tkscrolled.ScrolledText(self.right_frame, width=50, height=10,font='Helvetica 8')
        self.txtMessages.grid(row=1, column=0, pady=10)
        self.txtYourMessage = Entry(self.right_frame, width=30,font='Helvetica 8 bold')
        self.txtYourMessage.insert(0, "Your message")
        self.txtYourMessage.grid(row=2, column=0, padx=2, pady=10)
        self.btnSendMessage = Button(self.right_frame, text="Send Message", width=20,command=self.sendMessage,font='Helvetica 8 bold')
        self.btnSendMessage.grid(row=3, column=0, padx=10, pady=10)

        self.dice_btn = Button(self.right_frame, text="Dice", width=20,command=self.throw_dice,font='Helvetica 8 bold')
        self.dice_btn.grid(row=4, column=0, padx=10, pady=40)
        self.tk_image = ImageTk.PhotoImage(dice_images[0])
        self.lbl = Label(self.right_frame, width=50, image=self.tk_image)
        self.lbl.grid(row=5, column=0, padx=10, pady=0)
        self.dice_text_label = Label(self.right_frame, width=30,height=10, text="Dice Number\nwill appear here",font='Helvetica 8 bold')

        self.dice_text_label.grid(row=6, column=0, padx=0, pady=10)

    def nickname_popup_window(self):
        popup_window = Tk()
        popup_window.wm_title("Nickname")
        popup_window.geometry('300x150')
        popup_window.maxsize(300, 150)
        popup_window.minsize(250, 100)
        popup_label = Label(popup_window, text="Please Write Down a Nickname")
        popup_label.grid(row=0, column=0, pady=20, padx=65)
        default_nickname = StringVar(popup_label, value=random.choice(["Hossein", "Andy", "Sara", "John", "Jane"]))
        text_input = Entry(popup_window, textvariable=default_nickname)
        text_input.grid(row=1, column=0, pady=5, padx=20)
        ok_button = Button(popup_window, text="Enter", command=lambda: [self.get_nickname(text_input.get()),
                                                                        popup_window.destroy()])
        ok_button.grid(row=2, column=0, pady=5, padx=65)

    def get_nickname(self, nickname):
        if nickname != "":
            self.window.title(nickname)
            self.nickname = nickname
        else:
            self.nickname = random.choice(["Hossein", "Andy", "Sara", "John", "Jane"])
            self.window.title(self.nickname)
            self.nickname = nickname

        clientSocket.send(nickname.encode("utf-8"))
        self.window.deiconify()
        recvThread = Thread(target=self.recvMessage)
        recvThread.daemon = True
        recvThread.start()

    # Button Functions
    def sendMessage(self):
        clientMessage = self.txtYourMessage.get()
        self.txtMessages.insert(END, "\n" + f"{self.nickname} :" + clientMessage)
        self.txtMessages.see("end")
        clientSocket.send(clientMessage.encode("utf-8"))
        self.txtYourMessage.delete(0, END)

    def update_dice_image(self,dice_number):

        new_img = ImageTk.PhotoImage(dice_images[dice_number - 1])
        self.lbl.configure(image=new_img)
        self.lbl.image = new_img

    def get_name(self,name):
        if name == main_sus["Name"]:
            win = Toplevel(window)
            win.maxsize(470, 100)
            win.minsize(470, 100)
            win.wm_title("Result")
            l = Label(win, text=f"Well done Detective {self.nickname}, we have found the assassin")
            l.grid(row=0, column=3,pady=20)
            b = Button(win, text="Restart", command=lambda: [win.destroy(), self.restart()])
            b.grid(row=1, column=2)
            c = Button(win, text="Quit", command=lambda: self.window.destroy())
            c.grid(row=1, column=4)
            self.dice_btn["state"] = "normal"

            win.grab_set()
        else:
            win = Toplevel(window)
            win.maxsize(470, 100)
            win.minsize(470, 100)
            win.wm_title("Result")
            l = Label(win, text=f"We are in a wrong path, the assassin is smarter than us Detective {self.nickname}")
            l.grid(row=0, column=3, pady=20)
            b = Button(win, text="Restart", command=lambda: [win.destroy(), self.restart()])
            b.grid(row=1, column=2)
            c = Button(win, text="Quit", command=lambda: self.window.destroy())
            c.grid(row=1, column=4)
            self.dice_btn["state"] = "normal"

            win.grab_set()


    def suspects_pop_up(self,message):
        win = Toplevel(self.window)

        win.wm_title("Final Decision")
        win.maxsize(650, 780)
        win.minsize(650, 780)
        l = Label(win, text=message)
        l.grid(row=0, column=3, pady=20)
        Label(win, text=f"Name", font='Helvetica 8 bold').grid(row=1, column=1)
        Label(win, text=f"Blood Type", font='Helvetica 8 bold').grid(row=1, column=2)
        Label(win, text=f"Occupation", font='Helvetica 8 bold').grid(row=1, column=3)
        Label(win, text=f"Hair Color", font='Helvetica 8 bold').grid(row=1, column=4)
        Label(win, text=f"Age", font='Helvetica 8 bold').grid(row=1, column=5)
        Label(win, text=f"Sex", font='Helvetica 8 bold').grid(row=1, column=6)
        buttons = [Button(win, text=f'{i}') for i in range(10)]

        for i, b in zip(range(len(suspects)), buttons):
            b.grid(row=i + 2, column=0)
            b.config(text=f"{suspects[i]['Name']}")
            Label(win, text=f"{suspects[i]['Name']}").grid(row=i + 2, column=1)
            Label(win, text=f"{suspects[i]['Blood Type']}").grid(row=i + 2, column=2)
            Label(win, text=f"{suspects[i]['Occupation']}").grid(row=i + 2, column=3)
            Label(win, text=f"{suspects[i]['Hair Color']}").grid(row=i + 2, column=4)
            Label(win, text=f"{suspects[i]['Age']}").grid(row=i + 2, column=5)
            Label(win, text=f"{suspects[i]['Sex']}").grid(row=i + 2, column=6)
        self.tk_image0 = ImageTk.PhotoImage(sus_images[0])
        buttons[0].config(image=self.tk_image0,command=lambda: [self.get_name(buttons[0].cget('text')),win.destroy()])
        self.tk_image1 = ImageTk.PhotoImage(sus_images[1])
        buttons[1].config(image=self.tk_image1,command=lambda: [self.get_name(buttons[1].cget('text')),win.destroy()])
        self.tk_image2 = ImageTk.PhotoImage(sus_images[2])
        buttons[2].config(image=self.tk_image2,command=lambda: [self.get_name(buttons[2].cget('text')),win.destroy()])
        self.tk_image3 = ImageTk.PhotoImage(sus_images[3])
        buttons[3].config(image=self.tk_image3,command=lambda: [self.get_name(buttons[3].cget('text')),win.destroy()])
        self.tk_image4 = ImageTk.PhotoImage(sus_images[4])
        buttons[4].config(image=self.tk_image4,command=lambda: [self.get_name(buttons[4].cget('text')),win.destroy()])
        self.tk_image5 = ImageTk.PhotoImage(sus_images[5])
        buttons[5].config(image=self.tk_image5,command=lambda: [self.get_name(buttons[5].cget('text')),win.destroy()])
        self.tk_image6 = ImageTk.PhotoImage(sus_images[6])
        buttons[6].config(image=self.tk_image6,command=lambda: [self.get_name(buttons[6].cget('text')),win.destroy()])
        self.tk_image7 = ImageTk.PhotoImage(sus_images[7])
        buttons[7].config(image=self.tk_image7,command=lambda: [self.get_name(buttons[7].cget('text')),win.destroy()])
        self.tk_image8 = ImageTk.PhotoImage(sus_images[8])
        buttons[8].config(image=self.tk_image8,command=lambda: [self.get_name(buttons[8].cget('text')),win.destroy()])
        self.tk_image9 = ImageTk.PhotoImage(sus_images[9])
        buttons[9].config(image=self.tk_image9,command=lambda: [self.get_name(buttons[9].cget('text')),win.destroy()])
        return win

    def CheckGameEnd(self):
        if player_info["currentPosition"] > 60:
            win = self.suspects_pop_up(f"Detective {self.nickname}, who is the assassin?")
            win.grab_set()
            return True
        if player_info["opponentCurrentPosition"] > 60:
            win = self.suspects_pop_up(f"We have no more time to waste\nDetective {self.nickname}, who is the assassin?")
            win.grab_set()
            return True



    def restart(self):
        global suspects, main_sus, hints, used_positions
        player_info["currentPosition"] = 1
        player_info["opponentCurrentPosition"] = 1
        self.txtMessages.delete('1.0', END)
        counter = 0
        suspects, main_sus, hints, used_positions = sus_info()
        # print(main_sus)
        for j in range(1, 7):
            for i in range(0, 10):
                c = Canvas(self.left_frame, width=80, height=100)
                # Draw an Oval in the canvas
                c.create_oval(50, 50, 80, 80, fill="yellow")
                if i + counter + 1 in question_numbers:
                    c.create_text((65, 60), text='?')
                else:
                    c.create_text((65, 60), text=str(i + counter + 1))
                c.grid(row=j, column=i, ipadx=10, ipady=10)
                widgets['ovals'].append([c, i + counter + 1])
            counter += 10


    def throw_dice(self):
        number = random.choices(range(1, 7),weights=[0.7,0.7,0.7,0.6,0.3,0.2])[0]
        signals["number"] = str(number)
        clientSocket.send(f'{signals["number"]}:signal number'.encode("utf-8"))
        self.dice_text_label.config(text=f"You have {number}\n waiting for the Opponent", font='Helvetica 8 bold')
        self.CheckGameEnd()
        self.update_dice_image(number)
        player_info["currentPosition"] += number
        for w in widgets["ovals"]:
            if w[1] == player_info["currentPosition"] and w[1] == player_info["opponentCurrentPosition"]:

                w[0].create_oval(50, 50, 80, 80, fill="green")
                if w[1] in question_numbers:
                    w[0].create_text((65, 60), fill="white", text='?')
                    used_positions.append(w[1])
                else:
                    w[0].create_text((65, 60), fill="white", text=str(player_info["currentPosition"]))
                continue
            if w[1] == player_info["currentPosition"]:

                w[0].create_oval(50, 50, 80, 80, fill="blue")
                if w[1] in question_numbers:
                    w[0].create_text((65, 60), fill="white", text='?')

                    hint = random.choice(hints)
                    hints.remove(hint)

                    
                    self.txtMessages.insert(END, "\n" + f"Stranger : " + f"{hint}\n")
                    self.txtMessages.see("end")

                else:
                    w[0].create_text((65, 60), fill="white", text=str(player_info["currentPosition"]))

                continue
            if w[1] == player_info["opponentCurrentPosition"]:

                w[0].create_oval(50, 50, 80, 80, fill="red")
                if w[1] in question_numbers:
                    w[0].create_text((65, 60), fill="white", text='?')
                    used_positions.append(w[1])
                else:
                    w[0].create_text((65, 60), fill="white", text=str(player_info["opponentCurrentPosition"]))
                continue
            if w[1] in used_positions:
                w[0].create_oval(50, 50, 80, 80, fill="gray")
                w[0].create_text((65, 60), fill="white", text="?")
            else:
                w[0].create_oval(50, 50, 80, 80, fill="yellow")
            if w[1] in question_numbers:
                w[0].create_text((65, 60), fill="black", text="?")
            else:
                w[0].create_text((65, 60), fill="black", text=str(w[1]))
        self.dice_btn["state"] = "disabled"

    def recvMessage(self):
        while True:

            serverMessage = clientSocket.recv(1024).decode("utf-8")

            gameflag = self.CheckGameEnd()

            if gameflag:
                pass

            else:
                if ":signal number" in serverMessage:
                    nick_name_index = serverMessage.find(":")
                    # lbl["text"]=serverMessage[nick_name_index+1:-14]
                    self.update_dice_image(int(serverMessage[nick_name_index + 1:-14]))

                    player_info["opponentCurrentPosition"] += int(serverMessage[nick_name_index + 1:-14])

                    if serverMessage[:nick_name_index] != self.nickname:
                        self.dice_btn["state"] = "normal"

                        for w in widgets["ovals"]:
                            if w[1] == player_info["currentPosition"] and w[1] == player_info[
                                "opponentCurrentPosition"]:
                                w[0].create_oval(50, 50, 80, 80, fill="green")
                                if w[1] in question_numbers:
                                    w[0].create_text((65, 60), fill="white", text='?')
                                else:
                                    w[0].create_text((65, 60), fill="white",
                                                     text=str(player_info["currentPosition"]))
                                continue

                            if w[1] == player_info["opponentCurrentPosition"]:
                                w[0].create_oval(50, 50, 80, 80, fill="red")
                                if w[1] in question_numbers:
                                    w[0].create_text((65, 60), fill="white", text='?')
                                else:
                                    w[0].create_text((65, 60), fill="white",
                                                     text=str(player_info["opponentCurrentPosition"]))
                                continue
                            if w[1] == player_info["currentPosition"]:
                                w[0].create_oval(50, 50, 80, 80, fill="blue")
                                if w[1] in question_numbers:
                                    w[0].create_text((65, 60), fill="white", text='?')
                                else:
                                    w[0].create_text((65, 60), fill="white",
                                                     text=str(player_info["currentPosition"]))
                                continue
                            if w[1] in used_positions:
                                w[0].create_oval(50, 50, 80, 80, fill="gray")
                                w[0].create_text((65, 60), fill="white", text="?")
                            else:
                                w[0].create_oval(50, 50, 80, 80, fill="yellow")
                            # w[0].create_oval(50, 50, 80, 80, fill="yellow")
                            if w[1] in question_numbers:
                                w[0].create_text((65, 60), fill="black", text='?')
                            else:
                                w[0].create_text((65, 60), fill="black", text=str(w[1]))
                        self.dice_text_label.config(
                            text=f"The Opponent has {serverMessage[nick_name_index + 1:-14]}\n your turn",
                            font='Helvetica 8 bold')
                    else:
                        self.dice_btn["state"] = "disabled"


                else:
                    self.txtMessages.insert(END, "\n" + serverMessage)
                    self.txtMessages.see("end")





window = Tk()
# window.config(bg="skyblue")

window.config()
GUI = Main(window)

window.mainloop()
