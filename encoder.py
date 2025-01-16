from PIL import Image
from itertools import product
import os

class Encoder:
    def __init__(self):
        self.channels = 3  #RGB format
        self.text_length_info_bits = 16
    
    def convert_text_to_binary(self, text):
        text = text.encode('utf-8')
        text_in_binary = ''.join(format(char, '08b') for char in text)
        return text_in_binary

    def check_text_size(self, width, height, text_in_binary):
        available_bits = (width * height) * self.channels
        needed_bits = len(text_in_binary) + self.text_length_info_bits + self.channels #text length + info about the length + flag number
        if available_bits < needed_bits: # check if the message can accommodate 
            return False
        return True
    
    def modify_LSB(self, rgb_value, bit):
        binary_rgb_value = format(rgb_value, '08b')
        binary_rgb_value = binary_rgb_value[0:len(binary_rgb_value)-1] + str(bit)
        return int(binary_rgb_value, 2) #return decimal number

    def encode(self, image_path, FLAG_NUMBER, text):
        # load the original image
        original_image = Image.open(image_path)
        original_pixels = original_image.load()
        (width, height) = original_image.size
        
        text_in_binary = self.convert_text_to_binary(text)

        if not self.check_text_size(width, height, text_in_binary):
            return Exception("Image resolution is too low for the text")
        
        text_length_info = format(len(text_in_binary), '016b')       
        text_in_binary = text_length_info + text_in_binary

        new_image = Image.new(original_image.mode, (width, height))
        new_pixels = new_image.load()

        text_index = 0

        for column, row in product(range(height), range(width)): #iterating through image
            r, g, b = original_pixels[row, column]
            if row == 0 and column == 0:  # store a flag in the first pixel
                r = self.modify_LSB(r, 1)
                g = FLAG_NUMBER
                new_pixels[0, 0] = r, g, b                    
            elif text_index < len(text_in_binary):  # encode individual text characters
                r = self.modify_LSB(r, text_in_binary[text_index]) 
                text_index += 1

                if text_index < len(text_in_binary):
                    g = self.modify_LSB(g, text_in_binary[text_index])
                    text_index += 1
                if text_index < len(text_in_binary): 
                    b = self.modify_LSB(b, text_in_binary[text_index])
                    text_index += 1

                new_pixels[row, column] = r, g, b 
            else: 
                new_pixels[row, column] = r, g, b 

        original_image.close()
        return new_image