import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from lib.interface import Interface

bot = Interface('COM3')

params = bot.get_homing_paramaters()
print('Params:', params)

print('Homing')
bot.set_homing_command(0)


