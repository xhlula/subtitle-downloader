import sys
import os
try:
    from _winreg import *
except:
    from winreg import *


if len(sys.argv) == 1 or sys.argv[1] == '--i':
    path = '*\\shell\\subbot\\'
    command = "{0} \"{1}\\subbot.py\" \"%1\" --wait".format(sys.executable, os.path.dirname(__file__))
    CreateKey(HKEY_CLASSES_ROOT, path + "command")

    cmd = OpenKey(HKEY_CLASSES_ROOT, path + "command", 0, KEY_READ | KEY_WRITE)
    ico = OpenKey(HKEY_CLASSES_ROOT, path, 0, KEY_WRITE)
    try:
        # Set the icon to something semi appropriate. IE being useful right here :^)
        # TODO: Put own icon rather than a system one
        #SetValueEx(ico, 'Icon', 0, REG_SZ, 'ieframe.dll,114')

        # Setting caption to default key
        SetValueEx(ico, '', 0, REG_SZ, 'Download Subtitles')

        # Set full path to default key
        SetValue(cmd, '', REG_SZ, command)
    except WindowsError:
        print("Please run this file as an administrator")
    finally:
        CloseKey(cmd)
        CloseKey(ico)
elif sys.argv[1] == '--u':
    # For some reason python all I get is [Access denied] using pythons' DeleteKey method.
    # resorting to reg.exe on windows to delete the key for us
    os.system(r'reg delete HKCR\*\shell\subbot /f')