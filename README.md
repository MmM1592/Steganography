This program is a credit project for the course PGR1 (Computer Graphics 1). It focuses on steganography, specifically the process of encoding text into an image

SUPPORTED FORMATS:  
The program works with RGB images in PNG format and text using the English alphabet (ASCII/UTF-8)

TECHNOLOGIES USED:  
Python was chosen for this task due to its extensive range of libraries for image and data manipulation

The program has been tested in a Windows environment. To run it properly, you need Python version 3.10.11 or higher and the PILLOW library for image manipulation
You can install PILLOW via the command line with: pip install pillow

Other libraries that were used are: itertools and os

ALGORITHM:  
The program encodes the binary representation of text into the least significant bits (LSB) of individual RGB channels. The process is as follows:

ENCODING:  
  1. The program takes an input image path and the text to be encoded.

  2. It converts the text into its binary representation (each character is represented by 8 bits).

  3. It checks whether the message fits into the image; if not, it displays an error message.

  4. If the message fits, it creates a new image and encodes the data as follows:  
    The first pixel contains flags indicating that text is encoded:  
      Red channel LSB = 1  
      Green channel LSB = flag_number (a constant initialized in the main module)  
      Blue channel = blue channel value is unchanged  
    Next 8 bits store the length of the text  
    Subsequent bits store the binary representation of the text characters  
    Remaining pixels are copied unchanged from the original image  
  
Example:  
For the text "Hi" (binary representation 01101000 01101001) and an image with RGB values like (125, 140, 60)...:

Red channel (125 = 01111101) → Change the last bit to 0  
Green channel (140 = 10001100) → Change the last bit to 1  
Continue until all bits of the text are encoded  

DECODING:  
  1. The program takes an input image path and opens the image  
  2. It checks whether the first pixel contains the flags written during encoding:  
  3. If no flags are found, it raises an error  
  4. If flags are present, it proceeds with decoding  
  5. It reads the next 8 LSBs to get the text length  
  6. Reads the encoded text starting from the appropriate pixel  
  7. Finally it converts the binary text back to a string and prints it to the console  

USAGE:  
Run the program using main.py, and select either the encoding or decoding option  
Input path in the format: C:\\dir\\dir\\image.png  

CODE STRUCTURE:  
The code consists of three components: main.py, encoder.py, and decoder.py  

main.py:  
This file determines which part of the program (encoding or decoding) to execute  

encoder.py:  
  This class contains two functions:  
    modify_LSB(self, int rgb_value, str bit): a function to overwrite the LSB of a channel with a specific bit  
    encode(self, str input_path): the main encoding function that implements the algorithm  
    
decoder.py:  
  This class also contains two functions:  
    read_LSB(self, int rgb_value): a function to extract the LSB from a channel  
    decode(self, str input_path): the decoding function that implements the algorithm


