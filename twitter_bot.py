from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from selenium import webdriver
from tkinter import messagebox
from selenium.webdriver.common.keys import Keys
import time
import os


class TwitterBot:
    def __init__(self, username, password, likesRate):
        self.username = username
        self.password = password
        self.likesRate = likesRate
        self.bot = webdriver.Firefox()

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        time.sleep(3)
        email = bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')

        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def like_tweet(self, hashtag):
        bot = self.bot
        bot.get('https://twitter.com/search?q=%23' +
                hashtag + '&src=typeahead_click')
        time.sleep(3)

        for i in range(1, 5):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(2)

        tweetLinks = [i.get_attribute('href')
                      for i in bot.find_elements_by_xpath("//a[@dir='auto']")]

        filteredLinks = list(filter(lambda x: 'status' in x, tweetLinks))

        for tweet in filteredLinks:
            print("Fetched tweet: ", tweet)

        for link in filteredLinks:

            bot.get(link)
            time.sleep(int(self.likesRate))

            try:
                bot.find_element_by_xpath("//div[@data-testid='like']").click()
                time.sleep(1)

            except Exception as ex:
                time.sleep(3)
                print("Exception")

########################################################################
################################# GUI  #################################
########################################################################
# ---------------------------Functions----------------------


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def clicked():
    user = txtUser.get()
    password = txtPass.get()
    hashtag = txtHashtag.get()
    likes_sec = combo.get()

    bot = TwitterBot(user, password, likes_sec)
    bot.login()
    while True:
        bot.like_tweet(hashtag)


def show_version():
    messagebox.showwarning(
        'Version', 'Version Actual: 1.0.0 beta \n \n Desarrollado por robertocml')


# ----------------------------Main Interface-----------------
window = Tk()
window.title("Twitter Bot  ")

w = 300
h = 200
x = 50
y = 100

window.geometry('600x600')


img = ImageTk.PhotoImage(Image.open(resource_path('fotobot.jpg')))
imglabel = Label(window, image=img)
imglabel.place(x=250, y=20)

lbl_title = Label(window, text="Twitter Bot",
                  font=("Fixedsys", 40), background="#1FB6EE")
lbl_title.grid(column=0, row=0)
lbl_title.place(x=140, y=140)


lbl_user = lbl_title = Label(
    window, text="Username:", font=("Fixedsys", 12), background="#1FB6EE")
lbl_user.place(x=120, y=250)
txtUser = Entry(window, width=30)
txtUser.grid(column=1, row=1)
txtUser.place(x=220, y=250)


lbl_password = Label(
    window, text="Password:", font=("Fixedsys", 12), background="#1FB6EE")
lbl_password.place(x=120, y=300)
txtPass = Entry(window, show="*", width=30)
txtPass.grid(column=1, row=1)
txtPass.place(x=220, y=300)

lbl_hashtag = Label(
    window, text="Hashtag:", font=("Fixedsys", 12), background="#1FB6EE")
lbl_hashtag.place(x=130, y=350)
txtHashtag = Entry(window, width=30)
txtHashtag.grid(column=1, row=1)
txtHashtag.place(x=220, y=350)

lbl_combo = Label(
    window, text="Like every _ secs:", font=("Fixedsys", 12), background="#1FB6EE")
lbl_combo.place(x=50, y=400)
combo = Combobox(window, width=28)
combo['values'] = (5, 10, 15, 20)
combo.current(1)
combo.place(x=220, y=400)


btn = Button(window, text="Start",
             command=clicked)
btn.place(x=250, y=450)


menu = Menu(window)
item_Acerca = Menu(menu, tearoff=0)
item_Acerca.add_command(label='Version', command=show_version)
menu.add_cascade(label='Acerca', menu=item_Acerca)
window.config(menu=menu)


window['background'] = '#1FB6EE'
window.mainloop()
