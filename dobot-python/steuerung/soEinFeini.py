import sys
import os
import subprocess
sys.path.insert(0, os.path.abspath('.')) # Erzeugt einen Pfad, der auf das aktuelle Verzeichnis zeigt

from lib.interface import Interface
from lib.dobot import Dobot

interface = Interface('COM3')
dobot = Dobot('COM3')

if interface.connected():
    print('Bot status: Glücklich :D')
else:
    print('Bot status: Traurig :(')
    sys.exit(1)  

# TODO: UI braucht einen Homing Button
try:
    subprocess.run(["python", "homing.py"])
except Exception as e:
    print('Fehler beim Starten der homing.py:', e)
    sys.exit(1)

# TODO: Hier muss noch die Position des Saugnapfes angepasst werden
dobot.move_to(200, 0, 0, 0)

print('Ich fang jetzt an zu nuckeln!')
interface.set_end_effector_suction_cup(True, True)

# TODO: Farberkennung hinzufuegen (Wuerfel aufnehmen, Farbe erkennen, Wuerfel an definierte Position ablegen)

print('Sucking stopped!')
interface.set_end_effector_suction_cup(False, False) 