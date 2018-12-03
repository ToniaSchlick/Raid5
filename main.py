# --------------------------------------------
# Created on November 11 2018
# @author: Tonia Schlick and Jase Rost
# --------------------------------------------

from bitarray import bitarray
import tkinter as tk
from tkinter import messagebox
import time
import re
import math

testing = True


def test_log(message):
    if testing:
        print(message)


global num_disks
bit_slices = []
num_files = 5
place_holder = 0
driver = []
corrupted_disk = None
p_locations = []

def get_parity(bit_slice, location):
    print(location)
    parity = bit_slice[0]
    for x in range(1, len(bit_slice)):
        parity = parity ^ bit_slice[x]
    myparity = [parity]
    driver[location].append(myparity)


def save_data(data, labels, final):
    global p_locations
    global place_holder
    global num_disks
    global p_location
    global bit_slices
    done = False
    num_chunks = 4 #(num_disks-1)//2*2       # this can be changed to spread across more disks
    chunk_length = len(data) // num_chunks
    running = True
    x = 0
    while running:
        if place_holder - p_location == 0:
            p_locations.append(p_location)
            place_holder += 1
            p_location = p_location + num_disks-1
        else:
            bit_slice = data[(x * chunk_length): (x * chunk_length + chunk_length)]
            bit_slices.append(bit_slice)
            driver[place_holder % num_disks].append([bit_slice])
            place_holder += 1
            x += 1
            if x == num_chunks:
                running = False
        if place_holder % num_disks == 0 or (not running and final):
            if final and not place_holder % num_disks == 0:
                p_locations.append(p_location)
                p_location = p_location + num_disks - 1
            get_parity(bit_slices, (p_location - (num_disks - 1)) % num_disks)
            bit_slices = []


    for x in range(0, len(driver)):
        for y in range(0, len(driver[x])):
            if driver[x][y]:
                tag = labels[x][y]
                tag.config(text=display_bitarray(driver[x][y]))


def display_bitarray(array):
    return re.sub('[^0-9]+', '', str(array))


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


def kill_disk(disk, labels, num):
    global corrupted_disk
    print(str(num))
    corrupted_disk = num
    for x in range(0, len(disk)):
        disk[x] = 'X'
        labels[x].config(text=disk[x])


def init_data(labels):
    global p_location
    p_location = num_disks - 1
    files = ["file1", "file2", "file3", "file4", "file5"]
    for x in range(0, len(files)):
        data = bitarray()
        with open(files[x], 'rb') as fh:
            data.fromfile(fh)
        test_log(files[x] + ": " + (str(data)))
        test_log(files[x] + ": " + data.tostring())
        final = False
        if x == len(files)-1:
            final = True
        save_data(data, labels, final)

    for x in range(0, len(p_locations)):
        labels[p_locations[x] % len(driver)][x].config(fg="blue")
    print_disks()


def recover_disk(labels):
    global corrupted_disk
    lost_index = corrupted_disk
    for y in range(0, len(driver[lost_index])):
        bits = []
        driver[lost_index].pop(0)
        for x in range(0, len(driver)):
            if x is not lost_index and y < len(driver[x]):
                new_slice = driver[x][y]
                bits.append(new_slice[0])
        get_parity(bits, lost_index)
        print(driver[lost_index])

    for y in range(0, len(driver[lost_index])):
        for x in range(0, len(driver)):
            labels[lost_index][y].config(text=display_bitarray(driver[lost_index][y]))

    corrupted_disk = None

def get_num_disks(entry, window):
    global num_disks
    num_disks = int(entry.get())
    for x in range(0, num_disks):
        driver.append([])
    window.quit()
    print_disks()


def exit_window(window):
    window.quit()

def main():
    # print_disks()
    # print('\nkill disk 1')
    # kill_disk(disk1)
    # print_disks()
    # recover_disk(disk1)
    # print('\ndisk 1 recovered')
    # print_disks()
    # print_files()

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
    c = tk.Canvas(mainWin, height=500, width=1000, bg="gray")

    labels = []
    for x in range(0, num_disks):
        main_labels = []
        for y in range(0, num_files):
            main_labels.append(tk.Label(mainWin, bg='white'))
        labels.append(main_labels)
        
    #block = c.create_polygon(150, 100, 250, 200, fill="blue")
    for x in range(0, num_disks):
        width = (1000 - (5 * (num_disks + 1)))/num_disks
        left_anchor = width * x
        #main_labels = []
        for y in range(0, num_files):
            height = (500 - (5 * (num_files + 1)))/num_files
            top_anchor = height * y + 15
            c.create_rectangle(left_anchor+15, top_anchor, left_anchor+width, top_anchor+height, outline = "black", fill='white')
            #l = tk.Label(mainWin, text="Hello there!")
            #l.place(x=left_anchor+30, y = top_anchor+40)
            labels[x][y].place(x=left_anchor+30, y = top_anchor+40)
            #main_labels.append(l)
        #labels.append(main_labels)
    
    c.pack()
    stop = tk.Button(mainWin, text="Quit", command=lambda: exit_window(mainWin)).pack(side=tk.RIGHT, padx=(10, 10), pady=(10, 10))
    change = tk.Button(mainWin, text="Initialize", command=lambda tags=labels: init_data(tags)).pack(side=tk.RIGHT, padx=(10, 10), pady=(10, 10))
    recover = tk.Button(mainWin, text="Recover Disk", command=lambda tags=labels: recover_disk(tags)).pack(side=tk.RIGHT,
                                                                                                     padx=(10, 10),
                                                                                                     pady=(10, 10))


    for x in range(0, num_disks):
        label = "Disk " + str(x)
        b = tk.Button(mainWin, text=label, command=lambda y=x: kill_disk(driver[y], labels[y], y))
        b.pack(side= tk.LEFT, padx=(10, 10), pady=(10, 10))


    mainWin.mainloop()

if __name__ == '__main__':
    main()
