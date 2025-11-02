import random as rand
import array

keyLength = 50
bases = ["X", "Z"]
keyBits = [0, 1]
eve = False

#Generate initial key
aliceKey = [rand.choice(keyBits) for _ in range(keyLength)]
print("Initial key: ", end='')
print(aliceKey)

#Create basis strings
def generateBasis():
    return [rand.choice(bases) for _ in range(keyLength)]

aliceBasis = generateBasis()
bobBasis = generateBasis()
print("Alice Basis: " + ''.join(aliceBasis))
print("Bob Basis: " + ''.join(bobBasis))


# Encodes the message into 0, 1, +, 1 etc. depending on Alice's basis. 
# This means basis of message doesn't need to be stored elsewhere because it is 
# inherently present in the message string.
def encode(key, basis):
    encodedKey = []
    for i in range(keyLength):
        if (basis[i] == "X"):
            if(key[i] == 0):
                encodedKey.append("+")
            else:
                encodedKey.append("-")
        else:
            #If basis is Z
            if (key[i] == 0):
                encodedKey.append("0")
            else:
                encodedKey.append("1")
    return encodedKey

aliceEncodedKey = encode(aliceKey, aliceBasis)
print("Alice encoded key: ", end='')
print(''.join(aliceEncodedKey))

# Set current message to key sent from alice
currentMessage = aliceEncodedKey

#Decoding function which recieves encoded key list of +, -, 0 or 1, and decodes it based on the measure basis. 
def decode(keyEncoded, measureBasis):
    decodedKey = []

    for i in range(keyLength):
        if (measureBasis[i] == "Z"):
            if(keyEncoded[i] == "0"):
                decodedKey.append(0)
            elif (keyEncoded[i] == "1"):
                decodedKey.append(1)
            else:
                decodedKey.append(rand.choice(keyBits))
        elif (measureBasis[i] == "X"):
            if(keyEncoded[i] == "+"):
                decodedKey.append(0)
            elif (keyEncoded[i] == "-"):
                decodedKey.append(1)
            else:
                decodedKey.append(rand.choice(keyBits))
    
    return decodedKey

#Find the probability of a mismatch between items in two arrays
def checkError(arr1, arr2):
    count = 0

    for i, value in enumerate(arr1):
        if (arr1[i] != arr2[i]):
            count += 1
    return count / len(arr1)

#If Eve Intercepts the message.
eveBasis = generateBasis()
eveDecoded = []
if (eve):
    eveDecoded = decode(currentMessage, eveBasis)
    print("Eve Basis: " + ''.join(eveBasis))
    
    #Because Eve doesn't know the original bases, she recodes the message using her guess
    currentMessage = encode(eveDecoded, eveBasis)

    #Print results
    print("Eve decoded key: ", end='')
    print(eveDecoded)
    print("Eve re-encoded key: ", end='')
    print(''.join(currentMessage))



# Decodes Key sent by Alice using Alice Basis (should be identical without Eve)
aliceDecoded = decode(currentMessage, aliceBasis)
print("Alice decoded key: ", end='')
print(aliceDecoded)

#Decodes key sent by Alice using bob basis (should be 25% error rate before sifting)
bobDecoded = decode(currentMessage, bobBasis)
print("Bob decoded key: ", end='')
print(bobDecoded)

#Prints Error of unsifted bob key (should approach 0.25 as keyLength -> inf)
errorBob = checkError(bobDecoded, aliceDecoded)
print(errorBob)


# Transform keys and basis depending on Eve's measurements
def eve(key, basis): 
    return key, basis

finAliceKey, finAliceBases = eve(aliceKey, aliceBasis)




