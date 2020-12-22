import re, json, os

suppressErrors = True #Suppresses console output of failure of converting a statistic into a float.

# Takes EU4 Unique Country ideas code (File name is 00_country_ideas.txt in the eu4 game files) and converts it into a JSON format for a non-SQL database
#NOTE: Put the 00_country_ideas.txt file in the same directory and coverter.py.


# countryID is the abbreviation of the country found in the file, organizes the data to split the data in terms of traditions and ideas and groups bonuses when unlocked*.
# *This means that if a country idea or tradition unlocks 2+ bonuses, they are accordingly grouped together.

#Also adds technology group by accessing the countries file inside of the history folder [VERY JANK].

#The countryMods function is still a WIP.

def generateJSON(countryID):
    start = 0
    end = 0
    ideas = []
    traditions = []

    countryObj = {
        "countryName": "",
        "countryTag": countryID,
        "traditions": [],
        "ideas": [],
        "tech_group": "",
        "imagePath": "/images/flags/" + countryID
    }

    regex = re.compile(r"(\w+) = (-?\d+(?:\.\d+)?)")

    countryFile = ""
    #Finds the name of the country in the most jank way possible :P
    for fileName in os.listdir("countries/"):
        if fileName[0:3] == countryID:
            countryFile = fileName
            countryObj["countryName"] = fileName[fileName.index("-") + 1:fileName.index(".")].strip()

    with open("00_country_ideas.txt", "r") as f:
        for line in f:
            if countryID.upper() in line:
                break
            start += 1

        end = start

        temp = list()

        for line in f:
            if regex.search(line) is not None:
                s = line.rstrip()
                temp.append(s[0:s.index('=')].strip())
                temp.append(s[s.index('=') + 1:].strip())

            elif len(temp) > 0:
                ideas.append(temp)
                temp = list()

            if not re.match(r'\t', line) and re.match(r'}', line):
                break
            end += 1
    f.close()

    with open("00_country_ideas.txt", "r") as f:
        for line in f:
            if countryID.upper() in line:
                break
            start += 1

        end = start

        temp = list()
        for line in f:
            if regex.search(line) is not None:
                s = line.rstrip()
                temp.append(s[0:s.index('=')].strip())
                temp.append(s[s.index('=') + 1:].strip())

            elif len(temp) > 0:
                traditions.append(temp)
                temp = list()

            if re.match('\t*free = \w', line):
                break
            end += 1
    f.close()

    ideas = ideas[len(traditions):len(ideas)]

    with open("countries/" + countryFile, "r") as f:
        for line in f:
            if re.match("technology_group*\w", line):
                s = line.rstrip()
                countryObj["tech_group"] = s[s.index("=") + 1:].strip()
                break



    #Converts strings into floats.
    for i in range(len(traditions)):
        for j in range(len(traditions[i])):
            try:
                traditions[i][j] = float(traditions[i][j])
            except ValueError:
                if not suppressErrors:
                    print("Unable to convert string " + traditions[i][j] + " to Float")

    for i in range(len(ideas)):
        for j in range(len(ideas[i])):
            try:
                ideas[i][j] = float(ideas[i][j])
            except ValueError:
                if not suppressErrors:
                    print("Unable to convert string " + ideas[i][j] + " to Float")

    countryObj["traditions"] = traditions
    countryObj["ideas"] = ideas
    return countryObj

#gets the list of countries.
def getListOfCountries():
    countryNames = ""
    for fileName in os.listdir("countries/"):
            countryFile = fileName
            countryNames += "/images/flags/" + fileName[0:fileName.index("-")].strip() + ".png" + " - " + fileName[fileName.index("-") + 1:fileName.index(".")].strip() + ","
    with open("countryNames.txt", "w") as outfile:
        outfile.write(countryNames)
        outfile.close()

#gets the country IDs
def getIds():
    countryIDs = ""
    for fileName in os.listdir("countries/"):
        countryFile = fileName
        countryIDs += "\"" + fileName[0:fileName.index("-")].strip() + "\","
    with open("countryIDs.txt", "w") as outfile:
        outfile.write(countryIDs)
        outfile.close()


#gets the modifiers list
def getModifierList():
    countryMods = ""
    modRegex = re.compile(r"(>)\w+")
    with open("eu4CountryModifiersList.txt", "r") as f:
        for line in f:
            print(line)
            if re.match(r"(>)\w+", line):
                s = line.rstrip()

                countryMods += "\"" + (s[5:s.index('=')].strip()) + "\","
        with open("countryMods.txt", "w") as outfile:
            outfile.write(countryMods)
            outfile.close()


getModifierList()
# getIds()

# countries = ["ENG", "GER", "POL", "GBR", "SWE", "MOS", "RUS", "RUS", "SPA", "CAS", "NED"]
#
# for i in range(len(countries)):
#    countryFile = generateJSON(countries[i])
#
#    with open(countries[i] + ".txt", 'w') as outfile:
#        json.dump(countryFile, outfile)