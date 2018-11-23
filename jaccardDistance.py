
class JaccardDistance:

    def intersection(self, list1, list2):
        list3 = list(set(list1) & set(list2))
        return list3

    def union(self,list1,list2):
        list3 = set(list1+list2)
        return list3

    def jaccardDistance(self, name1, name2):
        a = self.intersection(name1, name2)
        b = self.union(name1,name2)
        a = len(a)
        b = len(b)
        c = 1-(a/b)
        return c

    def fixTypo(self,name,lastNames):
        firstname, lastName = name.split(" ")
        finalFirstName = firstname
        finalLastName = lastName

        if lastName not in lastNames:
            for l in lastNames:
                if abs(len(lastName)-len(l)) < 2:
                    score = self.jaccardDistance(lastName, l,)
                    if (score < 0.13):
                        finalLastName = l
                        break
                    if score < 0.25:
                        finalLastName = l

        return finalFirstName + " " + finalLastName