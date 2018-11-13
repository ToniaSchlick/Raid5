# --------------------------------------------
# Created on November 11 2018
# @author: Tonia Schlcik and Jase Rost
# --------------------------------------------

from bitarray import bitarray

testing = True


def test_log(message):
    if testing:
        print(message)


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


def main():
    init_data()
    print_disks()
    print('\nkill disk 1')
    kill_disk(disk1)
    print_disks()
    recover_disk(disk1)
    print('\ndisk 1 recovered')
    print_disks()
    print_files()


if __name__ == '__main__':
    main()