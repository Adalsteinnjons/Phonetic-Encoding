from hemmingDistance import HemmingDistance

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
print('HEMMING DISTANCE')
print('=============================================================')
print('True positive rate:')
print('Before the cleaning: %.2f'% trueRate(cleanedCorruptedNames,generatedNames), '%')


hd = HemmingDistance()

typoFixed = []
counter = 0
for name in cleanedCorruptedNames:
    counter += 1
    if (counter%1000 == 0):
        print(counter, ' names processed')
    typoFixed.append(hd.fixTypo(name,lastNamesDict))
#
# f = open("./preprocessed/noTypoLastNames.txt", "w+")
# for name in typoFixed:
#     if typoFixed[-1] == name:
#         f.write(name)
#     else:
#         f.write(name + '\n')

# typoFixed = extractWords('./preprocessed/noTypoLastNames.txt')
typoFixed = cleanDuplicate(typoFixed)
# print([value.split(" ") for value in typoFixed if len(value.split(" "))== 1 ])
print('After cleaning the lastnames: %.2f' % trueRate(typoFixed,generatedNames), '%')


maleFirstNamesDict.extend(femaleFirstNamesDict)

typoFixedFirstNames = []
counter = 0
for name in typoFixed:
    counter += 1
    if (counter%1000 == 0):
        print(counter,' names processed')
    typoFixedFirstNames.append(hd.fixTypoFirstNames(name,maleFirstNamesDict))
#
# f = open("./preprocessed/hemmingFinal.txt", "w+")
# for name in typoFixedFirstNames:
#     if typoFixedFirstNames[-1] == name:
#         f.write(name)
#     else:
#         f.write(name + '\n')

# typoFixedFirstNames = extractWords("./preprocessed/hemmingFinal.txt")
typoFixedFirstNames = cleanDuplicate(typoFixedFirstNames)
print('After cleaning the firstnames: %.2f' % trueRate(typoFixedFirstNames,generatedNames), '%')
print('=============================================================')

print('Number of eliminated Duplicates: ',len(corruptedNames)-len(typoFixedFirstNames), 'Names')









