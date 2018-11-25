import numpy as np
class CleverCombo:

    # self explained, importance: we don't eliminate duplicates
    def union(self,list1,list2):
        list3 = (list1+list2)
        return list3

    # create nGram string. you -> [##y,#yo,you,ou#,u##] for 3grams
    def nGrams(self,name,n):
        result = []
        for i in range(n-1):
            name = '#'+name+'#'
        start = 0
        for i in range(len(name)-(n-1)):
            result.append(name[start:start+n])
            start += 1
        return result

    # calculate the jaccard distance between 2 strings
    def jaccardDistance(self, name1, name2):
        nGramA = self.nGrams(name1,3)
        nGramB = self.nGrams(name2,3)
        intersec = [value for value in nGramA if value in nGramB]
        a = len(intersec)
        b = self.union(name1,name2)
        b = len(b)
        c = 1-(a/b)
        return c

    def levensthein(self,Correct, Corrupt):
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

    # used to clean lastnames using lastnames dictionary.
    # for performance, break if jaccardDistance ist smaller than 0.5
    # else, find the best.
    def fixTypo(self,name,lastNames):
        firstname, lastName = name.split(" ")
        finalFirstName = firstname
        finalLastName = lastName

        if lastName not in lastNames:
            bestscore = 100
            bestname = ''
            for l in lastNames:
                if abs(len(lastName)-len(l)) < 2:
                    score = self.jaccardDistance(lastName, l)
                    if (score < 0.6):
                        finalLastName = l
                        break
                    if score >= 0.6:
                        leven = self.levensthein(lastName,l)
                        if leven < bestscore:
                            bestscore = leven
                            bestname = l
                        finalLastName = bestname

        return finalFirstName + " " + finalLastName

    def fixTypoFirstNames(self,name,dictionary):
        firstname, lastName = name.split(" ")
        finalFirstName = firstname
        finalLastName = lastName

        if firstname not in dictionary:
            bestscore = 1
            bestname = ''
            for l in dictionary:
                aa = abs(len(firstname)-len(l))
                if aa < 2:
                    score = self.jaccardDistance(firstname, l,)
                    if score < 0.6:
                        finalFirstName = l
                        break
                    elif score >= 0.6:
                        leven = self.levensthein(lastName, l)
                        if leven < bestscore:
                            bestscore = leven
                            bestname = l
                        finalFirstName = bestname

        return finalFirstName + " " + finalLastName