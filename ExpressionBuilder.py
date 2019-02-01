
class ExpressionBuilder:
    def __init__(self):
        self.wordNumberMap = self.createWordMap()
        self.invert = True
        self.noInvert = False
        self.prefix = True
        self.noPrefix = False
        self.suffix = False

    def buildBinaryExpression(self, wordsList, separator, operation, invert, prefix):
        if len(separator.split()) > 1:
            sep = wordsList.index(separator.split()[0])
            separatorLen = len(separator.split())
        else:
            sep = wordsList.index(separator)
            separatorLen = 1

        if prefix:
            arg1 = self.convertTextToNumber(wordsList[1:sep])
        else:
            arg1 = self.convertTextToNumber(wordsList[:sep])

        arg2 = self.convertTextToNumber(wordsList[sep+separatorLen:])

        if invert:
            expression = str(arg2) + " " + operation + " " + str(arg1)
        else:
            expression = str(arg1) + " " + operation + " " + str(arg2)

        return expression

    def buildUnaryExpression(self, wordsList, operator, function, isArgPrefix, isResultPrefix):

        operatorLen = len(operator.split())
        if isArgPrefix:
            arg1 = self.convertTextToNumber(wordsList[:-operatorLen])
        else:
            arg1 = self.convertTextToNumber(wordsList[operatorLen:])

        if isResultPrefix:
            expression = function + "(" + str(arg1) + ")"
        else:
            expression = str(arg1) + function

        return expression

    def getExpressionFromPlanText(self, sentence):
        wordsList = sentence.split()

        if wordsList[0] == "dodaj":
            if "i" in wordsList:
                return self.buildBinaryExpression(wordsList, "i", "+", self.noInvert, self.prefix)

            if "do" in wordsList:
                return self.buildBinaryExpression(wordsList, "do", "+", self.invert, self.prefix)

        if wordsList[0] == "do":
            if "dodaj" in wordsList:
                return self.buildBinaryExpression(wordsList, "dodaj", "+", self.noInvert, self.prefix)

        if "plus" in wordsList:
            return self.buildBinaryExpression(wordsList, "plus", "+", self.noInvert, self.noPrefix)

        if wordsList[0] == "odejmij":
            if "od" in wordsList:
                return self.buildBinaryExpression(wordsList, "od", "-", self.invert, self.prefix)

        if wordsList[0] == "od":
            if "odejmij" in wordsList:
                return self.buildBinaryExpression(wordsList, "odejmij", "-", self.noInvert, self.prefix)

        if "odjac" in wordsList:
            return self.buildBinaryExpression(wordsList, "odjac", "-", self.noInvert, self.noPrefix)

        if wordsList[0] == "pomnoz":
            if "i" in wordsList:
                return self.buildBinaryExpression(wordsList, "i", "*", self.noInvert, self.prefix)

            if "przez" in wordsList:
                return self.buildBinaryExpression(wordsList, "przez", "*", self.noInvert, self.prefix)

        if "razy" in wordsList:
            return self.buildBinaryExpression(wordsList, "razy", "*", self.noInvert, self.noPrefix)

        if wordsList[0] == "podziel":
            if "i" in wordsList:
                return self.buildBinaryExpression(wordsList, "i", "/", self.noInvert, self.prefix)

            if "przez" in wordsList:
                return self.buildBinaryExpression(wordsList, "przez", "/", self.noInvert, self.prefix)

        if "dzielone" in wordsList:
            return self.buildBinaryExpression(wordsList, "dzielone przez", "/", self.noInvert, self.noPrefix)

        if "pierwiastek" in wordsList:
            return self.buildUnaryExpression(wordsList, "pierwiastek z", "sqrt", self.suffix, self.prefix)

        if "kwadrat" in wordsList:
            return self.buildUnaryExpression(wordsList, "kwadrat z", "^2", self.suffix, self.suffix)

        if "kwadratu" in wordsList:
            return self.buildUnaryExpression(wordsList, "do kwadratu", "^2", self.prefix, self.suffix)

        if "potegi" in wordsList:
            return self.buildBinaryExpression(wordsList, "do potegi", "^", self.noInvert, self.noPrefix)

        return "Not supported command."

    def convertTextToNumber(self, numberInTextList):
        current = result = 0

        for word in numberInTextList:
            if word not in self.wordNumberMap:
                raise Exception("Word not supported: " + word)

            scale, increment = self.wordNumberMap[word]
            current = current * scale + increment
            if scale > 100 or current > 1000:
                result += current
                current = 0

        result += current
        if numberInTextList[0] == "minus":
            result *= -1
        return result

    def createWordMap(self):
        wordNumberMap = {}
        jednosci = ["zero", "jeden", "dwa", "trzy", "cztery", "piec", "szesc", "siedem", "osiem",
                    "dziewiec", "dziesiec", "jedenascie", "dwanascie", "trzynascie", "czternascie", "pietnascie",
                    "szesnascie", "siedemnascie", "osiemnascie", "dziewietnascie"]

        dziesiatki = ["", "", "dwadziescia", "trzydziesci", "czterdziesci", "piecdziesiat",
                      "szescdziesiat", "siedemdziesiat", "osiemdziesiat", "dziewiecdziesiat"]

        setki = ["", "sto", "dwiescie", "trzysta", "czterysta", "piecset", "szescset",
                 "siedemset", "osiemset", "dziewiecset"]

        scale = ["", "tysiac", "milion", "miliard", "bilion", "biliard", "trylion"]

        casesPerPower = 2
        skaleCases = ["tysiace", "tysiacy",
                      "miliony", "milionow",
                      "miliardy", "miliardow",
                      "biliony", "bilionow",
                      "biliardy", "biliardow",
                      "tryliony", "trylionow"]

        for idx, word in enumerate(jednosci):   wordNumberMap[word] = (1, idx)
        for idx, word in enumerate(dziesiatki): wordNumberMap[word] = (1, idx * 10)
        for idx, word in enumerate(setki):      wordNumberMap[word] = (1, idx * 100)
        for idx, word in enumerate(scale):      wordNumberMap[word] = (1, 10 ** (idx * 3))

        power = 0
        for idx, word in enumerate(skaleCases):
            if idx % casesPerPower == 0:
                power += 3
            wordNumberMap[word] = (10 ** power, 0)

        wordNumberMap["i"] = (1, 0)
        wordNumberMap["minus"] = (1, 0)
        wordNumberMap["plus"] = (1, 0)

        return wordNumberMap
