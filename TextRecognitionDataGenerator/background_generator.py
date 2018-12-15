import cv2
import math
import os
import random
import numpy as np

from PIL import Image, ImageDraw, ImageFilter

class BackgroundGenerator(object):
    @classmethod
    def gaussian_noise(cls, height, width):
        """
            Create a background with Gaussian noise (to mimic paper)
        """

        # We create an all white image
        image = np.ones((height, width)) * 255

        # We add gaussian noise
        cv2.randn(image, 235, 10)

        return Image.fromarray(image).convert('RGB')

    @classmethod
    def plain_white(cls, height, width):
        """
            Create a plain white background
        """

        return Image.new("L", (width, height), 255).convert('RGB')

    @classmethod
    def quasicrystal(cls, height, width):
        """
            Create a background with quasicrystal (https://en.wikipedia.org/wiki/Quasicrystal)
        """

        image = Image.new("L", (width, height))
        pixels = image.load()

        frequency = random.random() * 30 + 20 # frequency
        phase = random.random() * 2 * math.pi # phase
        rotation_count = random.randint(10, 20) # of rotations

        for kw in range(width):
            y = float(kw) / (width - 1) * 4 * math.pi - 2 * math.pi
            for kh in range(height):
                x = float(kh) / (height - 1) * 4 * math.pi - 2 * math.pi
                z = 0.0
                for i in range(rotation_count):
                    r = math.hypot(x, y)
                    a = math.atan2(y, x) + i * math.pi * 2.0 / rotation_count
                    z += math.cos(r * math.sin(a) * frequency + phase)
                c = int(255 - round(255 * z / rotation_count))
                pixels[kw, kh] = c # grayscale
        return image.convert('RGB')

    @classmethod
    def picture(cls, height, width):
        """
            Create a background with a picture
        """

        pictures = os.listdir('./pictures')

        if len(pictures) > 0:
            picture = Image.open('./pictures/' + pictures[random.randint(0, len(pictures) - 1)])

            if picture.size[0] < width:
                picture = picture.resize([width, int(picture.size[1] * (width / picture.size[0]))], Image.ANTIALIAS)
            elif picture.size[1] < height:
                picture.thumbnail([int(picture.size[0] * (height / picture.size[1])), height], Image.ANTIALIAS)

            if (picture.size[0] == width):
                x = 0
            else:
                x = random.randint(0, picture.size[0] - width)
            if (picture.size[1] == height):
                y = 0
            else:
                y = random.randint(0, picture.size[1] - height)
                
            return picture.crop(
                (
                    x,
                    y,
                    x + width,
                    y + height,
                )
            )
        else:
            raise Exception('No images where found in the pictures folder!')

    @classmethod
    def myBackground(cls, height, width):
        """
            Create a background with dots and lines
        """

        def inP(h, w):
            return (h >= 0 and h < height and w >=0 and w < width)
        
        image = np.ones((height, width, 3)) * 255
        
        numDots = 300
        rH = np.random.randint(height, size=numDots)
        rW = np.random.randint(width, size=numDots)
        rR = np.random.randint(256, size=numDots)
        rG = np.random.randint(256, size=numDots)
        rB = np.random.randint(256, size=numDots)
        
        for i in range(numDots):
            image[rH[i]][rW[i]][0] = rR[i]
            image[rH[i]][rW[i]][1] = rG[i]
            image[rH[i]][rW[i]][2] = rB[i]
        
        
        numLines = np.random.randint(3) + 3
        i = 0
        while i < numLines:
            i += 1
            h1 = np.random.randint(height)
            h2 = np.random.randint(height)
            w1 = np.random.randint(width)
            w2 = np.random.randint(width)
            rR = np.random.randint(256)
            rG = np.random.randint(256)
            rB = np.random.randint(256)
        
        
            if (abs(h1-h2) + abs(w1-w2) < height):
                numLines += 1
                continue
        
            if (abs(h1-h2) >= abs(w1-w2)):
                if (h1 > h2):
                    h1, h2 = h2, h1
                    w1, w2 = w2, w1
        
                    
                for h in range(h1, h2+1):
                    w = int(w1 + (w2-w1) * h / (h2-h1))
                    for j in range(0, 1):
                        if inP(h, w + j):
                            image[h][w+j][0] = rR
                            image[h][w+j][1] = rG
                            image[h][w+j][2] = rB
        
            else:
                if (w1 > w2):
                    h1, h2 = h2, h1
                    w1, w2 = w2, w1
                    
                for w in range(w1, w2+1):
                    h = int(h1 + (h2-h1) * w / (w2-w1))
                    for j in range(0, 1):
                        if inP(h + j, w):
                            image[h+j][w][0] = rR
                            image[h+j][w][1] = rG
                            image[h+j][w][2] = rB
        
        
        p = Image.fromarray(np.asarray(np.clip(image, 0, 255), dtype='uint8'), "RGB")
        return p

