from PIL import Image
from itertools import product


class Decoder: 

     def __init__(self):
          self.text_length_info_bits = 16
          self.bits_per_char = 8

     def read_LSB(self, rgb_value):
          binary_rgb_value = format(rgb_value, '08b')
          lsb = binary_rgb_value[-1]
          return lsb
     
     def binary_to_text(self, hidden_text):
          bytes = [hidden_text[i : i + self.bits_per_char] for i in range(0, len(hidden_text), self.bits_per_char)]
          hidden_text = ''.join(chr(int(i, 2)) for i in bytes)
          return hidden_text

     def decode(self, image_path, FLAG_NUMBER):
          # load image
          image = Image.open(image_path)
          pixels = image.load()
          (width, height) = image.size

          hidden_text = ''
          text_length = ''
          text_index = 0

          #decode image
          for column, row in product(range(height), range(width)): #iterating through image, row first
               r, g, b = pixels[row, column]
               if row == 0 and column == 0: #check whether there is a hidden text
                    first_lsb = self.read_LSB(r)
                    if first_lsb != '1' or g != FLAG_NUMBER:
                         raise ValueError("Image does not contain any hidden message")
                    
               elif text_index < self.text_length_info_bits: #get length of text
                    text_length += self.read_LSB(r)
                    text_index += 1
                    if text_index < self.text_length_info_bits:
                         text_length += self.read_LSB(g)
                         text_index += 1
                    if text_index < self.text_length_info_bits:
                         text_length += self.read_LSB(b)
                         text_index += 1
                    else: 
                         hidden_text += self.read_LSB(g)
                         hidden_text += self.read_LSB(b)
                         text_index += 2
               
               elif text_index < int(text_length, 2) + self.text_length_info_bits: #get the text
                    hidden_text += self.read_LSB(r)
                    text_index += 1
                    if text_index < int(text_length, 2) + self.text_length_info_bits: 
                         hidden_text += self.read_LSB(g)
                         text_index += 1
                    if text_index < int(text_length, 2) + self.text_length_info_bits:
                         hidden_text += self.read_LSB(b)
                         text_index += 1
                    else: 
                         break
          
          hidden_text = self.binary_to_text(hidden_text)

          image.close()

          return hidden_text