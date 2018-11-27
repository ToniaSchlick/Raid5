# --------------------------------------------
# Created on November 11 2018
# @author: Tonia Schlick and Jase Rost
# --------------------------------------------

from bitarray import bitarray
import tkinter as tk
from tkinter import messagebox
import time

testing = True


def test_log(message):
    if testing:
        print(message)

global num_disks
place_holder = 0
disk1 = []
disk2 = []
disk3 = []
driver = [disk1, disk2, disk3]


def get_parity(a, b):
    parity = a ^ b
    return parity


def save_data(data):
    global place_holder
    a = data[0:data.length()//2]    # first half
    b = data[data.length()//2:]     # second half
    c = get_parity(a, b)            # parity bit

    driver[place_holder % len(driver)].append(c)
    driver[(place_holder + 1) % len(driver)].append(a)
    driver[(place_holder + 2) % len(driver)].append(b)
    place_holder += 1


def print_files():
    test_log('\nPrint Recovered Files')
    for x in range(5):
        position = x % len(driver)
        a = bitarray(driver[(position + 1) % len(driver)][x])
        b = bitarray(driver[(position + 2) % len(driver)][x])
        c = a+b
        print(c.tostring())
        print('\n')


def print_disks():
    count = 1
    for disk in driver:
        print('disk' + (str(count)))
        for x in disk:
            print(x)
        count += 1

##def display_disks(canvas):
##    global num_disks
##    for x in range(0, len(driver)):
##        width = 600/num_disks
##        left_anchor = width * x
##        for y in range(0, len(driver[x])):
##            height = 500/len(driver[x])
##            top_anchor = height * y
##            canvas.create_polygon(left_anchor, top_anchor, left_anchor+width, top_anchor+height)
            
def kill_disk(disk):
    for x in range(len(disk)):
        disk[x-1] = []


def init_data():
    files = ["file1", "file2", "file3", "file4", "file5"]
    for file in files:
        data = bitarray()
        with open(file, 'rb') as fh:
            data.fromfile(fh)
        test_log(file + ": " + (str(data)))
        test_log(file + ": " + data.tostring())
        save_data(data)


def recover_disk(disk):
    index = driver.index(disk)
    for x in range(len(disk)):
        disk[x] = get_parity(bitarray(driver[index + 1][x]), bitarray(driver[index + 2][x]))

def get_num_disks(entry, window):
    global num_disks
    num_disks = int(entry.get())
    window.quit()

def exit_window(window):
    window.quit()

def change_labels(labels):
    for x in labels:
        for y in x:
            y.config(text="General Kenobi!")
    
def main():
    init_data()
##    print_disks()
##    print('\nkill disk 1')
##    kill_disk(disk1)
##    print_disks()
##    recover_disk(disk1)
##    print('\ndisk 1 recovered')
##    print_disks()
##    print_files()

    global num_disks
    intro = tk.Tk()
    L1 = tk.Label(intro, text="How many disks would you like to run?")
    L1.pack()
    E1 = tk.Entry(intro)
    E1.focus_set()
    E1.pack()
    B1 = tk.Button(intro, text="Continue", command=lambda: get_num_disks(E1, intro))
    B1.pack()
    intro.bind('<Return>', (lambda e, B1=B1: B1.invoke()))
    intro.mainloop()
    intro.destroy()

    mainWin = tk.Tk()
    c = tk.Canvas(mainWin, height=500, width=600, bg="white")

    labels = []
    block = c.create_polygon(150, 100, 250, 200, fill="blue")
    for x in range(0, len(driver)):
        width = (600 - (5 * (num_disks + 1)))/num_disks
        left_anchor = width * x
        main_labels = []
        for y in range(0, len(driver[x])):
            height = (500 - (5 * (len(driver[x]) + 1)))/len(driver[x])
            top_anchor = height * y + 15
            c.create_rectangle(left_anchor+15, top_anchor, left_anchor+width, top_anchor+height, outline = "black")
            l = tk.Label(mainWin, text="Hello there!")
            l.place(x=left_anchor+30, y = top_anchor+40)
            main_labels.append(l)
        labels.append(main_labels)
    
    c.pack()
    stop = tk.Button(mainWin, text="Quit", command=lambda: exit_window(mainWin)).pack(side=tk.RIGHT)
    change = tk.Button(mainWin, text="Initialize", command=lambda: change_labels(labels)).pack(side=tk.RIGHT)

    for x in range(0, num_disks):
        label = "Disk " + str(x)
        b = tk.Button(mainWin, text=label, command=lambda: kill_disk(driver[x]))
        b.pack(side=tk.BOTTOM)

    mainWin.mainloop()

if __name__ == '__main__':
    main()
