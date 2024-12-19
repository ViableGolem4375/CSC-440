import marshal
import os
import pickle
import sys
from array import array
from typing import Dict
from typing import Tuple

"""
Invariant Documentation:

Invariant: At any point during the run time of this algorithm, the
           priority queue will contain nodes that represent a partition of
           the initial set of symbols from the codebook, and the "weight"
           of each node is the sum of the "weights" of the symbols which it
           represents.

Initialization: At the start of the algorithm, the priority queue contains
                a node for each symbol, thus the invariant holds true.

Maintenance: At each step of the algorithm, it will remove 2 nodes with the
             lowest "weights" from the priority queue and combine them into a
             new node. This operation maintains the partition of the symbols 
             (since the new node represents the union of the symbols 
             represented by the two old nodes) and the sum of the weights 
             (since the weight of the new node is the sum of the weights of 
             the two old nodes). Thus, the invariant holds true.

Termination: At the end of the algorithm, the priority queue contains a 
             single node that represents all the symbols. Therefore, the 
             invariant implies that the weight of this node is the sum of 
             the weights of all the symbols, which means that the 
             constructed coding is optimal.
"""

def encode(message: bytes) -> Tuple[str, Dict]:
    """ Given the bytes read from a file, encodes the contents using the Huffman encoding algorithm.

    :param message: raw sequence of bytes from a file
    :returns: string of 1s and 0s representing the encoded message
    dict containing the decoder ring as explained in lecture and handout.
    """
    frequency_list = {}
    for character in message:
        frequency_list[character] = frequency_list.get(character, 0) + 1
    dataset = frequency_list.keys()
    raw_data = []

    for data in dataset:
        raw_data.append((frequency_list[data], data))

    raw_data.sort()

    while len(raw_data) > 1:
        lowest_two_weights = tuple(raw_data[0:2])
        higher_weights = raw_data[2:]
        x = lowest_two_weights[0][0] + lowest_two_weights[1][0]
        raw_data = higher_weights + [(x, lowest_two_weights)]
        maximum = len(raw_data) - 1
        raw_data = quick_sort(raw_data, 0, maximum)

    raw_data = raw_data[0]

    tree = trim_dataset(raw_data)

    codex = {}

    codex = codemaker(tree)

    new_message = ""
    for character in message:
        new_message += codex[character]

    return new_message, codex

def trim_dataset(dataset):
    x = dataset[1]
    if not isinstance(x, tuple):
        return x
    else:
        return(trim_dataset(x[0]), trim_dataset(x[1]))
    
def quick_sort(list, lo, hi):
    if lo < hi:
        pi = quick_part(list, lo, hi)
        quick_sort(list, lo, pi -1)
        quick_sort(list, pi + 1, hi)
    return list

def quick_part(list, lo, hi):
    i = lo - 1
    pivot = list[hi]
    for j in range(lo, hi):
        if list[j][0] < pivot[0]:
            i = i + 1
            list[i], list[j] = list[j], list[i]
    list[i + 1], list[hi] = list[hi], list[i + 1]
    return (i + 1)

def codemaker(tree):
    codex = {}

    pattern = ""
    codex = codeHelper(tree, codex, pattern)

    return codex

def codeHelper(tree, codex, code):
    if not isinstance(tree, tuple):
        codex[tree] = code
    else:
        codeHelper(tree[0], codex, code + "0")
        codeHelper(tree[1], codex, code + "1")
    return codex

def decode(message: str, decoder_ring: Dict) -> bytes:
    """ Given the encoded string and the decoder ring, decodes the message using the Huffman decoding algorithm.

    :param message: string of 1s and 0s representing the encoded message
    :param decoder_ring: dict containing the decoder ring
    return: raw sequence of bytes that represent a decoded file
    """
    new_message = array('B')

    code_list = list(decoder_ring.items())

    i = 0
    j = i + 1

    while j <= len(message):
        for k in range(len(code_list)):
            if message[i:j] == code_list[k][1]:
                new_message.append(code_list[k][0])
                i += j - i
                j = i
                break
        j += 1

    return new_message


def compress(message: bytes) -> Tuple[array, Dict]:
    """ Given the bytes read from a file, calls encode and turns the string into an array of bytes to be written to disk.

    :param message: raw sequence of bytes from a file
    :returns: array of bytes to be written to disk
    dict containing the decoder ring
    """
    code_message, codex = encode(message)

    message_padding = 8 - len(code_message) % 8

    value = {"pad": message_padding}
    codex.update(value)

    for i in range(message_padding):
        code_message += "0"

    compressed_message = bytearray()
    for i in range(0, len(code_message), 8):
        byte = code_message[i:i+8]
        compressed_message.append(int(byte,2))

    return compressed_message, codex


def decompress(message: array, decoder_ring: Dict) -> bytes:
    """ Given a decoder ring and an array of bytes read from a compressed file, turns the array into a string and calls decode.

    :param message: array of bytes read in from a compressed file
    :param decoder_ring: dict containing the decoder ring
    :return: raw sequence of bytes that represent a decompressed file
    """
    byte_array = array('B', message)

    raw_message = ""

    for bit in byte_array:
        bits = bin(bit)[2:].rjust(8, '0')
        raw_message += bits

    message_padding = decoder_ring.get("pad")
    final_message = raw_message[0:len(raw_message) - message_padding]

    final_message = decode(final_message, decoder_ring)

    return final_message


if __name__ == '__main__':
    usage = f'Usage: {sys.argv[0]} [ -c | -d | -v | -w ] infile outfile'
    if len(sys.argv) != 4:
        raise Exception(usage)

    operation = sys.argv[1]
    if operation not in {'-c', '-d', '-v', '-w'}:
        raise Exception(usage)

    infile, outfile = sys.argv[2], sys.argv[3]
    if not os.path.exists(infile):
        raise FileExistsError(f'{infile} does not exist.')

    if operation in {'-c', '-v'}:
        with open(infile, 'rb') as fp:
            _message = fp.read()

        if operation == '-c':
            _message, _decoder_ring = compress(_message)
            with open(outfile, 'wb') as fp:
                marshal.dump((pickle.dumps(_decoder_ring), _message), fp)
        else:
            _message, _decoder_ring = encode(_message)
            print(_message)
            with open(outfile, 'wb') as fp:
                marshal.dump((pickle.dumps(_decoder_ring), _message), fp)

    else:
        with open(infile, 'rb') as fp:
            pickleRick, _message = marshal.load(fp)
            _decoder_ring = pickle.loads(pickleRick)

        if operation == '-d':
            bytes_message = decompress(array('B', _message), _decoder_ring)
        else:
            bytes_message = decode(_message, _decoder_ring)
        with open(outfile, 'wb') as fp:
            fp.write(bytes_message)
