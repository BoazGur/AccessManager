from tkinter import *
import pywintypes
from win10toast import  ToastNotifier
import os,pathlib

def start_up():
    toast= ToastNotifier()# inform thr user
    toast.show_toast("testUI","The file is runing",duration=2)
    os.chdir(pathlib.Path().absolute())
    return
def main():
    start_up()
    root = Tk()
    a = Label(root, text ="Hello World")
    a.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
      






