# -*- coding: utf-8 -*-
"""LSTM_TEST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ssdbUtPVDqZeCycfJjj7fhoYaP6KmH1C
"""

#Deep Learning LSTM TEST PART 
#HARROUZ MOUAD Faculty of Science and Technology MASTER2 ISICG 20208044
#Biyuzan  HAMZA Faculty of Science and Technology Master2 ISICG 20187435

from random import seed
from random import randint
from numpy import array
from math import ceil
from math import log10
from numpy import argmax
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.layers import RepeatVector
import tensorflow

#Global Variables 
Equations = []

# generate lists of random integers and their sum
def random_sum_pairs(n_examples, n_numbers, largest):
    X, y = list(), list()
    for i in range(n_examples):
        in_pattern = [randint(1, largest) for _ in range(n_numbers)]
        out_pattern = sum(in_pattern)
        X.append(in_pattern)
        y.append(out_pattern)
    return X, y

# generate lists of random integers and their substruction
def random_sub_pairs(n_examples, n_numbers, largest):
    X, y = list(), list()
    for i in range(n_examples):
        in_pattern = [randint(1, largest) for _ in range(n_numbers)]
        out_pattern = in_pattern[0]
        for i in range(1,len(in_pattern)):
          out_pattern=out_pattern-in_pattern[i]
        X.append(in_pattern)
        y.append(out_pattern)
    return X, y

# convert data to strings
def to_string(X, y,X1, n_numbers, largest):
    max_length = n_numbers * ceil(log10(largest + 1)) + n_numbers - 1
    Xstr = list()
    for pattern in X:
        strp = '+'.join([str(n) for n in pattern])
        strp = ''.join([' ' for _ in range(max_length - len(strp))]) + strp
        Xstr.append(strp)
    for pattern in X1:
        strp = '-'.join([str(n) for n in pattern])
        strp = ''.join([' ' for _ in range(max_length - len(strp))]) + strp
        Xstr.append(strp)


    max_length = ceil(log10(n_numbers * (largest + 1)))
    ystr = list()
    for pattern in y:
        strp = str(pattern)
        strp = ''.join([' ' for _ in range(max_length - len(strp))]) + strp
        ystr.append(strp)
    
    return Xstr, ystr

# integer encode strings
def integer_encode(X, y, alphabet):
    char_to_int = dict((c, i) for i, c in enumerate(alphabet))
    Xenc = list()
    for pattern in X:
        integer_encoded = [char_to_int[char] for char in pattern]
        Xenc.append(integer_encoded)
    yenc = list()
    for pattern in y:
        integer_encoded = [char_to_int[char] for char in pattern]
        yenc.append(integer_encoded)
    return Xenc, yenc

def one_hot_encode(X, y, max_int):
    Xenc = list()
    for seq in X:
        pattern = list()
        for index in seq:
            vector = [0 for _ in range(max_int)]
            vector[index] = 1
            pattern.append(vector)
        Xenc.append(pattern)
    yenc = list()
    for seq in y:
        pattern = list()
        for index in seq:
            vector = [0 for _ in range(max_int)]
            vector[index] = 1
            pattern.append(vector)
        yenc.append(pattern)
    return Xenc, yenc

# generate an encoded dataset
def generate_data(n_samples,n_samples_substruction, n_numbers, largest, alphabet):
    # generate pairs
    global Equations 
    
    X, y = random_sum_pairs(n_samples, n_numbers, largest)
    X1,y1 = random_sub_pairs(n_samples_substruction, n_numbers, largest)
   
    # convert to strings
    X, y = to_string(X, y+y1,X1, n_numbers, largest)
    Equations=[X[i] for i in range(len(X))] 
    # integer encode
    X, y = integer_encode(X, y, alphabet)
   
    # one hot encode
    X, y = one_hot_encode(X, y, len(alphabet))
 
    # return as numpy arrays
    X, y = array(X), array(y)
    return X, y

# invert encoding
def invert(seq, alphabet):
    int_to_char = dict((i, c) for i, c in enumerate(alphabet))
    strings = list()
    for pattern in seq:
        string = int_to_char[argmax(pattern)]
        strings.append(string)
    return ''.join(strings)

import re

model_name = 'OutputData/SUB_ADD1637408951.4818375.h5'
print("===== Loading Model ====")

model = tensorflow.keras.models.load_model(model_name)
print("===== Model Loaded ====")

#To string for element 
def to_string_test(X,X1, n_numbers, largest):
    max_length = n_numbers * ceil(log10(largest + 1)) + n_numbers - 1
    Xstr = list()
    for pattern in X:
        strp = '+'.join([str(n) for n in pattern])
        strp = ''.join([' ' for _ in range(max_length - len(strp))]) + strp
        Xstr.append(strp)
    for pattern in X1:
        strp = '-'.join([str(n) for n in pattern])
        strp = ''.join([' ' for _ in range(max_length - len(strp))]) + strp
        Xstr.append(strp)
    return Xstr

print("===== Testing some Random values  ====")
n_numbers = 2
largest = 100
alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', ' ','+']
size=5
size_substraction=5
n_batch = 10
X, y = generate_data(size,size_substraction, n_numbers, largest, alphabet)
result = model.predict(X, batch_size=n_batch, verbose=0)
# calculate error
expected = [invert(x, alphabet) for x in y]
predicted = [invert(x, alphabet) for x in result]
# show some examples
for i in range(size+size_substraction):
    print('Equation : %s ,Expected=%s, Predicted=%s' % (Equations[i],expected[i], predicted[i]))

#User tests
non_correct=True
#expression = "30-15-7+40-11-9-4+33-12+6" 
expression=input('Enter your equestion , you can use only number or + and - : ')


while non_correct :

  regexp = re.compile(r'[^+\-/^0-9\s]')

  if len(regexp.findall(expression)):
      expression=input('re-Enter your equestion , you can use only number or + and - : ')
  else:
      non_correct=False

print("Equation : ", expression)
items=expression.replace(" ","")
number_or_symbol = re.compile('(\d+|[^ 0-9])')
item=re.findall(number_or_symbol, items)

i=0
while(i<len(item)-2):

  if("+" in str(item[1])):
    X=[[int(item[0]),int(item[2])]]
    X=to_string_test(X,[], n_numbers, largest)

  else :
    X=[[int(item[0]),int(item[2])]]
    X=to_string_test([],X, n_numbers, largest)
   
  X, _ = integer_encode(X,[] , alphabet)
  X, _ = one_hot_encode(X, [], len(alphabet))
  X = array(X)
  result = model.predict(X, batch_size=n_batch, verbose=0)
  predicted = [invert(x, alphabet) for x in result]
  
  new_equation=item[i+3:]
  item=predicted+new_equation
  i=0

print("results =  ", item[0])