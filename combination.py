def intersection(list1,list2):
    list3 = list(set(list1) & set(list2))
    return list3

def union(list1, list2):
    list3 = list(set(list1 + list2))
    return list3

def extractWords(path):
    text = open(path, 'r')
    text = text.read()
    text = [s.strip() for s in text.split('\n')]
    return text

def cleanDuplicate(names):
    return list(set(names))

def trueRate(names,controlList):
    return (len(intersection(names,controlList))/len(controlList)) * 100

generatedPath = './cleaningDataset/generatedNames.txt'
generatedNames = extractWords(generatedPath)

hemming = extractWords('./preprocessed/noTypoLastNames.txt')
jaccard = extractWords('./preprocessed/jaccardFinal.txt')
levenstein = extractWords('./cleaningDataset/LevenstheinNames.txt')
soundex = extractWords('./cleaningDataset/SoundexNames.txt')

unionJaccardHemming = union(hemming,jaccard)
mitLevenStein = union(unionJaccardHemming,levenstein)
mitSoundex = union(mitLevenStein,soundex)
final = cleanDuplicate(mitSoundex)
print(len(final))
print(trueRate(final,generatedNames))


