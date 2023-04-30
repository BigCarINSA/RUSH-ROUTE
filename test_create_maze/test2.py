from PIL import Image
import numpy as np
import csv
import test_3

# Define the size of the image
width = test_3.width
height = test_3.height

# Define the color values
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
BLUE = [0, 0, 255]

# Load the CSV file and convert it to a numpy array
with open('converted_image.csv', mode='r') as file:
    reader = csv.reader(file, delimiter= ";")
    converted_image = [[int(col) for col in row] for row in reader]

converted_image = np.array(converted_image)

# Create an RGB image with the same size as the converted image
image = np.zeros((width, height, 3), dtype=np.uint8)

# Convert the values in the converted image to RGB colors
for i in range(width):
    for j in range(height):
        if converted_image[i][j] == 0:  # black
            image[i][j] = BLACK
        elif converted_image[i][j] == 1:  # white
            image[i][j] = WHITE
        elif converted_image[i][j] == 2:  # blue
            image[i][j] = BLUE

# Save the image to a file
Image.fromarray(image).save('image_converted.jpg')
