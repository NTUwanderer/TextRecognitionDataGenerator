import random
import numpy as np

from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter

class ComputerTextGenerator(object):
    @classmethod
    def generate(cls, text, fonts, text_color, height, width):
        cpyTxt = str(text)
        index = -1
        imgs = []
        while len(cpyTxt) != 0:
            index += 1
            spaceIndex = cpyTxt.find(" ")
            txt = str(cpyTxt)
            if (spaceIndex != -1):
                txt = cpyTxt[0:spaceIndex]
                cpyTxt = cpyTxt[spaceIndex+1:]
            else:
                cpyTxt = ""

            font_size = int((0.8 + np.random.rand()/10) * height)

            image_font = ImageFont.truetype(font=fonts[index], size=font_size)

            text_width, text_height = image_font.getsize(txt)
            txt_img = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))

            txt_draw = ImageDraw.Draw(txt_img)

            colors = [ImageColor.getrgb(c) for c in text_color.split(',')]
            c1, c2 = colors[0], colors[-1]

            rR = np.random.randint(256)
            rG = np.random.randint(256)
            rB = np.random.randint(256)
            fill = (
                rR,
                rG,
                rB
            )

            txt_draw.text((0, 0), txt, fill=fill, font=image_font)

            imgs.append(txt_img)

        return imgs
