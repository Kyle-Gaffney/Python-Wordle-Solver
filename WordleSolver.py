with open('WordleDict.txt', 'r') as file:
    word_list=[word for line in file for word in line.split()]

import string
alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)

#Collect all 5 letter non-proper noun words from the dictionary
fiveletterwords = [x for x in word_list if len(x)==5 and x[0] not in alphabet_list]

#collect lists of each letter in each position
l_1 = [x[0] for x in fiveletterwords]
l_2 = [x[1] for x in fiveletterwords]
l_3 = [x[2] for x in fiveletterwords]
l_4 = [x[3] for x in fiveletterwords]
l_5 = [x[4] for x in fiveletterwords]
all_letters = l_1+l_2+l_3+l_4+l_5

import collections

#count up the number of occurences of each letter in each list
c_1=collections.Counter(l_1)
c_2=collections.Counter(l_2)
c_3=collections.Counter(l_3)
c_4=collections.Counter(l_4)
c_5=collections.Counter(l_5)
alc=collections.Counter(all_letters)

#set limit of the number of guesses allowed
maxguessnumber=6

#Define Wordle Guess Input Function
def input_guess():
    while True:
        guess = input("Enter 5-letter word guess: ")
        if len(guess) == 5 and guess.lower() in fiveletterwords:
            break
    return guess.lower()

#Define Wordle Response Input Function
def input_response():
    print("Type the color-coded reply from Wordle:")
    print(" G for Green, Y for Yellow, and X for gray (ex:GGYGX)")
    while True:
        response = input("Color Response from Wordle: ")
        if len(response) == 5 and set(response) <= {"G", "Y", "X"}:
            break
        else:
            print(f"Error - invalid answer {response}")
    return response

for k in range(maxguessnumber):
    guess_score=[]
    #for first 2 guesses punish repeated letters and use total letter count
    if k<2:
        for i in fiveletterwords:
            guess_score.append((alc[i[0]]+alc[i[1]]+alc[i[2]]+alc[i[3]]+alc[i[4]])*len(set(i))/5)
    #for remaining guesses dont penalize repeated letters and use positional letter count
    else:
        for i in fiveletterwords:
            guess_score.append((c_1[i[0]]+c_2[i[1]]+c_3[i[2]]+c_4[i[3]]+c_5[i[4]]))
    #sort the wordscores to display the best first guess
    wordtuple = list(zip(fiveletterwords , guess_score ))
    sortedwordtuple = sorted(wordtuple, key=lambda pair: pair[1], reverse=True)
    #Display top 5 guesses
    print(sortedwordtuple[:5])
    #User inputs guess, and Wordle response
    guess=input_guess()
    responses=input_response()
    if responses=='GGGGG':
        print(f'Congrats you solved the Wordle in {k+1} guesses: the Wordle word was {guess}')
        break
    # check for repeated letters
    guessletters = [char for char in guess]
    repeats = [x for x, count in collections.Counter(guess).items() if count > 1]
    repeatsindex=[]
    for rl in repeats:
        repeatsindex.append([i for i, j in enumerate(guessletters) if j==rl])
    repeatsresponses=[]
    for j in repeatsindex:
        repeatsresponses.append([responses[i] for i in j])
    repeatresponsedict=dict(zip(repeats , repeatsresponses))
    #Trim solution list using Wordle response information corrected with repeated letters:
    for i in range(5):
        if guess[i] in repeats:
            #all repeated letters are gray
            if (repeatresponsedict.get(guess[i]).count('G')+repeatresponsedict.get(guess[i]).count('Y'))==0:
                fiveletterwords = [x for x in fiveletterwords if guess[i] not in x]
            #the current letter is gray and there is exactly 1 non-gray repeated letter
            elif responses[i]=='X' and (repeatresponsedict.get(guess[i]).count('G')+repeatresponsedict.get(guess[i]).count('Y'))==1:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i])==1) and x[i] != guess[i]]
            #the current letter is gray and there are exactly 2 non-gray repeated letters
            elif responses[i]=='X' and (repeatresponsedict.get(guess[i]).count('G')+repeatresponsedict.get(guess[i]).count('Y'))==2:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 2) and x[i] != guess[i]]
            #the current letter is yellow and there are no other repeated letters in the word
            elif responses[i] == 'Y' and (repeatresponsedict.get(guess[i]).count('G') + repeatresponsedict.get(guess[i]).count('Y')) == 1:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 1) and x[i] != guess[i]]
            #the current letter is yellow and there is exactly 1 other repeated letter in the word
            elif responses[i]=='Y' and (repeatresponsedict.get(guess[i]).count('G')+repeatresponsedict.get(guess[i]).count('Y'))==2:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 2) and x[i] != guess[i]]
            #the current letter is yellow and there are exactly 2 other repeated letters in the word
            elif responses[i]=='Y' and (repeatresponsedict.get(guess[i]).count('G')+repeatresponsedict.get(guess[i]).count('Y'))==3:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 3) and x[i] != guess[i]]
            #the current letter is green and are no other repeated letters in the word
            elif responses[i] == 'G' and (repeatresponsedict.get(guess[i]).count('G') + repeatresponsedict.get(guess[i]).count('Y')) == 1:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 1) and x[i] == guess[i]]
            #the current letter is green and there is exactly 1 other repeated letter in the word
            elif responses[i] == 'G' and (repeatresponsedict.get(guess[i]).count('G') + repeatresponsedict.get(guess[i]).count('Y')) == 2:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 2) and x[i] == guess[i]]
            #the current letter is green and there are exactly 2 other repeated letter in the word
            elif responses[i] == 'G' and (repeatresponsedict.get(guess[i]).count('G') + repeatresponsedict.get(guess[i]).count('Y')) == 3:
                fiveletterwords = [x for x in fiveletterwords if (x.count(guess[i]) == 3) and x[i] == guess[i]]
        # old rules for non-repeated letter guesses
        elif responses[i] == 'X':
            fiveletterwords = [x for x in fiveletterwords if guess[i] not in x ]
        elif responses[i] == 'G':
            fiveletterwords = [x for x in fiveletterwords if guess[i] == x[i] ]
        elif responses[i] == 'Y':
            fiveletterwords = [x for x in fiveletterwords if ( guess[i] in x and guess[i] != x[i] )]