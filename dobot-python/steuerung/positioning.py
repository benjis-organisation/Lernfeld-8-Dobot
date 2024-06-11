import sys
import os
sys.path.insert(0, os.path.abspath('.')) # Erzeugt einen Pfad, der auf das aktuelle Verzeichnis zeigt

from lib.dobot import Dobot
# from camera.Calculate_color import calculate_color
# from camera.Capture_an_image import capture_image

bot = Dobot('COM3')

print('Bot status:', 'connected' if bot.connected() else 'not connected')

# Wir die Position noch benoetigt? Drin wegen Fehlermeldung.
pose = bot.get_pose()
print('Posistion:', pose)

def move_and_suck(bot, positions, suck):
    for position in positions:
        bot.move_to(*position)
    bot.interface.set_end_effector_suction_cup(*suck)

# color_positions = {
#     "1": [(4.2, 67, 41.5, 0.5)],
#     "2": [(-4, 65, 41.5, 0.5)],
#     "3": [(4.4, 54, 55, 0.5)],
#     "4": [(-4, 55, 55, 0.5)]
# }

# color_movement = {
#     "1": [(80, 60, 47.5, 0.5)],
#     "2": [(60, 60, 47.5, 0.5)],
#     "3": [(40, 60, 47.5, 0.5)],
#     "4": [(20, 60, 47.5, 0.5)]
# }

# color_endpositions = {
#     "red": [(80, 30, 30, 0.5)],
#     "green": [(60, 30, 30, 0.5)],
#     "blue": [(40, 30, 30, 0.5)],
#     "yellow": [(20, 30, 30, 0.5)]
# }

# for i in range(1, len(color_positions) + 1):
#     move_and_suck(bot, color_positions[i], (True, True))
#     print("Fahre zur Kamera")
#     move_and_suck(bot, [(-90, 50, 45, 0.5), color_movement[i]], (False, False))
#     capture_image()
#     print(f"Würfel Nummer {i}") #F wird für die Variable i eingesetzt
#     color_name = calculate_color()
#     if color_name in color_positions:
#         bot.move_to(color_endpositions[color_name])
#     else:
#         print(f"Farbe unbekannt: {color_name}")

print("Würfel Nummer 1")
move_and_suck(bot, [(4.2, 67, 41.5, 0.5)], (True, True))

print("Fahre zur Kamera")
move_and_suck(bot, [(-90, 50, 45, 0.5), (80, 60, 47.5, 0.5)], (False, False))

bot.move_to(80, 30, 30, 0.5)

# print("Würfel Nummer 2")
# move_and_suck(bot, [(-4, 65, 41.5, 0.5)], (True, True))

# print("Fahre zur Kamera")
# move_and_suck(bot, [(-90, 50, 45, 0.5), (60, 60, 47.5, 0.5)], (False, False))

# bot.move_to(60, 30, 30, 0.5)

# print("Würfel Nummer 3")
# move_and_suck(bot, [(4.4, 54, 55, 0.5)], (True, True))

# print("Fahre zur Kamera")
# move_and_suck(bot, [(-90, 50, 45, 0.5), (40, 60, 47.5, 0.5)], (False, False))

# bot.move_to(40, 30, 30, 0.5)

# print("Würfel Nummer 4")
# move_and_suck(bot, [(-4, 55, 55, 0.5)], (True, True))

# print("Fahre zur Kamera")
# move_and_suck(bot, [(-90, 50, 45, 0.5), (20, 60, 47.5, 0.5)], (False, False))

# bot.move_to(20, 30, 30, 0.5)