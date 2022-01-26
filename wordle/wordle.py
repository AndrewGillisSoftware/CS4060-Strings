#Preprocessing for Best First Guess
#tines is the best word for the first guess
#Most Common Letters
MCLetters = ['e','i','t','s','a','n','h','u','r','d','m','w','g','v','l','f','b','k','o','p','x','c','z','j','y','q']

#Determines if a word has double letters in it
def hasDoubleLetters(word):
    for i in range(len(word)):
        for x in range(len(word)):
            if i != x and word[i] == word[x]:
                return True

    return False

#Grades the word based on how common the letters within the word is. Note this works best when double have been removed
#Highest grade possible if doubles are not removed is eeeee which is 130
def gradeWordByCommonLetters(word):
    grade = 0
    for char in word:
        grade += 26 - MCLetters.index(char)
    return grade

#Sorts the List of Words by removing doubles and sorting by the grade function defined earlier
def getBestEarlyGuessList(words):
    wordsNoD = []
    for word in words:
        if not hasDoubleLetters(word):
            wordsNoD.append(word)

    wordsNoD.sort(key=gradeWordByCommonLetters, reverse=True)

    return wordsNoD
#End of Preprocessing of first guess

#Gets word list from text document
def getWordList(wordsFileName):
    words = []
    file = open(wordsFileName + ".txt", "r")
    for word in file:
        word = word.strip()
        words.append(word)
    file.close()
    return words

#Filters words to only be words with letters at correct locations
def filterCorrectSpot(guess, words, indexsWithCorrect):
    wordsToKeep = []

    for word in words:
        keep = True
        for index in indexsWithCorrect:
            #Does Letter Not Match with the Guess's correct letter indexs
            if word[index] != guess[index]:
                keep = False
                break
        if keep:
            wordsToKeep.append(word)

    return wordsToKeep

#Filter Out Words with Letters in the Wrong Spots but are in the word
def filterWrongSpot(guess, words, indexsWithWrongSpot):
    wordsToKeep = []
    wordsNotAtSpot = []

    #Keep Only Words with Letters Not at That Spot
    for word in words:
        keep = True
        for index in indexsWithWrongSpot:
            if word[index] == guess[index]:
                keep = False
                break
        if keep:
            wordsNotAtSpot.append(word)

    #Keep Only Words with Letters in that Word
    for word in wordsNotAtSpot:
        keep = True
        for index in indexsWithWrongSpot:
            if guess[index] not in word:
                keep = False
                break;
        if keep:
            wordsToKeep.append(word)

    return wordsToKeep

#Filters out words with letters not present
#Double characters in the word list act weird if this function does not account for them
#that is what the .count is for
def filterLettersNotPresent(guess, words, indexsNotPresent):
    wordsToKeep = []

    for word in words:
        keep = True
        for index in indexsNotPresent:
            if word.count(guess[index]) > 1:
                if word[index] == guess[index]:
                    keep = False
                    break
            else:
                if guess[index] in word and guess.count(guess[index]) == 1:
                    keep = False
                    break
        if keep:
            wordsToKeep.append(word)

    return wordsToKeep

# C - Correct Spot, W - Correct Letter Wrong Spot, N - Letter Not Present
#After Every Guess use this function to filter the master list
def filterWordList(guess, words, filterKey):
    indexsWithCorrect = []
    indexsWithWrongSpot = []
    indexsNotPresent = []

    #Generate the Lists of indexs for the different filters
    for i in range(len(filterKey)):
        if filterKey[i] == 'C':
            indexsWithCorrect.append(i)
        elif filterKey[i] == 'W':
            indexsWithWrongSpot.append(i)
        else:
            indexsNotPresent.append(i)

    #Run Through All The Filtering Systems
    words = filterLettersNotPresent(guess,words,indexsNotPresent)

    words = filterCorrectSpot(guess, words, indexsWithCorrect)

    words = filterWrongSpot(guess, words, indexsWithWrongSpot)

    print(str(len(words)) + " Possible Words Remain")
    print(words)
    return words

def main():
    #Pulls Word List from the Words File and Creates a List
    words = getWordList("words")

    #Best First Guess Note that list must Exist
    guess = getBestEarlyGuessList(words)[0]
    found = False
    print("First Guess: " + guess)
    print("Inputting Wordle's Response")
    print("C - Correct Letter and Position")
    print("W - Correct Letter Wrong Position")
    print("N - Letter Not Present")
    print("Example CCCCC is the Wordle Word of the Day and Will Exit the Program")
    #While the word has not been found
    while not found:
        #Get the Response from Wordle on how good the guess was
        filterKey = input("What was Wordle's Response: ")
        #If word was 100% correct exit program
        if filterKey == "CCCCC":
            found = True
        else:
            #Filter the List based on Response and Guess
            words = filterWordList(guess,words,filterKey)
            #If No Words remain in the master list exit the program
            if len(words) == 0:
                print("Word Could Not Be Found")
                break
            #Set the guess and prompt the user to enter the guess into wordle
            guess = words[0]
            print("Next Best Guess: " + guess)

#Run Main
main()