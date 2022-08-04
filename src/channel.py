import numpy as np


def channel(sent_signal):
    s = np.mean(np.absolute(sent_signal) ** 2)
    if s <= 1:
        s = 1

    theta = np.random.rand()

    noise_power = (10 ** (-2.65)) * s
    shift = np.exp(-2j * np.pi * theta)
    sent_signal = sent_signal * shift
    noise_std = np.sqrt(noise_power / 2)
    rcv_signal = sent_signal + noise_std * np.random.randn(len(sent_signal)) + 1j * noise_std * np.random.randn(
        len(sent_signal))
    return rcv_signal


def serialize_complex(complex_vector, file_name):
    complex_vector = complex_vector.reshape(-1)
    np.savetxt(file_name, np.concatenate([np.real(complex_vector), np.imag(complex_vector)]))


def deserialize_complex(file_name):
    tx_data = np.loadtxt(file_name)
    N_sample = tx_data.size
    N_sample = N_sample // 2
    tx_data = tx_data[0:N_sample] + 1j * tx_data[N_sample:(2 * N_sample)]
    return tx_data
