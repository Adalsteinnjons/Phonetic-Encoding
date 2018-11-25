class HemmingDistance:

    def hemmingDistance(self,firstName, secondName,tol):
        totalError = 0
        lenFirstName = len(firstName)
        lenSecondName = len(secondName)
        totalError += abs(lenFirstName-lenSecondName)

        for x,y in zip(firstName,secondName):
            if x != y:
                totalError += 1
            # if totalError >= tol:
            #     break

        return totalError


    def fixTypo(self,name,lastnames):

        firstname, lastName = name.split(" ")
        finalFirstName = firstname
        finalLastName = lastName

        if lastName not in lastnames:
            for l in lastnames:
                error = self.hemmingDistance(lastName,l,2)
                if(error == 1):
                    finalLastName = l
                    break
                if(error == 2):
                    finalLastName = l

        return finalFirstName + " " + finalLastName


    def fixTypoFirstNames(self,name,dictionary):
        firstName, lastName = name.split(" ")
        finalFirstName = firstName
        finalLastName = lastName

        if firstName not in dictionary:
            for f in dictionary:
                error = self.hemmingDistance(firstName, f, 2)
                if (error == 1):
                    finalFirstName = f
                    break
                if (error == 2):
                    finalFirstName = f


        return finalFirstName + " " + finalLastName
