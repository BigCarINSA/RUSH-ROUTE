import csv
from PIL import Image

width = 20
height = 40

# open the image file
image_file = "image.png"
im = Image.open(image_file)

# convert the image to a list
pixels = list(im.getdata())

# convert the pixel values to 0, 1, or 2
pixel_list = []
for i in range(0, len(pixels), height):
    row = []
    for j in range(height):
        pixel = pixels[i+j]
        if pixel == (0, 0, 0): # black
            row.append(0)
        elif pixel == (255, 255, 255): # white
            row.append(1)
        elif pixel == (0, 255, 0): # green
            row.append(2)
    pixel_list.append(row.copy())
            

# save the list to a CSV file
with open('converted_image.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=";")
    for row in pixel_list:
        writer.writerow(row)
    
print("Pixel list saved to pixel_list.csv")
