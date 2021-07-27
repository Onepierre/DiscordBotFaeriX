from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
#40 caractères max sur la ligne


def split_lines(text):
    lines = [""]
    words = text.split(" ")
    line_count = 0
    letter_count = 0
    for word in words:
        if letter_count + len(word) >= 40:
            lines[line_count] = lines[line_count][1:]
            lines.append("")
            line_count += 1
            letter_count = 0

        lines[line_count] += (" ")
        lines[line_count] += word
        letter_count += len(word) + 1
    return lines

def create_image():
    top_img = Image.open("astrid/base/top_img.jpg")
    bottom_img = Image.open("astrid/base/bottom_img.jpg")
    middle_img = Image.open("astrid/base/middle_img.jpg")

    #Get lengths
    top_size = top_img.size
    bottom_size = bottom_img.size
    middle_size = middle_img.size

    taille_font = 44
    font = ImageFont.truetype("fonts/arlrdbd.ttf", taille_font)

    text = find_text()

    splitted = split_lines(text)
    
    new_image = Image.new(
        'RGB', (top_img.size[0], top_img.size[1]+middle_img.size[1]*len(splitted)+bottom_img.size[1]), (250, 250, 250))
    new_image.paste(top_img, (0, 0))

    for i,line in enumerate(splitted):
        middle_img = Image.open("astrid/base/middle_img.jpg")
        draw = ImageDraw.Draw(middle_img)
        w, h = draw.textsize(line, font=font)
        draw.text((540-w/2, 0),
                line, (74, 57, 13), font=font)
        middle_img.save('astrid/temp.png')

        text_img = Image.open("astrid/temp.png")
        new_image.paste(text_img, (0, top_size[1]+middle_size[1]*i))


    new_image.paste(bottom_img, (0, top_size[1]+middle_size[1]*len(splitted)))
    new_image.save("astrid/conseil.png", "PNG")

def find_text():
    #quotes = np.loadtxt("astrid/quotes_lin.txt", delimiter=';', dtype='str')
    quotes = np.loadtxt("astrid/quotes.txt", delimiter=';', dtype='str')
    return np.random.choice(quotes)




if __name__ == "__main__":
    create_image()
