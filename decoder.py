from PIL import Image
from itertools import product


class Decoder: 

     def read_LSB(self, rgb_value):
          binary_rgb_value = format(rgb_value, '08b')
          lsb = binary_rgb_value[-1]
          return lsb

     def decode(self, input_path, FLAG_NUMBER):
          try:
               # load image
               image = Image.open(input_path)
               pixels = image.load()
               (width, height) = image.size

               hidden_text = ''
               text_length = ''
               text_index = 0
               bits_per_char = 8

               #decode image
               for column, row in product(range(height), range(width)): #iterating through image, row first
                    r, g, b = pixels[row, column]
                    if row == 0 and column == 0: #check whether there is a hidden text
                         first_lsb = self.read_LSB(r)
                         if first_lsb != '1' or g != FLAG_NUMBER:
                              raise ValueError("Image does not contain any hidden message")
                         
                    elif text_index < bits_per_char: #get length of text
                         text_length += self.read_LSB(r)
                         text_index += 1
                         if text_index < bits_per_char:
                              text_length += self.read_LSB(g)
                              text_index += 1
                         if text_index < bits_per_char:
                              text_length += self.read_LSB(b)
                              text_index += 1
                         else: 
                              hidden_text += self.read_LSB(b)
                              text_index += 1
                    
                    elif text_index < int(text_length, 2) + bits_per_char: #get the text
                         hidden_text += self.read_LSB(r)
                         text_index += 1
                         if text_index < int(text_length, 2) + bits_per_char: 
                              hidden_text += self.read_LSB(g)
                              text_index += 1
                         if text_index < int(text_length, 2) + bits_per_char:
                              hidden_text += self.read_LSB(b)
                              text_index += 1
                         else: 
                              break
               
               #display the hidden message
               bytes = [hidden_text[i:i+bits_per_char] for i in range(0, len(hidden_text), bits_per_char)]
               hidden_text = ''.join(chr(int(i, 2)) for i in bytes)
               print("The hidden message is:")
               print(hidden_text)
       
          except ValueError as value_error:
             raise ValueError(f"{value_error}")
          finally:
               image.close()