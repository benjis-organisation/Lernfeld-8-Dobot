from flask import Flask, render_template_string
import cv2
import numpy as np
from matplotlib.colors import rgb2hex
import webcolors
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

app = Flask(__name__)

def patch_asscalar(a):
    return a.item()

setattr(np, "asscalar", patch_asscalar)

def get_requested_color(requested_color):
    return sRGBColor(*requested_color, is_upscaled=True)

def get_lab_color(color):
    return convert_color(color, LabColor)

def get_delta_e(requested_lab, lab):
    return delta_e_cie2000(requested_lab, lab)

def get_closest_color(requested_color):
    min_colors = {}
    requested_lab = get_lab_color(get_requested_color(requested_color))

    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        color = sRGBColor(r_c, g_c, b_c, is_upscaled=True)
        lab = get_lab_color(color)
        delta_e = get_delta_e(requested_lab, lab)
        min_colors[delta_e] = name

    return min_colors[min(min_colors.keys())]

def get_simplified_color_name(color_name):
    color_name = color_name.lower()
    basic_colors = ["blue", "green", "red", "yellow", "purple", "pink", "orange", "black", "white", "gray"]
    return next((basic_color for basic_color in basic_colors if basic_color in color_name), color_name)

@app.route('/', methods=['GET'])
def index():
    frame = cv2.imread('captured_image.jpg')
    if frame is None:
        return "Failed to load image", 500

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height, width, _ = frame.shape

    if height < 10 or width < 10:
        return "Invalid image dimensions", 500

    height_start, height_end = int(height * 0.4), int(height * 0.6)
    width_start, width_end = int(width * 0.4), int(width * 0.6)

    if height_start >= height_end or width_start >= width_end:
        return "Calculated section is empty", 500

    middle_section = frame[height_start:height_end, width_start:width_end]
    avg_color_per_row = np.average(middle_section, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    hex_color = rgb2hex(avg_color/255)

    color_name = get_closest_color(avg_color.astype(int))
    color_name = get_simplified_color_name(color_name)

    template = f"""
    <!DOCTYPE html>
    <html>
    <body style="background-color: {hex_color}; color: white; font-size: 2em; text-align: center; padding-top: 20%;">
        Hintergrundfarbe: {color_name}
    </body>
    </html>
    """

    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True, port=5001)