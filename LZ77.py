import math
import numpy as np
from bitarray import bitarray

class LZ77Compressor:
    """
    A simplified implementation of the LZ77 Compression Algorithm
    """
    MAX_WINDOW_SIZE = 400

    def __init__(self, window_size=20):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE) 
        self.lookahead_buffer_size = 15 # length of match is at most 4 bits

    def compress(self, message, output_file_path=None, verbose=True):
        """
        Given the path of an input file, its content is compressed by applying a simple 
        LZ77 compression algorithm. 

        The compressed format is:
        0 bit followed by 8 bits (1 byte character) when there are no previous matches
            within window
        1 bit followed by 12 bits pointer (distance to the start of the match from the 
            current position) and 4 bits (length of the match)
        
        If a path to the output file is provided, the compressed data is written into 
        a binary file. Otherwise, it is returned as a bitarray

        if verbose is enabled, the compression description is printed to standard output
        """
        data = None
        i = 0
        number_bit_size = int(np.ceil(np.log2(len(message))))
        data = bytes(message, encoding='utf-8')
        code = ""

        while i < len(data):
            #print i

            match = self.findLongestMatch(data, i)

            if match: 
                # Add 1 bit flag, followed by 12 bit for distance, and 4 bit for the length
                # of the match 
                (bestMatchDistance, bestMatchLength) = match

                code += "1"
                code += format(bestMatchDistance, 'b').zfill(number_bit_size)
                code += format(bestMatchLength, 'b').zfill(number_bit_size)

                #if verbose:
                    #print("<1, %i, %i>" % (bestMatchDistance, bestMatchLength))

                i += bestMatchLength

            else:
                code += "0"
                code += format(ord(data[i:i+1]), 'b').zfill(8)
                
                #if verbose:
                    #print("<0, %s>" % data[i:i+1].decode("utf-8"))

                i += 1

        # an output file path was not provided, return the compressed data
        return format(number_bit_size, 'b').zfill(4) + code


    def findLongestMatch(self, dataByte, current_position):
        """ 
        Finds the longest match to a substring starting at the current_position 
        in the lookahead buffer from the history window
        """
        data = dataByte.decode("utf-8")
        end_of_buffer = min(current_position + self.lookahead_buffer_size, len(data) + 1)

        best_match_distance = -1
        best_match_length = -1

        # Optimization: Only consider substrings of length 2 and greater, and just 
        # output any substring of length 1 (8 bits uncompressed is better than 13 bits
        # for the flag, distance, and length)
        for j in range(current_position + 2, end_of_buffer):

            start_index = max(0, current_position - self.window_size)
            substring = data[current_position:j]

            for i in range(start_index, current_position):

                repetitions = len(substring) / (current_position - i)

                last = len(substring) % (current_position - i)

                matched_string = data[i:current_position] * int(repetitions) + data[i:i+last]

                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_position - i 
                    best_match_length = len(substring)

        if best_match_distance > 0 and best_match_length > 0:
            return (best_match_distance, best_match_length)
        return None


