import cv2
import numpy as np

# Initialize a blank canvas
window_height, window_width = 900, 1200  # Adjusted window size
canvas = np.ones((window_height, window_width, 3), dtype='uint8') * 255

# Initialize drawing variables
drawing = False
brush_size = 5
color = (0, 0, 0)  # Black color
shape = "brush"
x1, y1 = 0, 0

# Create window and bind the draw function to mouse events
cv2.namedWindow('Paint')

# Color palette
colors = {
    'black': (0, 0, 0),
    'red': (0, 0, 255),
    'green': (0, 255, 0),
    'blue': (255, 0, 0),
    'yellow': (0, 255, 255),
    'white': (255, 255, 255)
}

# Brush sizes
brush_sizes = [1, 2, 3, 4, 5]

# Button configuration
button_width, button_height = 100, 40
button_margin = 10
button_radius = 8

buttons = [
    {'label': 'Clear', 'pos': (button_margin, button_margin)},
    {'label': 'Black', 'pos': (button_margin + button_width + button_margin, button_margin)},
    {'label': 'Red', 'pos': (button_margin + 2 * (button_width + button_margin), button_margin)},
    {'label': 'Green', 'pos': (button_margin + 3 * (button_width + button_margin), button_margin)},
    {'label': 'Blue', 'pos': (button_margin + 4 * (button_width + button_margin), button_margin)},
    {'label': 'Yellow', 'pos': (button_margin + 5 * (button_width + button_margin), button_margin)},
    {'label': 'Eraser', 'pos': (button_margin + 6 * (button_width + button_margin), button_margin)},
    {'label': 'Size 1', 'pos': (button_margin, button_margin + button_height + button_margin)},
    {'label': 'Size 2', 'pos': (button_margin + button_width + button_margin, button_margin + button_height + button_margin)},
    {'label': 'Size 3', 'pos': (button_margin + 2 * (button_width + button_margin), button_margin + button_height + button_margin)},
    {'label': 'Size 4', 'pos': (button_margin + 3 * (button_width + button_margin), button_margin + button_height + button_margin)},
    {'label': 'Size 5', 'pos': (button_margin + 4 * (button_width + button_margin), button_margin + button_height + button_margin)},
    {'label': 'Brush', 'pos': (button_margin + 5 * (button_width + button_margin), button_margin + button_height + button_margin)},
    {'label': 'Rectangle', 'pos': (button_margin + 6 * (button_width + button_margin), button_margin + button_height + button_margin)},
    {'label': 'Line', 'pos': (button_margin + 7 * (button_width + button_margin), button_margin + button_height + button_margin)},
    {'label': 'Circle', 'pos': (button_margin + 8 * (button_width + button_margin), button_margin + button_height + button_margin)},
]

# Function to draw flat buttons with shadow
def draw_stylish_button(img, x, y, width, height, radius, label):
    # Draw button shadow
    shadow_color = (150, 150, 150)
    shadow_offset = 5
    cv2.rectangle(img, (x + shadow_offset, y + shadow_offset), (x + width + shadow_offset, y + height + shadow_offset), shadow_color, -1)

    # Draw button background
    button_color = (70, 130, 180)  # Steel blue color
    cv2.rectangle(img, (x, y), (x + width, y + height), button_color, -1, cv2.LINE_AA)

    # Draw button border
    border_color = (0, 0, 0)
    cv2.rectangle(img, (x, y), (x + width, y + height), border_color, 2, cv2.LINE_AA)

    # Draw button label
    text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    text_x = x + (width - text_size[0]) // 2
    text_y = y + (height + text_size[1]) // 2 - 5
    cv2.putText(img, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)


# Function to draw on the canvas
def draw(event, x, y, flags, param):
    global drawing, brush_size, color, shape, x1, y1

    if event == cv2.EVENT_LBUTTONDOWN:
        if y < button_height * 2 + button_margin * 2:  # Check if click is within button area
            for button in buttons:
                bx, by = button['pos']
                if bx <= x <= bx + button_width and by <= y <= by + button_height:
                    handle_action(button['label'].lower())
                    return
        else:
            drawing = True
            x1, y1 = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if shape == "brush":
                cv2.circle(canvas, (x, y), brush_size, color, -1)
            elif shape == "rectangle":
                temp_canvas = canvas.copy()
                cv2.rectangle(temp_canvas, (x1, y1), (x, y), color, brush_size)
                canvas[:] = temp_canvas[:]
            elif shape == "line":
                temp_canvas = canvas.copy()
                cv2.line(temp_canvas, (x1, y1), (x, y), color, brush_size)
                canvas[:] = temp_canvas[:]
            elif shape == "circle":
                temp_canvas = canvas.copy()
                cv2.circle(temp_canvas, ((x1 + x) // 2, (y1 + y) // 2), int(((x - x1) ** 2 + (y - y1) ** 2) ** 0.5),
                           color, brush_size)
                canvas[:] = temp_canvas[:]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


# Function to handle button actions
def handle_action(action):
    global color, brush_size, shape
    if action == 'clear':
        canvas[:] = 255
    elif action == 'black':
        color = colors['black']
    elif action == 'ed':
        color = colors['red']
    elif action == 'green':
        color = colors['green']
    elif action == 'blue':
        color = colors['blue']
    elif action == 'yellow':
        color = colors['yellow']
    elif action == 'eraser':
        color = colors['white']
    elif action.startswith('size_'):
        brush_size = int(action.split('_')[1])
    elif action == 'brush':
        shape = "brush"
    elif action == 'ectangle':
        shape = "rectangle"
    elif action == 'line':
        shape = "line"
    elif action == 'circle':
        shape = "circle"


# Function to display buttons on the canvas
def display_buttons(canvas):
    for button in buttons:
        x, y = button['pos']
        draw_stylish_button(canvas, x, y, button_width, button_height, button_radius, button['label'])


# Bind the draw function to mouse events
cv2.setMouseCallback('Paint', draw)

# Main loop
while True:
    display_canvas = canvas.copy()
    display_buttons(display_canvas)
    cv2.imshow('Paint', display_canvas)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC key to exit
        break

cv2.destroyAllWindows()