import numpy as np
import decimal

MAX_POWER = 1500

def encode(message):
    Message = message

    # Calculate first symbol frequency
    FreqSymb =[[Message[0], Message.count(Message[0])]]
    ProbSymb =[[Message[0], Message.count(Message[0])/len(Message)]]
    nbsymboles = 1

    # Find new unique symbol and calculate the interval range for each symbol
    for i in range(1, len(Message)):
        if not list(filter(lambda x: x[0] == Message[i], ProbSymb)):
            count = Message.count(Message[i])
            FreqSymb += [[Message[i], count]]
            ProbSymb += [[Message[i], ProbSymb[-1][1]+count/len(Message)]]
            nbsymboles += 1
    
    Code = ProbSymb[:]
    Code = [['', 0]] + ProbSymb[:]
    
    for i in range(len(Message)): 
        #Cherche dans quel intervalle est le symbole à coder
        temp = list(filter(lambda x: x[0] == Message[i], Code))
        indice = Code.index(temp[0])

        #Calcul des bornes pour coder le caractère
        Debut = decimal.Decimal(Code[indice-1][1])
        Plage = decimal.Decimal(Code[indice][1]) - Debut
        #print(Message[i], ' est dans l\'intervalle', indice, ' de ', Debut, ' à ', Debut + Plage)
        #print()      
        #Nouveaux intervalles pour coder le prochain symbole
        Code = [['', Debut]]  
        for j in range(len(ProbSymb)):
            Code += [[ProbSymb[j][0], Debut+decimal.Decimal(ProbSymb[j][1])*Plage]]
            
        #print(Code)

    ok = True
    valfinal = 0
    p = 0
    while ok:
        p += 1
        if (p >= MAX_POWER):
            valfinal = "NaN"
            break
        #else:
            #print(p)
        #Essayer différentes sommes de puissance négative de 2
        valfinal += decimal.Decimal(np.power(2.0,-p))
        if valfinal > (Debut + Plage):
            valfinal -= decimal.Decimal(np.power(2.0,-p)) #Hors de la borne maximale, on annule l'ajout.
        elif valfinal > Debut :
            ok = False

    #print(valfinal)
    # Too much precision needed
    if (valfinal == "NaN"):
        return valfinal

    #Table hex vers binaire
    hex2bin = dict('{:x} {:04b}'.format(x,x).split() for x in range(16))

    def float_dec2bin(d):
        hx = float(d).hex() #Conversion float vers hex
        p = hx.index('p')
        #Conversion hex vers bin avec la table
        bn = ''.join(hex2bin.get(char, char) for char in hx[2:p])

        #return ( bn.strip('0') + hx[p:p+2] + bin(int(hx[p+2:]))[2:])
        return ("0"*(int(hx[p+2:])-1) + "1" + bn.strip('0')[2:])

    messagecode = float_dec2bin(valfinal)

    plageCode = ""
    number_bit_size = int(np.ceil(np.log2(len(message))))
    for symb in FreqSymb:
        plageCode += format(ord(symb[0]), 'b').zfill(8)
        plageCode += format(symb[1], 'b').zfill(number_bit_size)
    plageCode += "11111111"     #charactere special pour séparer la plage du message codé

    numberbitlengthCode = format(number_bit_size, 'b').zfill(4)

    code = numberbitlengthCode + plageCode + messagecode

    longueur = messagecode.count('0') + messagecode.count('1') + messagecode.count('-')
    
    #print("Longueur = {0}".format(longueur))

    return code
