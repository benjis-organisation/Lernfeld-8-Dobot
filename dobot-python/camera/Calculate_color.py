import cv2
import numpy as np
from matplotlib.colors import rgb2hex
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

basic_colors = {
    "red": (1, 0, 0),
    "green": (0, 1, 0),
    "blue": (0, 0, 1),
    "yellow": (1, 1, 0),
}

def patch_asscalar(a):
    return a.item()

def get_closest_color(requested_color):
    min_colors = {}
    requested_color = convert_color(sRGBColor(*requested_color, is_upscaled=True), LabColor)

    for name, rgb in basic_colors.items():
        color = convert_color(sRGBColor(*rgb), LabColor)
        delta_e = delta_e_cie2000(requested_color, color)
        min_colors[delta_e] = name

    return min_colors[min(min_colors.keys())]

def calculate_color():
    frame = cv2.imread('captured_image.jpg')
    if frame is None:
        return "Failed to load image", 500

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, _ = frame.shape

    if height < 10 or width < 10:
        return "Invalid image dimensions", 500

    height_start, height_end = int(height * 0.2), int(height * 0.8)
    width_start, width_end = int(width * 0.2), int(width * 0.8)

    if height_start >= height_end or width_start >= width_end:
        return "Calculated section is empty", 500

    middle_section = frame[height_start:height_end, width_start:width_end]
    avg_color_per_row = np.average(middle_section, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)

    color_name = get_closest_color(avg_color.astype(int))
    
    return color_name

setattr(np, "asscalar", patch_asscalar)
# print(calculate_color())