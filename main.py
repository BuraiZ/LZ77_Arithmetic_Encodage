import code_bin
import code_ari
import message_generator
from LZ77 import LZ77Compressor

import argparse
import time
import xlwt
import numpy as np
import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, nargs='?', default="encoding_data")
parser.add_argument("-n", type=int, nargs='?', default=1)
parser.add_argument("-m", type=str, nargs='?')
parser.add_argument("-l", type=int, nargs='?')
parser.add_argument("-s", type=int, nargs='?')
parser.add_argument("-r", type=float, nargs='?')
parser.add_argument("-w", type=int, nargs='?', default=50)
args = parser.parse_args()



def write_data_to_spreadsheet(filename, data):
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")
    current_row = 3
    
    # header 1
    sheet.write_merge(1, 1, 1, 5, "Test Case")
    sheet.write_merge(1, 1, 6, 7, "Encodage binaire")
    sheet.write_merge(1, 1, 8, 10, "Encodage arithmétique")
    sheet.write_merge(1, 1, 11, 14, "Encodage LZW")
    
    # header 2
    sheet.write(2, 1, "No")
    sheet.write(2, 2, "Message")
    sheet.write(2, 3, "Longueur")
    sheet.write(2, 4, "Nombre de symbole")
    sheet.write(2, 5, "Taux de répétition")
    
    sheet.write(2, 6, "Code")
    sheet.write(2, 7, "Longueur (bits)")

    sheet.write(2, 8, "Code")
    sheet.write(2, 9, "Longueur (bits)")
    sheet.write(2, 10, "Taux de compression")
    sheet.write(2, 11, "Durée de compression")

    sheet.write(2, 12, "Code")
    sheet.write(2, 13, "Longueur (bits)")
    sheet.write(2, 14, "Taux de compression")
    sheet.write(2, 15, "Durée de compression")
    
    for entry in data:
        current_col = 1
        for field in entry:
            sheet.write(current_row, current_col, entry.get(field))
            current_col += 1
        current_row += 1
    
    book.save("./Results/" + filename + ".xls")

def get_number_of_symbol_from(message):
    ProbSymb =[[message[0], message.count(message[0])/len(message)]]
    nbsymboles = 1

    for i in range(1, len(message)):
        if not list(filter(lambda x: x[0] == message[i], ProbSymb)):
            ProbSymb += [[message[i], ProbSymb[-1][1]+message.count(message[i])/len(message)]]
            nbsymboles += 1
    
    return nbsymboles

def main(fArg, nArg, wArg, mArg=None, lArg=None, sArg=None, rArg=None):
    collected_data = []
    for i in range(1, nArg+1):
        # message generation
        if (mArg):
            message = mArg
        else:
            if (lArg == None or sArg == None or rArg == None):
                messageData = message_generator.generate(lArg, sArg, rArg)
            else:
                messageData = message_generator.generate()
            message = messageData.get('message')

        # binary encoding
        binary_code = code_bin.encode(message)
        
        # arithmetic encoding
        start_time = time.perf_counter()
        ari_code = code_ari.encode(message)
        ari_elapsed_time = time.perf_counter() - start_time
        
        # LZ77 encoding
        compressor = LZ77Compressor(window_size=wArg)
        start_time = time.perf_counter()
        lz77_code = compressor.compress(message)
        lz77_elapsed_time = time.perf_counter() - start_time
        
        entry = {
            "test_case": i,
            "message": message,
            "message_length": len(message),
            "message_n_symbol": get_number_of_symbol_from(message),
            "taux_de_repetition": messageData.get('test_case').get('repeat_prob'),

            "binary_code": binary_code,
            "binary_code_length": len(binary_code),

            "ari_code": "ERROR" if (ari_code == "NaN") else ari_code,
            "ari_code_length": "ERROR" if (ari_code == "NaN") else len(ari_code),
            "ari_code_compression_rate": "ERROR" if (ari_code == "NaN") else float(len(ari_code)/len(binary_code)),
            "ari_duration": "ERROR" if (ari_code == "NaN") else ari_elapsed_time,

            "lw77_code": "ERROR" if (lz77_code == "NaN") else lz77_code,
            "lw77_code_length": "ERROR" if (lz77_code == "NaN") else len(lz77_code),
            "lw77_code_compression_rate": "ERROR" if (lz77_code == "NaN") else float(len(lz77_code)/len(binary_code)),
            "lw77_duration": "ERROR" if (lz77_code == "NaN") else lz77_elapsed_time
        }
        collected_data.append(entry)
        pprint.pprint(entry)
        print("\n")
        print("----------------------------------------------------------------------")
        print("\n")

    write_data_to_spreadsheet(fArg, collected_data)

if __name__ == "__main__":
    main(args.f, args.n, args.w, args.m, args.l, args.s, args.r)
