from time import time
encoded_text = open("encoded_text.txt").read()
from code import Decoder
d = Decoder(encoded_text)
start = time()
decoded_text = d.decode()
finish = time()
print(decoded_text)

duration = finish - start
print("Execution Time: " + str(duration))
