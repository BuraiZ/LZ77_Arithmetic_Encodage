import random
import time

MIN_MESSAGE_LENGTH = 2
MAX_MESSAGE_LENGTH = 50

MIN_RANDOM_SYMBOL = 2
MAX_RANDOM_SYMBOL = 26

MIN_REPEAT_PROB = 0
MAX_REPEAT_PROB = 0.8

MIN_REPEAT_LENGTH = 1
MAX_REPEAT_LENGTH = 5

TIMEOUT = 2

SYMBOLS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def get_number_of_unique_symbol_from(message):
    ProbSymb =[[message[0], message.count(message[0])/len(message)]]
    nbsymboles = 1

    for i in range(1, len(message)):
        if not list(filter(lambda x: x[0] == message[i], ProbSymb)):
            ProbSymb += [[message[i], ProbSymb[-1][1]+message.count(message[i])/len(message)]]
            nbsymboles += 1
    
    return nbsymboles

def get_random_message_length():
    return random.randint(MIN_MESSAGE_LENGTH, MAX_MESSAGE_LENGTH-1)

def get_random_number_of_symbol():
    return random.randint(MIN_RANDOM_SYMBOL, MAX_RANDOM_SYMBOL-1)

def get_random_repeat_probability():
    return random.uniform(MIN_REPEAT_PROB, MAX_REPEAT_PROB)

def get_random_symbol_from(array):
    return SYMBOLS[random.randint(0, len(array)-1)]

def get_available_symbol_array(n_symb):
    return SYMBOLS[:n_symb]

def generate_random_test_case():
    return {
        "length": get_random_message_length(),
        "n_symbol": get_random_number_of_symbol(),
        "repeat_prob": get_random_repeat_probability()
    }

def generate_test_case(length, n_symbol, repeat_prob):
    if (length == None or n_symbol == None or repeat_prob == None):
        test_case = {
            "length": get_random_message_length() if (length == None) else length,
            "n_symbol": get_random_number_of_symbol() if (n_symbol == None) else n_symbol,
            "repeat_prob": get_random_repeat_probability() if (repeat_prob == None) else repeat_prob
        }
        test = test_case
    else:
        test = generate_random_test_case()

    # make sure that the length is never lower than the number of unique symbol
    valid = test.get('length') >= test.get('n_symbol')
    while not(valid):
        test = generate_test_case(length, n_symbol, repeat_prob)
        valid = test.get('length') >= test.get('n_symbol')
    
    return test

def generate_message(test_case):
    message = []
    symbols = get_available_symbol_array(test_case.get('n_symbol'))

    valid = False  #Message is valid if it has AT LEAST 2 different symbols

    start_time = time.time()
    while not(valid):
        if (time.time() - start_time > TIMEOUT):
            return None

        message = []
        while len(message) < test_case.get('length'):
           # reuse the symbols in the message to create a repeat effect
            if (random.uniform(0, 1) < test_case.get('repeat_prob') and len(message) > 0):
                repeat_start_point = random.randint(0, len(message)-1)
                repeat_length = random.randint(MIN_REPEAT_LENGTH, MAX_REPEAT_LENGTH)

                repeated_symbols = message[repeat_start_point:repeat_start_point+repeat_length]
                message = message + repeated_symbols

                if (len(message) > test_case.get('length')):
                    message = message[:test_case.get('length')]
            else:
                message.append(get_random_symbol_from(symbols))
        
        nSymb = get_number_of_unique_symbol_from(message)
        valid = nSymb > 1 and nSymb == test_case.get('n_symbol')

    return ''.join(message)

def generate(length=None, n_symbol=None, repeat_prob=None):
    test = generate_test_case(length, n_symbol, repeat_prob)

    message = generate_message(test)
    while (message == None):
        test = generate_test_case(length, n_symbol, repeat_prob)
        message = generate_message(test)
    
    return { "message": message, "test_case": test}
