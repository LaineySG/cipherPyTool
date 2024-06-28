import math
import random


def shift_char(char,shift): #defaults to plus, for enc. use negative shift value for dec.
    result = ""
    result += chr((ord(char) + shift))
    return result

    #The ceasar cipher takes a message and shifts each character by a set shift-length.
def ceasar_cipher(message,shift,type):
    result = ""
    if (type == "dec"):
        shift = -shift
    for i in range(len(message)):
        char = message[i]
        result += shift_char(char,shift)
    return result

    #The vigenere cipher takes a message and shifts each character by a shift-length determined by the value of a repeating phrase or keyword.
def vigenere_cipher(message,key,type):
    result = ""
    keycursor=0
    for i in range(len(message)):
        if (keycursor >= len(key)):
            keycursor = 0
        char = message[i]
        
        if (type == "enc"):
            shift = ord(key[keycursor])
        elif (type == "dec"):
            shift = -ord(key[keycursor])
            
        keycursor+=1
        result += shift_char(char,shift)
    return result

    #The atbash cipher takes a message and reverses all letters in the string. This version does numbers as well.
def atbash_cipher(message):
    result = ""
    for i in range(len(message)):
        char = message[i]
        if (char.isspace()):
            result += char
        elif (char.isupper()): #65
            result += chr(25 - (ord(char) - 65) + 65) #ord(char) - 65 gives us the ASCII from 0 to 25 (of 26). We then subtract 25 from it, add 65 back.
        elif (char.islower()): #97
            result += chr(25 - (ord(char) - 97) + 97)
        elif (char.isnumeric()):
            result += str((9-int(char)))
        else:
            result += char
    return result

    #The rot13 cipher takes a message and shifts each char by 13. This makes it very simple to shift messages back and forth.
def rot13_cipher(message):
    result = ""
    for i in range(len(message)):
        char = message[i]
        if (char.isspace() or char.isnumeric()):
            result += char
        elif (char.isupper()): #65
            result += chr((ord(char) - 65 + 13) % 26 + 65) #take char, convert to 0-26 ascii, add 13 (shift 13), modulo 26 (so result will be 0-26).
        elif (char.islower()): #97
            result += chr((ord(char) - 97 + 13) % 26 + 97)
        else:
            result += char
    return result
def affine_cipher(message, a, b, type): #a is multiplicative, b is additive shift
    result = ""
    for i in range(len(message)):
        char = message[i]
        if (char.isspace() or char.isnumeric()):
            result += char
        elif (char.isupper()): #65
            if (type == "dec"):
                result += chr(math.floor((((ord(char) - 65) - b) / a) % 26 + 65))
            else:
                result += chr(math.floor(((ord(char) - 65) * a + b) % 26 + 65)) #take char, convert to 0-26 ascii, do operations, modulo 26 (so result will be 0-26).
        elif (char.islower()): #97
            if (type == "dec"):
                result += chr(math.floor((((ord(char) - 97) - b) / a) % 26 + 97))
            else:
                result += chr(math.floor(((ord(char) - 97) * a + b) % 26 + 97))
        else:
            result += char
    return result
def baconian_cipher(message,type):
    #all ascii chars will be converted to a digit 0 to 26, then to 5-bit binary
    #Once in binary we will have strings like 01010, we can convert to azaza. Then we will generate a string of random numbers, where:
    #0,1,2,3,4 are a and 5,6,7,8,9 are Z. We will also add padding to ensure it's a minimum of 50 bits (padding will be all a/0's)
    result = ""
    if (type == "enc"):
        for i in range(len(message)):
            char = message[i]
            if (char.isspace() or char.isnumeric()):
                result += char
            elif (char.isupper()): #65
                char_dec = (ord(char)-65)
                char_bin = bin(char_dec)[2:].zfill(5)
                for i in range(len(char_bin)):
                    if (char_bin[i] == '0'):
                        result += str(random.randint(0,4))
                    else:
                        result += str(random.randint(5,9))
            elif (char.islower()): #97
                char_dec = (ord(char)-97)
                char_bin = bin(char_dec)[2:].zfill(5)
                for i in range(len(char_bin)):
                    if (char_bin[i] == '0'):
                        result += str(random.randint(0,4))
                    else:
                        result += str(random.randint(5,9))
            else:
                result += char
    else: #dec
        result= ""
        numberList = []
        binDec = 0
        for i in range(len(message)):
            if (message[i].isnumeric()):              
                numberList.append(int(message[i]))
                if (int(message[i]) >= 5):
                    binDec += (2 ** (5- len(numberList))) #if number is high enough add the thing
                if (len(numberList) >= 5):
                    result += chr(binDec + 97)
                    binDec = 0
                    numberList = []
            else:
                result += message[i]
    return result
