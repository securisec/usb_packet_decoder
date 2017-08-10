#!/usr/bin/env python
'''
# keyMap is based on http://www.usb.org/developers/hidpage/Hut1_12v2.pdf page 53
# https://docs.mbed.com/docs/ble-hid/en/latest/api/md_doc_HID.html
'''

# TODO: Change from subprocess tshark to pyshark
# TODO: Write one for a mouse movements with plot graph

import subprocess
from sys import argv, exit

try:
    import tqdm
    from colorama import Fore, Style
except:
    print 'pip install tqdm colorama'

try:
    file = argv[1]
except IndexError:
    print '\nPass a pcap file as an argument.'
    exit(0)

keyMap = {'04': 'a', '05': 'b', '06': 'c', '07': 'd', '08': 'e', '09': 'f', '0a': 'g', '0b': 'h', '0c': 'i', '0d': 'j',
          '0e': 'k', '0f': 'l', '10': 'm', '11': 'n', '12': 'o', '13': 'p', '14': 'q', '15': 'r', '16': 's', '17': 't',
          '18': 'u', '19': 'v', '1a': 'w', '1b': 'x', '1c': 'y', '1d': 'z', '1e': '1', '1f': '2', '20': '3', '21': '4',
          '22': '5', '23': '6', '24': '7', '25': '8', '26': '9', '27': '0', '2d': '-', '2e': '=', '2f': '[', '30': ']',
          '31': '\\', '32': '#', '33': ';', '34': "\'", '35': '`', '36': ',', '37': '.', '38': '/',
          '28': Fore.GREEN + 'ENTER\n' + Style.RESET_ALL, '2c': ' ',
          '4f': Fore.YELLOW + 'RIGHTARROW' + Style.RESET_ALL, '50': Fore.YELLOW + 'LEFTARROW' + Style.RESET_ALL,
          '51': Fore.YELLOW + 'DOWNARROW' + Style.RESET_ALL, '52': Fore.YELLOW + 'UPARROW' + Style.RESET_ALL,
          '4c': Fore.RED + 'DEL' + Style.RESET_ALL, '2a': Fore.RED + 'BACKSPACE' + Style.RESET_ALL,
          '3a': 'F1', '3b': 'F2', '3c': 'F3', '3d': 'F4', '3e': 'F5', '3f': 'F6', '40': 'F7', '41': 'F8', '42': 'F9',
          '43': 'F10', '44': 'F11', '45': 'F12'}

specialChars = data = ['1e:!', '1f:@', '20:#', '21:$', '22:%', '23:^', '24:&', '25:*', '26:(', '27:)',
                       '2b:\t', '2c: ', '2d:_', '2e:+', '2f:{', '30:}', '31:|', '32:~', '33::', '34:\"',
                       '35:~', '36:<', '37:>', '38:?']

readPackets = subprocess.Popen('tshark -r %s -T fields -e usb.capdata | grep -v 00:00:00:00:00:00:00:00' % file,
                               stdout=subprocess.PIPE, shell=True)
usbKeys = readPackets.stdout.readlines()

whatWastyped = []
for pressedKeys in tqdm.tqdm(usbKeys, ncols=20):
    if not '00:00:00:00:00:00:00:00' in pressedKeys:
        try:
            shiftKey = pressedKeys.split(':')[0]
            buttonPressed = pressedKeys.split(':')[2]
            for key, value in keyMap.iteritems():
                if buttonPressed in key:
                    if shiftKey == '02':
                        for x in specialChars:
                            if buttonPressed in x.split(':')[0]:
                                whatWastyped.append(x.split(':')[1])
                                break
                        else:
                            whatWastyped.append(value.upper())
                            break
                    else:
                        whatWastyped.append(value)
                        break
        except IndexError:
            continue

print 'Product Vendor: ' + ''.join(set(subprocess.Popen('tshark -r %s -T fields -e usb.idVendor' % file, shell=True,
                                                        stdout=subprocess.PIPE).stdout.read()))
print 'Product ID: ' + ''.join(set(subprocess.Popen('tshark -r %s -T fields -e usb.idProduct' % file, shell=True,
                                                    stdout=subprocess.PIPE).stdout.readlines()))
print
print ''.join(whatWastyped)
print
