from PIL import Image
from random import randint
from colormath import color_objects
from colormath.color_objects import LabColor, BaseRGBColor, XYZColor, sRGBColor
from colormath import color_diff
from colormath import color_conversions

image_name = "" #Put the name of the file here, it should be in the same folder and this application

def make_colors(number_of_colors_to_use = randint(20,40)):
    colors_array = []
    for color in xrange(0, number_of_colors_to_use):
        colors_array.append([randint(0, 255), randint(0, 255), randint(0, 255)])
    return colors_array

def closest_color(actual_pixels, colors_to_use):
    best_pixels = []
    list_pixels =[]
    ###First we go through the array of actual pixels from the image.  By each row first
    for row_of_pixels in actual_pixels:
    #Then we look though each pixel in a row setting up a temporary row to add things onto each time
        temp_row = []
        for pixel in row_of_pixels:
    #For each pixel we are going to compare it to the list of owned colors

            color_array_for_min = []
            for owned_color in colors_to_use:
    #if the pixel is a clear pixel (0,0,0,0) we don't need to look through the other colors so we break the loop
                if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                    color_array_for_min.append([0,0,0,0,0])
                    break
    #otherwise we try to find the owned pixel that is the most similiar to the color
                else:
                    color1 = color_objects.sRGBColor(pixel[0],pixel[1],pixel[2], True)
                    color2 = color_objects.sRGBColor(owned_color[0],owned_color[1],owned_color[2], True)

                    #lab = LabColor(0.903, 16.296, -2.22)
                    color1lab = color_conversions.convert_color(color1, LabColor)
                    color2lab = color_conversions.convert_color(color2, LabColor)

                    dif1994 = color_diff.delta_e_cie1994(color1lab,color2lab,K_L=1, K_C=1, K_H=1, K_1=0.045, K_2=0.015)
                    #print (d1994)
                    #difference = d1994
                    #difference = math.sqrt(((owned_color[0]-pixel[0]))**2 + ((owned_color[1]-pixel[1]))**2 + ((owned_color[2]-pixel[2]))**2) # Euclidean distance, not as accurate at the delta 1994
                    color_array_for_min.append([owned_color[0],owned_color[1],owned_color[2],255, dif1994])
    #kind of creating a temporary variable that will always be bigger
            temp_color = [0,0,0,0,100000]
    #Find out which color has the smallest distance
            for color in color_array_for_min:
                if color[4] < temp_color[4]:
                    temp_color = color
    #add the smallest one to the row, repeat for rest of row
            temp_row.append(temp_color[0:4])
            list_pixels.append(tuple(temp_color[0:4]))
    #add the best row to the image, repeat for each row
    return list_pixels

def get_pixel_list(image_location):
    im = Image.open(image_location)
    xlim = im.size[0]
    ylim = im.size[1]
    pixels = list(im.getdata())
    width, height = im.size
    pixels = [pixels[i*width:(i+1)*width] for i in xrange(height)]
    return pixels, xlim, ylim

xdim = 0 # x dimensions of the image
ydim = 0 # y dimensiosn
#actual_pixels, xdim, ydim = get_pixel_list("terrasprites/terra1.png")
actual_pixels, xdim, ydim = get_pixel_list("ol.jpg")
colors = make_colors()
list_pixels = closest_color(actual_pixels,colors)
#print(list_pixels)
im2 = Image.new("RGBA", (xdim, ydim), "white")
im2.putdata(list_pixels)
im2.save(image_name,"JPEG")