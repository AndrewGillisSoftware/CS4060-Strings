#Andrew Gillis
#01-module
#1/28/2022

import time

# Brute Force Search
# Considered the typical first thought approach when someone thinks of string algorithms
# Worst Case: O(n^2)
def naive(needle, haystack):
    bundleOfNeedles = []

    #For Every Character in the Haystack
    for haystackIndex in range(len(haystack) - len(needle)):
        match = True
        #For Every Character in the needle
        for needleIndex in range(len(needle)):
            #Determine if there is a bad character
            if needle[needleIndex] != haystack[haystackIndex + needleIndex]:
                match = False
        #Determine if match is present
        if match:
            #Add index of match to indexs list
            bundleOfNeedles.append(haystackIndex)

    #return list of pattern indexs
    return bundleOfNeedles

# Uses a Sliding Window and Hash function to have a faster Average runtime
# m and n refer to the size of the needle and the size of the haystack
# Best/Average runtime: O(m+n)
# Worst Case: O(mn)
def robinKarp(needle, haystack):
    numOfSpuriousHits = 0
    bundleOfNeedles = []

    # Terrible Hash Function (Collision Chance is High ish) but Great for Demonstrating the Algorithm as it decouples understanding of Hashing Theory
    # The hash maps the word into the sum of it's unicode characters. Hash is a:97 b:98 etc ... Ex.) hash(ab) is 97 + 98 = 195.
    # You may ask why is this a terrible Hash Function for this application? Well any combination of letters the needle contains will result in hit!
    # Bad Hash Example.) hash(abcd) = hash(bcda) = hash(cdab) etc ... since every hit MUST be checked for pattern verification this will result in a bad run time

    # A Hash Function with a lower collision rate would be where the position of character affects the hash result. Many implementations of Robin Karp account for
    # this by taking the unicode value to the power of the letter position and summing it. Then by using modulus you can shrink the hash result space to prevent
    # the result from becoming unreasonably large. See this brilliant artical on Robin Karp for Details of such a Hashing Function : https://brilliant.org/wiki/rabin-karp-algorithm/
    def hash(word):
        hash = 0
        for charIndex in range(len(word)):
            hash += ord(word[charIndex])
        return hash

    #This Function Slides the window by replacing 1 character in the sum
    def rollHash(prevHash, oldChar, newChar):
        return prevHash - ord(oldChar) + ord(newChar)

    #Computes the Initial Hashes of the needle and a haystack segment the size of the needle
    needleHash = hash(needle)
    haystackHash = hash(haystack[0:len(needle)])

    #For Every Character in the haystack except for the last length of needle characters
    for haystackIndex in range(len(haystack) - len(needle)):
        #Verify character match is legit only when the hash values match
        if haystackHash == needleHash:
            match = True
            #Get the currently observed segment of the haystack
            haystackSegment = haystack[haystackIndex: len(needle) + haystackIndex]

            #Verify each character
            for index in range(len(needle)):
                if needle[index] != haystackSegment[index]:
                    match = False
                    numOfSpuriousHits += 1
                    break
            if match:
                #Match was found add needle to the index list
                bundleOfNeedles.append(haystackIndex)
        #Move Hash Window 1 character forward
        haystackHash = rollHash(haystackHash,haystack[haystackIndex], haystack[haystackIndex+len(needle)])

    #Print the Number of Spurious Hits that occurred
    print("Spurious Hits Occurred (Verifications that Did NOT Result in Match): " + str(numOfSpuriousHits))

    #return the list of indexs matching the pattern
    return bundleOfNeedles

