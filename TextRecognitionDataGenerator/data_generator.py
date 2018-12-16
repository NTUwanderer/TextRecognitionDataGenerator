import os
import random

from PIL import Image, ImageFilter

from computer_text_generator import ComputerTextGenerator
try:
    from handwritten_text_generator import HandwrittenTextGenerator
except ImportError as e:
    print('Missing modules for handwritten text generation.')
from background_generator import BackgroundGenerator
from distorsion_generator import DistorsionGenerator
import numpy as np

class FakeTextDataGenerator(object):
    @classmethod
    def generate_from_tuple(cls, t):
        """
            Same as generate, but takes all parameters as one tuple
        """

        cls.generate(*t)

    @classmethod
    def generate(cls, index, text, fonts, out_dir, height, extension, skewing_angle, random_skew, blur, random_blur, background_type, distorsion_type, distorsion_orientation, is_handwritten, name_format, width, alignment, text_color):
        ##########################
        # Create picture of text #
        ##########################
        images = ComputerTextGenerator.generate(text, fonts, text_color, height, width)

        #############################
        # Generate background image #
        #############################
        background_width = sum([ im.size[1] for im in images ])
        background = Image.fromarray(np.ones((height, background_width, 3), dtype='uint8') * 255, "RGB")

        print('# of images: {}'.format(len(images)))
        acc_width = np.random.randint(2, 13) # offset
        for idx, image in enumerate(images):
            random_angle = random.randint(0-skewing_angle, skewing_angle)
            rotated_img = image.rotate(skewing_angle if not random_skew else random_angle, expand=1)

            #############################
            # Apply distorsion to image #
            #############################
            if distorsion_type == 0:
                distorted_img = rotated_img # Mind = blown
            elif distorsion_type == 1:
                distorted_img = DistorsionGenerator.sin(
                    rotated_img,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
                )
            elif distorsion_type == 2:
                distorted_img = DistorsionGenerator.cos(
                    rotated_img,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
                )
            else:
                distorted_img = DistorsionGenerator.random(
                    rotated_img,
                    vertical=(distorsion_orientation == 0 or distorsion_orientation == 2),
                    horizontal=(distorsion_orientation == 1 or distorsion_orientation == 2)
                )

            ##################################
            # Resize image to desired format #
            ##################################
            new_width = int(float(distorted_img.size[0] + 10) * (float(height) / float(distorted_img.size[1] + 10)))
            resized_img = distorted_img.resize((new_width, height - 10), Image.ANTIALIAS)


            #############################
            # Place text with alignment #
            #############################
            new_text_width, _ = resized_img.size
            background.paste(resized_img, (int(acc_width), np.random.randint(2, 10)))
            acc_width += new_text_width
        
        background = BackgroundGenerator.applyMyBackground(height, background_width, np.array(background))

        ##################################
        # Apply gaussian blur #
        ##################################

        final_image = background.filter(
            ImageFilter.GaussianBlur(
                radius=(blur if not random_blur else random.randint(0, blur))
            )
        )

        #####################################
        # Generate name for resulting image #
        #####################################
        if name_format == 0:
            image_name = '{}_{}.{}'.format(text, str(index), extension)
        elif name_format == 1:
            image_name = '{}_{}.{}'.format(str(index), text, extension)
        elif name_format == 2:
            image_name = '{}.{}'.format(str(index),extension)
        else:
            print('{} is not a valid name format. Using default.'.format(name_format))
            image_name = '{}_{}.{}'.format(text, str(index), extension)

        # Save the image
        final_image.convert('RGB').save(os.path.join(out_dir, image_name))
