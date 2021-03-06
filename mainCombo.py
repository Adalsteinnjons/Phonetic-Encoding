from cleverCombo import CleverCombo

# Pleaser remove emptyline at the end of the .txt file before proceeding

def extractWords(path):
    text = open(path, 'r')
    text = text.read()
    text = [s.strip() for s in text.split('\n')]
    return text

def intersection(list1,list2):
    list3 = list(set(list1) & set(list2))
    return list3

def cleanDuplicate(names):
    return list(set(names))

def trueRate(names,controlList):
    return (len(intersection(names,controlList))/len(controlList)) * 100

corruptPath = './cleaningDataset/corruptedNames.txt'
femalePath = './cleaningDataset/femaleFirstnames.txt'
malePath = './cleaningDataset/maleFirstnames.txt'
lastNamesPath = './cleaningDataset/lastnames.txt'
generatedPath = './cleaningDataset/generatedNames.txt'

corruptedNames = extractWords(corruptPath)
femaleFirstNamesDict = extractWords(femalePath)
maleFirstNamesDict = extractWords(malePath)
lastNamesDict = extractWords(lastNamesPath)
generatedNames = extractWords(generatedPath)

cleanedCorruptedNames = cleanDuplicate(corruptedNames)
print('=============================================================')
print('CLEVER COMBO')
print('=============================================================')
print('True positive rate:')
print('Before the cleaning: %.2f'% trueRate(cleanedCorruptedNames,generatedNames), '%')


combo = CleverCombo()

typoFixed = []
counter = 0
# append the fixed name to typofixed array.
for name in cleanedCorruptedNames:
    counter += 1
    if (counter%1000 == 0):
        print(counter, ' names processed')
    typoFixed.append(combo.fixTypo(name, lastNamesDict))


# typoFixed = extractWords('./preprocessed/jaccardLastNames.txt')
typoFixed = cleanDuplicate(typoFixed)
print('After cleaning the lastnames: %.2f' % trueRate(typoFixed,generatedNames), '%')

maleFirstNamesDict.extend(femaleFirstNamesDict)

typoFixedFirstNames = []
counter = 0
for name in typoFixed:
    counter += 1
    if (counter%1000 == 0):
        print(counter, ' names processed')
    typoFixedFirstNames.append(combo.fixTypoFirstNames(name, maleFirstNamesDict))


# typoFixedFirstNames = extractWords("./preprocessed/jaccardFinal.txt")
typoFixedFirstNames = cleanDuplicate(typoFixedFirstNames)
print('After cleaning the firstnames: %.2f' % trueRate(typoFixedFirstNames,generatedNames), '%')

print('=============================================================')
print('Number of eliminated Duplicates: ',len(corruptedNames)-len(typoFixedFirstNames), 'Names')