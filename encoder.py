from PIL import Image
from itertools import product
import os

class Encoder:
    def __init__(self):
        self.channels = 3  #RGB format

    def modify_LSB(self, rgb_value, bit):
        binary_rgb_value = format(rgb_value, '08b')
        binary_rgb_value = binary_rgb_value[0:len(binary_rgb_value)-1] + str(bit)
        return int(binary_rgb_value, 2) #return decimal number


    def encode(self, input_path, FLAG_NUMBER):
        try:
            # load the original image
            original_image = Image.open(input_path)
            original_pixels = original_image.load()
            (width, height) = original_image.size
            total_pixels = width * height

            #text input
            text = ((input("Enter the text: ").strip())).encode('utf-8')
            if not text:
                raise ValueError("Cannot encode empty text")           
            
            # encode the text in format:
            # first pixel flags if the image contain text - LSB r = 1, g = flag number, b = b
            # 8 bits containing info about the length of the text
            # n * 8 bits containing the text
            # rest of the pixels is copied from the original image
            
            text_length = len(text)
            bits_per_char = 8
            
            text_bits = bits_per_char + (text_length * bits_per_char) # info about length of text + n * 8 bits 
            needed_bits = self.channels + text_bits # + first pixel (flags)
            available_bits = total_pixels * self.channels # total avaiable bits in image

            if available_bits < needed_bits: # check if the message can accommodate 
                raise ValueError("Image resolution is too low for the text")

            new_image = Image.new(original_image.mode, (width, height)) # if yes -> create a new image
            new_pixels = new_image.load()

            text_length_info = format(text_length * bits_per_char, '08b') #length of text in binary
            text_in_binary = ''.join(format(char, '08b') for char in text) #text in binary
            text_in_binary = text_length_info + text_in_binary #add the length info to the beginning
            text_index = 0

            for column, row in product(range(height), range(width)): #iterating through image, row first
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

                    

            #save the image with hidden text
            output_path = input("Enter the new image name or path where you want to save it: ").strip()
            if not output_path:
                current_dir = os.path.dirname(__file__)
                output_path = os.path.join(current_dir, "EncryptedImage.png")

            new_image.save(output_path)
            print(f"Text successfully hidden in {output_path}")

        except ValueError as value_error:
            print(f"Validation Error: {value_error}")
        finally:
            original_image.close()