import math
import bitarray
import sys
import numpy as np
import cmath 

chunk_size = 8
A = 3/2
n0 = 2
chunk_size = 6
normalization_factor = 3/2 * 1/(2**(chunk_size/2))

def read_file(filename):
    with open(filename, mode="r") as file:
        text = file.readlines()[0]
    
    return text

def txt_to_bin(text):
    bin_str = ''
    for c in  text:
        c_bin = str(bin(ord(c))[2:])
        #Bit padding for reaching ASCII size
        while len(c_bin) < 7:
            c_bin = '0' + c_bin
        bin_str+=c_bin
    return bin_str



def pad_to_size(bin_str):
    size = len(bin_str)
    #Tota string padding to be divisible by chunk (not necessary for 78 chars, but in case)
    while((size%chunk_size)!=0):
        bin_str+='0'
        size+=1
    return bin_str


def clip(val):
    return (2*val+1)*normalization_factor

def map_chunk_to_complex(val_tpl):
    p, q, index_val = val_tpl
    #We use an if here instead of pattern matching because of python 3.9 compatibility
    #Sign bitmap : put a minus sign if the corresponding bit is a 1 
    if index_val == 0: return complex((clip(p)), clip(q))
    if index_val == 1: return complex(clip(p),  - clip(q))
    if index_val == 2: return complex(-clip(p) , clip(q))
    if index_val == 3: return complex(-clip(p) , - clip(q))

def pqis_from_string(bin_str):
    pqis=[]
    pqlen=(chunk_size-2)//2
    #we get the pqi from each chunk (chunk_size bits)
    for i in range(0, len(bin_str), chunk_size):
        p=int(bin_str[i:i+pqlen], 2)
        q=int(bin_str[i+pqlen:i+2*pqlen], 2)
        i=int(bin_str[i+2*pqlen:i+chunk_size], 2)
        pqis.append([p, q, i])
    return pqis


def clx_vec_from_pqis(pqis):
    return [map_chunk_to_complex(pqi) for pqi in pqis]

 

def serialize_complex(complex_vector,filename):
    complex_vector = complex_vector.reshape(-1)
    np.savetxt(filename,np.concatenate([np.real(complex_vector),
    np.imag(complex_vector)]))

def main():
    filename = ''
    if(len(sys.argv)>1):
        filename = sys.argv[1]
    if(filename):
        bin_str = txt_to_bin(read_file(filename))
        complex_arr = clx_vec_from_pqis(pqis_from_string(pad_to_size(bin_str))) 
        #Prepend header for theta estimation on receive
        X = [A]*n0 + complex_arr
        serialize_complex(np.array(X), "channel_input.txt")

if __name__== "__main__":
    main()


