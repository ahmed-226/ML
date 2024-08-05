import sys
from utils import preprocess

open_price = float(sys.argv[1])
high_price = float(sys.argv[2])
low_price = float(sys.argv[3])
volume = float(sys.argv[4])

prediction = preprocess(open_price, high_price, low_price, volume)
print(prediction[0])