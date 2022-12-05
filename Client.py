# Python based Graphical User Interface Client for Chat Application using Custom Tkinter

# Authors:
#     Light : Github: https://github.com/Nesasio
#     Rudy : Github: https://github.com/Rudrransh17

# Status: Development


# Custom Tkinter for modern GUI- Github: https://github.com/TomSchimansky/CustomTkinter
# Custom Tkinter documentation: https://github.com/TomSchimansky/CustomTkinter/wiki

# Help with multiple windows: https://github.com/TomSchimansky/CustomTkinter/wiki/CTkToplevel



# ======================== PROTOTYPE CLIENT OF NEURON =============================


# Importing the libraries
# -- command to install: pip install customtkinter --


import customtkinter
import tkinter
import tkinter.scrolledtext
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

import os
import datetime
import socket
import threading

import sys
import re



# ======================================================================================

# Setting the default appearance and color theme
# Help: https://github.com/TomSchimansky/CustomTkinter/wiki/AppearanceMode

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")



# Path for Image files
PATH = os.path.dirname(os.path.realpath(__file__))



# Host and Port
HOST = '127.0.0.1'
PORT = 1234


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# ======================================================================================


class App(customtkinter.CTk):

    WIDTH = 500
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.title("Log in to NEURON")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)



        # --------------------- Login Page -----------------------


        self.loginFrame = customtkinter.CTkFrame(master = self)
        self.loginFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)

        self.loginLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "Login System", text_font = ("Roboto", 24))
        self.loginLabel.pack(pady = 12, padx = 10)


        # Username and Password variables
        self.username = StringVar()
        self.password = StringVar()

        # NOTE: Unfortunately, placeholder_text doesn't work in combination with StringVar() T_T


        self.usernameLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "Username:", text_font = ("Roboto", 12))
        self.usernameLabel.pack(pady = (8, 0), padx = 10)

        self.loginEntry = customtkinter.CTkEntry(master = self.loginFrame, textvariable = self.username, width = 200)
        self.loginEntry.pack(pady = 3, padx = 10)


        self.passwordLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "Password:", text_font = ("Roboto", 12))
        self.passwordLabel.pack(pady = (3, 0), padx = 10)

        self.passwordEntry = customtkinter.CTkEntry(master = self.loginFrame, textvariable = self.password, width = 200, show = "*")
        self.passwordEntry.pack(pady = (3, 8), padx = 10)


        self.loginButton = customtkinter.CTkButton(master = self.loginFrame, text = "Login", hover_color = "green", command = self.login)
        self.loginButton.pack(pady = 8, padx = 5)

        self.signupLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "New user? Sign up!", text_font = ("Roboto", 10))
        self.signupLabel.pack(pady = (3, 3), padx = 10)

        self.signupButton = customtkinter.CTkButton(master = self.loginFrame, text = "Sign Up", hover_color = "dark blue", command = self.SignUpPage)
        self.signupButton.pack(pady = (3, 12), padx = 5)


        # ------------------------------------------------------------


        self.gui_Done = False
        self.running = True




    # ***********************************************************

    # On closing the window
    def on_closing(self, event = 0):
        self.destroy()



    # ***********************************************************

    # On Logging in
    def login(self):

        global auth_mode
        auth_mode = 'Login'

        # Getting the user info from the username and password entries
        global usernameInfo
        global passwordInfo

        usernameInfo = self.username.get()
        passwordInfo = self.password.get()

        threading.Thread(target=self.receive).start()
        #threading.Thread(target=self.send).start()


    # ****************** Method to recieve file ********************

    def receiveFile(self, fileName):
        file = open(fileName,'wb')
        l = client.recv(1024)
        while (l):
            file.write(l)
            l = client.recv(1024)
            if l == 'Completed'.encode():
                break
        file.close()


    # ******************* Method to send file **********************

    def sendFile(self, filePath):
        file = open(filePath,'rb')
        l = file.read(1024)
        while (l):
            client.send(l)
            l = file.read(1024)
        client.send('Completed'.encode())
        file.close()
        client.send('{} : Sent a file {}'.format(usernameInfo,fileName).encode())


    # ***********************************************************

    # send() Method
    def send():
        while True:
            message = '{} : {}'.format(usernameInfo, input())
            client.send(message.encode())


    # ***********************************************************

    #receive() Method
    def receive(self):

        global textArea

        while True:
            try:

                message = client.recv(1024).decode()

                if message == 'Login or Reg':
                    client.send(auth_mode.encode())

                elif message == 'USER':
                    client.send(usernameInfo.encode())

                elif message == 'PW':
                    client.send(passwordInfo.encode())

                elif message == 'EMAIL':
                    client.send(emailInfo.encode())

                elif message == 'Authenticated':
                    self.ChatWindow()

                elif message == 'Send File Name':
                    client.send(fileName.encode())

                elif message == 'Send File':
                    self.sendFile(filePath)

                elif message == 'Receive File Name':
                    receiveFileName = client.recv(1024).decode()

                elif message == 'Receive File':
                    self.receiveFile(receiveFileName)

                elif message == 'Authentication Failed':
                    print(message)
                    quit()

                else:
                    print(message)

                    textArea.config(state = 'normal')
                    textArea.insert('end\n', message)

                    textArea.yview('end')
                    textArea.config(state='disabled')



            except Exception as e:
                print(e)
                client.close()
                break



    # ***********************************************************

    # Method for Sign up button
    def SignUpPage(self):

        signUpWindow = customtkinter.CTkToplevel(self)
        signUpWindow.title("Sign up to NEURON")
        signUpWindow.geometry("500x450")
        signUpWindow.minsize(500, 450)
        signUpWindow.maxsize(500, 450)


        # Disabling the login window while on the sign up screen
        signUpWindow.grab_set()


        # Variables to store registered username, password and email
        global regUser
        global regPass
        global regEmail

        regUser = StringVar()
        regPass = StringVar()
        regEmail = StringVar()

        # Placeholder_text cannot be used together with StringVar() method.
        # Maybe it will be implemented in the future versions
        # Reference: https://github.com/TomSchimansky/CustomTkinter/wiki/CTkEntry


        signUpFrame = customtkinter.CTkFrame(master = signUpWindow)
        signUpFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)

        signUpWindowLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Sign Up to NEURON", text_font = ("Roboto", 24))
        signUpWindowLabel.pack(pady = (12, 10), padx = 10)


        signUpUserLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Enter Username:", text_font = ("Roboto", 12))
        signUpUserLabel.pack(pady = (15, 2), padx = 10)

        usernameEntry = customtkinter.CTkEntry(master = signUpFrame, textvariable = regUser, width = 250)
        usernameEntry.pack(pady = (2, 8), padx = 10)


        signUpEmailLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Enter Email:", text_font = ("Roboto", 12))
        signUpEmailLabel.pack(pady = (4, 2), padx = 10)

        emailEntry = customtkinter.CTkEntry(master = signUpFrame, textvariable = regEmail, width = 250)
        emailEntry.pack(pady = (2, 8), padx = 10)


        signUpPassLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Enter Password:", text_font = ("Roboto", 12))
        signUpPassLabel.pack(pady = (4, 2), padx = 10)

        passwordEntry = customtkinter.CTkEntry(master = signUpFrame, textvariable = regPass, width = 250, show = "*")
        passwordEntry.pack(pady = (2, 20), padx = 10)


        confirmButton = customtkinter.CTkButton(master = signUpFrame, height = 35, text = "Sign Up", hover_color = "dark green", command = self.SignUp)
        confirmButton.pack(pady = 6, padx = 5)

        cancelButton = customtkinter.CTkButton(master = signUpFrame, height = 35, text = "Cancel", hover_color = "red", command = signUpWindow.destroy)
        cancelButton.pack(pady = 6, padx = 5)


    # ***********************************************************

    # For Signing up
    def SignUp(self):

        global auth_mode
        auth_mode = 'Register'

        global usernameInfo
        global passwordInfo
        global emailInfo

        # Getting the info for registering the user
        usernameInfo = regUser.get()
        emailInfo = regEmail.get()
        passwordInfo = regPass.get()

        threading.Thread(target = self.receive).start()


    # ***********************************************************

    def ChatWindow(self):
        print("Chat Window Opened")

        mainChat = customtkinter.CTkToplevel(self)
        mainChat.title("NEURON")
        mainChat.geometry("800x500")
        mainChat.minsize(600, 500)
        mainChat.maxsize(1000, 600)


        # Getting the paths for Image files
        send_image = self.load_image("/GUI_Images/chat.png", 20)
        attach_image = self.load_image("/GUI_Images/add-folder.png", 20)
        home_image = self.load_image("/GUI_Images/home.png", 20)




        # -------- Creating two frames ---------

        # Configuring 2x1 grid layout for 2 frames

        mainChat.grid_columnconfigure(1, weight = 1)
        mainChat.grid_rowconfigure(0, weight = 1)


        frame1 = customtkinter.CTkFrame(master = mainChat,
                                            width = 200,
                                            corner_radius = 0)
        frame1.grid(row = 0, column = 0, sticky = "nswe")


        frame2 = customtkinter.CTkFrame(master = mainChat, corner_radius = 10)
        frame2.grid(row = 0, column = 1, sticky = "nswe", padx = 20, pady = 20)




        # -------------- Frame 1 ----------------

        # Configuring a 1x8 grid layout inside frame 1

        frame1.grid_rowconfigure(0, minsize = 10)
        frame1.grid_rowconfigure(3, weight = 1)
        frame1.grid_rowconfigure(5, minsize = 20)
        frame1.grid_rowconfigure(8, minsize = 10)

        label1 = customtkinter.CTkLabel(master = frame1,
                                            text = "NEURON",
                                            text_font = ("Impact Regular", -16))
        label1.grid(row = 1, column = 0, padx = 10, pady = 10)




        # About Button
        aboutButton = customtkinter.CTkButton(master = frame1,
                                                    text = "ABOUT",
                                                    text_color = "white",
                                                    width = 100,
                                                    height = 30,
                                                    corner_radius = 15,
                                                    hover_color = "green",
                                                    fg_color = "dark blue",
                                                    command = self.ShowAbout)
        aboutButton.grid(row = 2, column = 0, padx = 5, pady = 20)




        # Logout and Exit Button
        exitButton = customtkinter.CTkButton(master = frame1,
                                                    text = "Logout and Exit",
                                                    text_color = "white",
                                                    width = 100,
                                                    height = 50,
                                                    corner_radius = 15,
                                                    hover_color = "dark red",
                                                    fg_color = "red",
                                                    image = home_image,
                                                    command = self.exitMain)
        exitButton.grid(row = 5, column = 0, padx = 5, pady = 20)




        # Appearance Mode
        modeLabel = customtkinter.CTkLabel(master = frame1,
                                                text = "Appearance Mode:",
                                                text_font = ("Franklin Gothic", -14))
        modeLabel.grid(row = 6, column = 0, sticky = "w", padx = 20, pady = 0)

        menu1 = customtkinter.CTkOptionMenu(master = frame1,
                                                width = 100,
                                                height = 30,
                                                text_color = "white",
                                                dropdown_hover_color = "gray",
                                                button_hover_color = "dark blue",
                                                values = ["Dark", "Light", "System Default"],
                                                command = self.ChangeAppearance)
        menu1.grid(row = 7, column = 0, sticky = "s", padx = 20, pady = 10)





        # -------------- Frame 2 ----------------

        # Configuring 4x6 grid layout inside frame 2

        frame2.rowconfigure((0, 1, 2, 3, 4), weight = 1)
        frame2.rowconfigure(6, weight = 1)
        frame2.columnconfigure((0, 1, 2, 3, 4), weight = 1)
        frame2.columnconfigure(6, minsize = 10)


        # Text Area
        global textArea

        textArea = tkinter.scrolledtext.ScrolledText(mainChat, height = 20)
        textArea.grid(row = 0, column = 1, columnspan = 3, rowspan = 1,
                                padx = 20, pady = (20, 0), sticky = "new")
        textArea.config(state = 'disabled')



        # Text Box
        global signal
        signal = StringVar()

        global entry1

        entry1 = customtkinter.CTkEntry(master = frame2,
                                            textvariable = signal,
                                            width = 120,
                                            placeholder_text = "Say Something...",
                                            placeholder_text_color = "gray")
        entry1.grid(row = 5, column = 0, columnspan = 3, padx = 20, pady = (20, 0), sticky = "we")



        # Send Message Button
        sendButton = customtkinter.CTkButton(master = frame2,
                                                    width = 20,
                                                    height = 30,
                                                    text = "SEND",
                                                    hover_color = "red",
                                                    text_color = "white",
                                                    image = send_image,
                                                    command = self.SendMessage)
        sendButton.grid(row = 5, column = 3, padx = 10, pady = (20, 0), sticky = "we")




        # Attach file button
        attachButton = customtkinter.CTkButton(master = frame2,
                                                    width = 20,
                                                    height = 30,
                                                    text = "ATTACH",
                                                    hover_color = "red",
                                                    text_color = "white",
                                                    image = attach_image,
                                                    command = self.AttachFile)
        attachButton.grid(row = 5, column = 4, padx = 10, pady = (20, 0), sticky = "we")






    # ***********************************************************

    # Method to load the Button Images

    def load_image(self, path, image_size):
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))




    # ***********************************************************

    # Method to create Top level window for About Button
    def ShowAbout(self):

        aboutWindow = customtkinter.CTkToplevel(self)
        aboutWindow.title("ABOUT")
        aboutWindow.geometry("400x200")
        aboutWindow.minsize(400, 200)
        aboutWindow.maxsize(400, 200)

        aboutLabel1 = customtkinter.CTkLabel(master = aboutWindow, text = "Neuron is a LAN based chat app built purely using Python!")
        aboutLabel1.grid(row = 0, column = 0, padx = (10, 0), pady = 10)


        # To Disable the main window while about window is open, grab_set() method is used
        # On closing the about window, main window will be automatically re-enabled
        aboutWindow.grab_set()

        # grab_release() method also re-enables a disabled window


        # To hide the parent window: withdraw()
        # To restore it again: deiconify()

        # Hides the main window
        # self.withdraw()


        # NOTE: main window won't get restored on closing the
        # top level window if the main window was hid using withdraw() method.



    # ***********************************************************


    # Method to logout and exit

    def exitMain(self):


        # For some reason this part took awfully large amount of time and effort
        # to create, I don't know why...
        # And I don't know if it's just me but tkinter grid system is somehow
        # weird, easy, simple and complicated all at the same time.


        exitConfirm = customtkinter.CTkToplevel(self)
        exitConfirm.title("Logout and Exit")
        exitConfirm.geometry("420x130")
        exitConfirm.minsize(420, 130)
        exitConfirm.maxsize(420, 130)


        # Disabling the main window while in the confirmation window
        exitConfirm.grab_set()


        exitFrame = customtkinter.CTkFrame(master = exitConfirm,
                                            width = 370,
                                            corner_radius = 5)
        exitFrame.pack(padx = 0, pady = 10)


        # A Label on exit confirmation page
        exitLabel = customtkinter.CTkLabel(master = exitFrame,
                                            text = "Are you sure you want to logout and exit?",
                                            text_font = ("Impact Regular", 14))
        exitLabel.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)



        # Confirmed Exit Button
        confirmButton = customtkinter.CTkButton(master = exitFrame,
                                                text = "Exit",
                                                text_color = "white",
                                                width = 110,
                                                height = 50,
                                                corner_radius = 15,
                                                hover_color = "red",
                                                command = self.destroy)
        confirmButton.grid(row = 1, column = 0, padx = (40, 0), pady = 10)



        # Cancel Button
        cancelButton = customtkinter.CTkButton(master = exitFrame,
                                                text = "Cancel",
                                                text_color = "white",
                                                width = 110,
                                                height = 50,
                                                corner_radius = 15,
                                                hover_color = "green",
                                                command = exitConfirm.destroy)
        cancelButton.grid(row = 1, column = 1, padx = 0, pady = 10)


        # This part's done, FINALLY!!!



    # ***********************************************************


    # Method to change the window mode
    def ChangeAppearance(self, newAppearance):

        if newAppearance == "Light":
            customtkinter.set_appearance_mode("light")

        elif newAppearance == "System Default":
            customtkinter.set_appearance_mode("system")

        else:
            customtkinter.set_appearance_mode("dark")




    # ***********************************************************

    # Method to send message
    def SendMessage(self):

        global textmess
        textmess = signal.get()

        msg = f"{usernameInfo}: {textmess}"
        client.send(msg.encode('ascii'))
        # entry1.delete('1.0', 'end')



    # ***********************************************************

    # Method to attach a file
    def AttachFile(self):
        global fileName
        global filePath
        root = tkinter.Tk()
        root.withdraw()
        filePath = filedialog.askopenfilename()
        fileName = os.path.basename(filePath)
        client.send('File Transfer'.encode())



    # ***********************************************************


# ======================================================================================

if __name__ == "__main__":
    app = App()
    app.mainloop()

# ================================ END OF PROGRAM ======================================