# Z Box Algorithm Does a linear preprocessing step called get Z list
# A Z list entry contains a sort of closeness number which can be compared to the length of the needle
# if the closeness is the same as the length of the needle then their is a match present and add that
# index to the bundle of needles
# m and n refer to the size of the needle and the size of the haystack
# Worst Case: O(m+n)
def zBox(needle, haystack):
    bundleOfNeedles = []

    #Generate the Z List
    def getZList(needle, haystack):
        cHaystack = needle + ">" + haystack
        zList = [0] * len(cHaystack)

        leftBound = 0
        rightBound = 0
        for charIndex in range(1, len(cHaystack)):

            #Should the Z Box be expanded?
            if charIndex > rightBound:
                leftBound = charIndex
                rightBound = charIndex

                #Expanding Index. Box is Expanding!
                expIndex = rightBound - leftBound

                #While Not at the end of the combined haystack and their is not a bad character
                while cHaystack[expIndex] == cHaystack[rightBound] and rightBound < len(cHaystack):
                    rightBound += 1
                    expIndex = rightBound - leftBound

                #Set the Z to the Resulting Box Start
                zList[charIndex] = expIndex

                rightBound -=1
            else:

                # A Left and Right Interval Exists
                if zList[charIndex - leftBound] < rightBound - charIndex + 1:
                    # Set current index to start of Interval
                    zList[charIndex] = zList[charIndex - leftBound]
                else:
                    leftBound = charIndex

                    # Expanding Index. Box is Expanding!
                    expIndex = rightBound - leftBound

                    while cHaystack[rightBound] == cHaystack[expIndex] and rightBound < len(cHaystack):
                        rightBound += 1
                        expIndex = expIndex

                    rightBound -= 1
        return zList

    #END OF Z ARRAY FUNCTION

    #Get the Preprocessed Z List
    z = getZList(needle, haystack)

    #For Every Entry in Z List
    for zMagicNum in range(len(z)):
        #Match Found
        if len(needle) == z[zMagicNum]:
            #Add Index to the Bundle. Remove the needle length and the deliminator length to get the nonconcatinated index
            bundleOfNeedles.append(zMagicNum - 1 - len(needle))

    # return the list of indexs matching the pattern
    return bundleOfNeedles

#Turns a file contents into a single string
def getHaystackFromFile(filename):
    haystack = ""
    file = open(filename + ".txt", "r", encoding="utf-8")
    for line in file:
        line = line.strip()
        haystack += line
    file.close()
    return haystack

# WARNING THIS NEXT FUNCTION WAS BASED ON AN IDEA I SAW FROM CLASS I TAKE NO CREDIT FOR COMING UP WITH THE IDEA
# Prints out the context from the document (haystack) of a certain span of characters around the targeted pattern
# Ensure bundle of needles is the result of one of the above search algorithms shown above
def printContextsOfPattern(bundleOfNeedles, haystack, span):
    for needle in bundleOfNeedles:
        leftBound = 0
        rightBound = len(haystack) - 1
        if needle - span > 0:
            leftBound = needle - span
        if needle + span < len(haystack):
            rightBound = needle + span
        print(haystack[leftBound:rightBound])

# Used for observing changes in actual runtime for the algorithms
def percentChange(prev,cur):
    if cur == prev:
        return 100.0
    try:
        return ((cur - prev) / prev) * 100.0
    except ZeroDivisionError:
        return 0

def main():
    haystack = getHaystackFromFile("constitution")

    #Get Stats on the Different Algorithms
    algoNames =["\nNaive - Brute Force", "Robin Karp", "Z"]
    #Acts like Function Ptrs in C
    searchAlgoList = [naive, robinKarp, zBox]
    runtimeList = []

    needle = input("Enter the Pattern to Search the Constitution: ")
    needles = []

    #Run Some Tests on the Speed of the Algorithms
    for algorithmIndex in range(len(algoNames)):
        print(algoNames[algorithmIndex] + " Algorithm")
        #Get Timer Data
        timerStart = time.time()
        needles = searchAlgoList[algorithmIndex](needle,haystack)
        timerEnd = time.time()
        runtimeList.append(timerEnd-timerStart)
        print("Indices of Pattern Start: " + str(needles))
        print("Time in Seconds: " + str("{:.5f}".format(timerEnd - timerStart)) + "\n")

    #Display Interesting Timer Data Comparisions
    print("Robin Karp Algorithm is " + str("{:.2f}".format(percentChange(runtimeList[1], runtimeList[0])) + "% decrease in runtime when searching for the pattern \"" + needle + "\" than the Naive Algorithm!\n"))

    print("Z-Box Algorithm is " + str("{:.2f}".format(percentChange(runtimeList[2], runtimeList[0])) + "% decrease in runtime when searching for the pattern \"" + needle + "\" than the Naive Algorithm!\n"))

    print("Context of the Pattern in the Constitution:")

    #Print out the context of the pattern in the text
    printContextsOfPattern(needles, haystack, 50)

#Run Main
main()

