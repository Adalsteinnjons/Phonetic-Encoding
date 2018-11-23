correct = open("cleaningDataset/correctedNames.txt", 'w')

corrupt_txt_file = open("cleaningDataset/corruptedNames.txt", "r")
female_txt_file = open("cleaningDataset/femaleFirstnames.txt", "r")
male_txt_file = open("cleaningDataset/maleFirstnames.txt", "r")
lastnames_txt_file = open("cleaningDataset/lastnames.txt", "r")


def txtToList(txtFile):
    list = txtFile.read().split('\n')
    return list

#comment
corrupt = txtToList(corrupt_txt_file)
female = txtToList(female_txt_file)
male = txtToList(male_txt_file)
lastnames = txtToList(lastnames_txt_file)


# remove identical values, set only has distinct values, however the order is lost
def removeIdenticalValues(someList):
    before = len(someList)
    output = list(set(someList))
    after = len(output)
    print(before - after, " duplicates eliminated")
    return output

def splitFnLnList(FnLnList):
    Fn = []
    Ln = []
    for names in FnLnList:
        splitlist = names.split()
        Fn.append(splitlist[0])
        Ln.append(splitlist[1])

    return Fn, Ln


# to split FN and LN in the corrupt words list
corruptFirstnames, corruptLastnames = splitFnLnList(corrupt)


# merge male first name and female first name together
firstnames = female + male


# Does the soundex encoding for any given string input in uppercase
def soundex(inputString):
    output = ""
    output += inputString[0]

    dictionary = {"BFPV": "1", "CGJKQSXZ": "2", "DT": "3", "L": "4", "MN": "5", "R": "6", "AEIOUHWY": "."}

    for char in inputString[1:]:  # rest vom string ohne das erste Element
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if code != output[-1]:  # to not allow duplicates
                    output += code

    output = output.replace(".", "")  # replace dot with empty
    output = output[:4].ljust(4, "0")  # only the first 4 values are used and the filled up with 0 if it is less

    return output


# takes a list and returns list with soundex encodings
def listToSoundex(list):
    soundexList = []
    for e in list:
        soundexList.append(soundex(e))
    return soundexList


corruptFirstnamesSoundex = listToSoundex(corruptFirstnames)
corruptLastnamesSoundex = listToSoundex(corruptLastnames)
firstnamesSoundex = listToSoundex(firstnames)
lastnamesSoundex = listToSoundex(lastnames)

# compares and checks if the encodings from the correct names and the corrupted are the same,
# if they are the same it replaces the corrupted with the correct version.
def correctNames(corruptNamesSoundex, correctNamesSoundex, correctNames, corruptNames):
    correctedNames = [None for _ in range(len(corruptNames))]
    noMatchCounter = 0

    for index, entry in enumerate(corruptNames):
        if entry in correctNames:
            correctedNames[index] = entry
        else:
            if corruptNamesSoundex[index] in correctNamesSoundex:
                correctedNames[index] = correctNames[(correctNamesSoundex.index(corruptNamesSoundex[index]))]
            else: noMatchCounter += 1





    print(correctedNames)
    print(len(correctedNames))

    return correctedNames, noMatchCounter


correctedFirstnames, noMatchFN = correctNames(corruptFirstnamesSoundex, firstnamesSoundex, firstnames, corruptFirstnames)
correctedLastnames, noMatchLN = correctNames(corruptLastnamesSoundex, lastnamesSoundex, lastnames, corruptLastnames)
print(noMatchFN, " No-matches found in firstnames")
print(noMatchLN, " No-matches found in lastnames")

correctedNames = list(zip(correctedFirstnames, correctedLastnames))

#remove the duplicates
correctedNames = removeIdenticalValues(correctedNames)

#Get the corrected name list into a file
correct.write('\n'.join('{} {}'.format(x[0],x[1]) for x in correctedNames))

#compare the corrected and the generated names list and see how many machtes we have
generatedNames_txt_file = open("cleaningDataset/generatedNames.txt", "r")
generatedNames = txtToList(generatedNames_txt_file)
# split and the zipped to get the same format to compare
generatedFN, generatedLN = splitFnLnList(generatedNames)
generatedNames = list(zip(generatedFN,generatedLN))

def findMatches(list1, list2):
    return len(list(set(list1) & set(list2)))

WholeNameMatchCounter = findMatches(generatedNames,correctedNames)

corruptZippednames = list(zip(corruptFirstnames,corruptLastnames))

# check how many corrupt matches
CorruptCounter = findMatches(corruptZippednames, generatedNames)
print("Without any optimization we have ", CorruptCounter, "idendical matches")
#for the whole name
print("With Soundex We have found", WholeNameMatchCounter, " identical matches")
print("That means our PTR is ", WholeNameMatchCounter/len(generatedNames))

#remove duplicates int the FN, LN list
correctedFirstnames = removeIdenticalValues(correctedFirstnames)
correctedLastnames = removeIdenticalValues(correctedLastnames)
generatedFN = removeIdenticalValues(generatedFN)
generatedLN = removeIdenticalValues(generatedLN)

FNMatchCounter = findMatches(generatedFN, correctedFirstnames)
LNMatchCounter = findMatches(generatedLN,correctedLastnames)

#for the first names
print("We have found", FNMatchCounter, " identical matches if we only look at FN")
print("The True Positive Rate for FN is", FNMatchCounter/(len(generatedFN)))

#for the last names
print("We have found", LNMatchCounter, " identical matches if we only look at LN")
print("The True Positive Rate for LN is", LNMatchCounter/(len(generatedLN)))


