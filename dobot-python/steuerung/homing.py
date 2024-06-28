import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from lib.interface import Interface

# Funktion, um das Homing durchzuführen
def perform_homing():
    bot = Interface('COM3')

    params = bot.get_homing_paramaters()
    print('Params:', params)

    print('Homing')
    bot.set_homing_command(0)

if __name__ == "__main__":
    perform_homing()
