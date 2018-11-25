import numpy as np

correct = open("cleaningDataset/LevenstheinNames.txt", 'w')

corrupt_txt_file = open("cleaningDataset/corruptedNames.txt", "r")
female_txt_file = open("cleaningDataset/femaleFirstnames.txt", "r")
male_txt_file = open("cleaningDataset/maleFirstnames.txt", "r")
lastnames_txt_file = open("cleaningDataset/lastnames.txt", "r")


def txtToList(txtFile):
    list = txtFile.read().split('\n')
    return list


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


# Calculates the Levensthein distance with matrices like in the youtube tutorial:
# https://www.youtube.com/watch?v=We3YDTzNXEk
def levensthein(Correct, Corrupt):
    sizeCorrect = len(Correct) + 1
    sizeCorrupt = len(Corrupt) + 1

    matrix = np.zeros((sizeCorrect, sizeCorrupt))
    for x in range(sizeCorrect):
        matrix[x, 0] = x
    for y in range(sizeCorrupt):
        matrix[0, y] = y

    for x in range(1, sizeCorrect):
        for y in range(1, sizeCorrupt):
            if Correct[x - 1] == Corrupt[y - 1]:
                matrix[x, y] = min(matrix[x - 1, y] + 1, matrix[x - 1, y - 1], matrix[x, y - 1] + 1)
            else:
                matrix[x, y] = min(matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1)
    LevDistance = matrix[sizeCorrect - 1, sizeCorrupt - 1]

    return LevDistance


def correctNames(Corrupted, Correct):
    correctedNames = [None for _ in range(len(Corrupted))]
    counter = 0
    for corruptIndex, n in enumerate(Corrupted):
        minDist = 20 #some value that will never bi the min value
        if (corruptIndex % 100 == 0):
            #To print out the progress. When it has reached 271 twice, the programm is finished.
            counter += 1
            print(counter)
        for correctIndex, m in enumerate(Correct):

            dist = levensthein(n, m)

            # Go through all names and find the Name that needs the least amount of changes, where the distance is the smallest
            if (dist <= minDist):
                minDist = dist
                idx = correctIndex

            #write the corrected name in the array. Gets over written each time we find a more likely name.
            correctedNames[corruptIndex] = Correct[idx]

    return correctedNames


correctedFirstnames = correctNames(corruptFirstnames, firstnames)
correctedLastnames = correctNames(corruptLastnames, lastnames)

correctedNames = list(zip(correctedFirstnames, correctedLastnames))

# remove identical values, set only has distinct values, however the order is lost
def removeIdenticalValues(someList):
    before = len(someList)
    output = list(set(someList))
    after = len(output)
    print(before - after, " duplicates eliminated")
    return output

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

#for the whole name
print("With Levenathein We have found", WholeNameMatchCounter, " identical matches")
print("That means our PTR is ", WholeNameMatchCounter/len(generatedNames))
