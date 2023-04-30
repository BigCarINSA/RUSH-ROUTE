from PIL import Image
import numpy as np
import csv

# Define the size of the image
width = 30
height = 15

# Define the color values
BLACK = 0
GREEN = 1
RED = 2

# Load the image and convert it to a numpy array
image = np.array(Image.open('image.jpg').convert('RGB'))

# Create a 2D list to store the converted image
converted_image = [[0 for _ in range(width)] for _ in range(height)]

# Convert the color values to 0, 1, and 2
for i in range(height):
    for j in range(width):
        if (image[i][j] == [255, 255, 255]).all():  # black
            converted_image[i][j] = GREEN
        elif (image[i][j] == [0, 0, 0]).all():  # white
            converted_image[i][j] = BLACK
        else:
            #elif (image[i][j] == [0, 0, 255]).all():  # blue
            converted_image[i][j] = RED

# Export the converted image to a CSV file
with open('converted_image.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for row in converted_image:
        writer.writerow(row)
