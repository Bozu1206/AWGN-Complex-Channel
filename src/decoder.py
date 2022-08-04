import cmath
import math

import numpy as np

import channel
import encoder

n0 = 2


def estimate_phase_shift(received_y):
    # Compute first 1/sqrt(n)*sum(Yi)
    Y = sum(received_y[:n0]) / np.sqrt(len(received_y[:n0]))

    # Then get the arg(Y
    return -cmath.phase(Y)



def modulus(z):
    return np.abs(z)


def decode_one_message(clx_lib, clx_val, pqi_lib, z):
    dist = []
    for qam_point in clx_lib:
        dist.append(modulus(qam_point - z * clx_val))
    return pqi_lib[dist.index(min(dist))]


def decode_total_message(true_sig, theta_estimate):
    pqi_lib = []
    clx_lib = []
    z = complex(math.cos(theta_estimate), math.sin(theta_estimate))
    for p in range(0, 4):
        for q in range(0, 4):
            for i in range(0, 4):
                pqi_lib.append([p, q, i])
                clx_lib.append(encoder.map_chunk_to_complex((p, q, i)))

    return [decode_one_message(clx_lib, y, pqi_lib, z) for y in true_sig]


def pqi_to_str(pqi_tup):
    p, q, i = pqi_tup
    three_bit_format = '{0:02b}'
    return three_bit_format.format(p) + three_bit_format.format(q) + three_bit_format.format(i)


def pqis_to_bin_str(pqi_arr):
    bin_str = ''
    for pqi in pqi_arr:
        bin_str += pqi_to_str(pqi)

    return bin_str


def bin_str_to_final_msg(bin_str):
    count = 0
    s_fin = ""
    ascii_bit_per_char = 7  # ASCII char fit on 7 bits
    nb_char = len(bin_str) / ascii_bit_per_char

    for count in range(count, int(nb_char)):
        c = bin_str[count * ascii_bit_per_char: count * ascii_bit_per_char + ascii_bit_per_char]

        if len(c) != ascii_bit_per_char:
            break

        s_fin += (chr(int(c, 2)))

    return s_fin


def deserialize_complex(file_name):
    tx_data = np.loadtxt(file_name)
    N_sample = tx_data.size
    N_sample = N_sample // 2
    tx_data = tx_data[0:N_sample] + 1j * tx_data[N_sample:(2 * N_sample)]
    return tx_data


def main():
    sig = deserialize_complex("channel_input.txt")

    # COMMENT THE NEXT LINE IF YOU WANT TO RUN ON THE SERVER
    sig = channel.channel(sig)

    shift = estimate_phase_shift(sig[:n0])
    pqis = decode_total_message(sig[n0:], shift)
    result = bin_str_to_final_msg(pqis_to_bin_str(pqis))
    print(result)


if __name__ == '__main__':
    main()
