def encode(message):
    code = ''.join(format(ord(x), 'b').zfill(8) for x in message)
    return code