def railfence_cipher(message,rails,type):
    railmatrix = []
    result = ''
    cursor = 0
    dir = -1 #-1 is down, 1 is up
    for i in range(rails): #for each rail
        railmatrix.append([]) #add a 'row'
    if (type == "enc"):
        for i in range(len(message)):
            railmatrix[cursor].append(message[i])
            if (dir == -1): #down
                cursor+=1
            else: #up
                cursor -=1
            if (cursor == (rails-1) or cursor == 0):
                dir = -dir
        #so now we have the railmatrix made up
        for i in range(rails):
            for j in range(len(railmatrix[i])):
                result += railmatrix[i][j]
    else:
        railmatrix = [[' ' for i in range(len(message))] for j in range(rails)] #Create and populate the matrix w/ empty columns and rows
        dir = -1
        row, col = 0, 0 #col and row cursors    

        #Now we mark the rows to fill
        for i in range(len(message)):
            if row == 0:
                dir = 1
            if row == (rails - 1):
                dir = -1
            railmatrix[row][col] = '*'
            col += 1
            
            # find next row
            if (dir == 1):
                row += 1
            else:
                row -= 1
                
        # Fill the rail matrix w/ the correct item
        cursor = 0
        for i in range(rails):
            for j in range(len(message)):
                if ((railmatrix[i][j] == '*') and (cursor < len(message))): #if marked and not out of bounds
                    railmatrix[i][j] = message[cursor]
                    cursor += 1
            
        # Reconstruct original message by reading in zig-zag
        result = []
        row, col = 0, 0
        for i in range(len(message)):
            
            # check the direction of flow
            if row == 0:
                dir = 1
            if row == rails-1:
                dir = -1
                
            #Fill the spaces
            if (railmatrix[row][col] != '*'):
                result.append(railmatrix[row][col])
                col += 1
                
            # find the next row using
            # direction flag
            if (dir == 1):
                row += 1
            else:
                row -= 1
        result = "".join(result)
        
    return result

def polybius_cipher(message, type):
    polybius_square = [
    ['a','b','c','d','e'],
    ['f','g','h','i','j'],
    ['k','l','m','n','o'], 
    ['p','q','r','s','t'],
    ['u','v','w','x','y']]
    message = message.lower()
    result = ''
    if (type == "enc"):
        for i in range(len(message)):
            found = False
            for j in range(0,5):
                if (message[i] in polybius_square[j]):
                    found = True
                    idx = polybius_square[j].index(message[i])
                    if ((j+1) >= 5):
                        result += polybius_square[0][idx]
                    else:
                        result += polybius_square[j+1][idx]
            if (found == False):
                result += message[i]
    else:
        for i in range(len(message)):
            found = False
            for j in range(0,5):
                if (message[i] in polybius_square[j]):
                    found = True
                    idx = polybius_square[j].index(message[i])
                    if ((j-1) <0):
                        result += polybius_square[4][idx]
                    else:
                        result += polybius_square[j-1][idx]
            if (found == False):
                result += message[i]
    return result
def simplesub_ciper(message,seed, type):
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u,','v','w','x','y','z']
    message = message.lower()
    random.seed(seed)
    random.shuffle(alpha)
    result = ''
    if (type == "enc"):
        for i in range(len(message)):
            if (message[i].islower()):
                asciiDec = (ord(message[i]) - 97)
                if (asciiDec < 26):
                    result += alpha[asciiDec]
            else:
                result += message[i]
    else:
        for i in range(len(message)):
            if (message[i].islower()):
                idx = alpha.index(message[i])
                result += chr(idx + 97 )
            else:
                result += message[i]


    return result
def columntranspo_cipher(message,key,type):
    result = ''
    dict = {}
    if (type=="enc"):
        for i in range(len(key)):
            #one column
            dict[key[i]] = [] #sets the dictionary key item equal to an empty array

        #Now table is made up of key # of columns, now we fill it w/ values
        cursor = 0
        for i in range(len(message)):
            #for each char in msg
            dict[key[cursor]].append(message[i]) #append message to dictionary at key
            cursor+=1 #append the char to the specified column and increment cursor
            if (cursor >= (len(key))):
                cursor = 0

        #Here is where we sort the dictionary keys alphabetically
        keylist = list(dict.keys())
        keylist.sort()
        alpha_dict = {i: dict[i] for i in keylist}

        for i in range(len(key)):
            newitems = ''.join(dict[keylist[i]])
            result += newitems
    else: #decrypt message
        
        for i in range(len(key)):
            #one column
            dict[key[i]] = [] #sets the dictionary key item equal to an empty array


        #Now that we have the empty dict w/ keys, we must sort it alphabetically. 
        keylist = list(dict.keys())
        keylist.sort()
        alpha_dict = {i: dict[i] for i in keylist}

        #Now table is made up of key # of columns, now we fill it w/ values
        cursor = 0
        for i in range(len(message)):
            #for each char in msg
            dict[key[cursor]].append(message[i]) #append message to dictionary at key
            cursor+=1 #append the char to the specified column and increment cursor
            if (cursor >= (len(key)-1)):
                cursor = 0

        returnedlist = {}
        #Now we must sort in the correct order again to recover message 
        for i in range(len(key)):
            for j in range(len(key)):
                if key[i] == dict[keylist[j]]:
                    returnedlist[key[i]] = dict[keylist[i]]
                    break

        #then we print
        for i in range(len(key)):
            newitems = ''.join(returnedlist[key[i]])
            result += newitems
        #
    
    return result;
    
        


def main():
    pt = "secretcode"
    print(pt)
    ciph = columntranspo_cipher(pt,"beach","enc")
    print(ciph)
    pt2 = columntranspo_cipher(ciph, "beach", "dec")
    print(pt2)

if __name__ == "__main__":
    main()