import encoder as e
import decoder as d
import os

try:
    FLAG_NUMBER = 123 #number indicating hidden message
    decode_or_encode = input("For encoding enter 0, for decoding enter 1: \n").strip()

    if decode_or_encode == "0" or decode_or_encode == "1":
        input_path = input("Enter the path to your image: ").strip() #input
        #exceptions
        if not input_path:
            raise ValueError("The path is empty")
        if not os.path.exists(input_path):
            raise ValueError("Path does not exist")
        
        if decode_or_encode == "0":  #encoding
            encoder = e.Encoder()
            encoder.encode(input_path, FLAG_NUMBER)
        else: #decoding
            decoder = d.Decoder()
            decoder.decode(input_path, FLAG_NUMBER)
    
    else: 
        raise ValueError("The entry is not correct")

except ValueError as value_error:
    print(f"Validation Error: {value_error}")