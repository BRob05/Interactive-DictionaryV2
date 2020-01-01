import mysql.connector
from difflib import get_close_matches 

connect = mysql.connector.connect("""Connection String""")

def TypoStrings(term):
    item = connect.cursor()

    item.execute(f"select Expression from Dictionary where Expression LIKE '{term[0]}%'")
    allterms = item.fetchall()

    if term not in allterms:
        words = []              #adding only the words of the dictionary to a list to be compared in get_close_matches
        for iterator in range(len(allterms)):
            words.append(allterms[iterator][0])
        
        match = get_close_matches(term, words)
        if len(match) > 0:
            match = match[0]
            response = input(term + " is not a word in the dictionary.  Did you mean %s instead? (Y/N): " % match)

            if response == 'Y' or response == 'y' or response == 'Yes' or response == 'yes':
                item.execute("SELECT * FROM Dictionary WHERE Expression = '%s' " % match)
                results = item.fetchall()
                for definition in results:
                    print(definition[1])
                print(' ')
                return Menu()
            
            elif response == 'N' or response == 'n' or response == 'No' or response == 'no':
                print("The word you are looking for is not in the dictionary.  Please check your spelling and try again.")
                return UserPrompt()


def WordInDictionary(term):
    item = connect.cursor()

    item.execute("SELECT * FROM Dictionary WHERE Expression = '%s' " % term)
    results = item.fetchall()
    
    if results:
        for definition in results:
            print (definition[1])
        return Menu()
    else:
        return TypoStrings(term)


def UserPrompt():
    termprompt = input("Enter a term: ")
    return WordInDictionary(termprompt)

def Menu():
    print("Welcome to the Interactive Dictionary Version 2!  Choose from one of the following: ")
    print("1. Look up a term.")
    print("2. Exit application.\n")
    menuprompt = input("Choose an option: ")

    if menuprompt == '1':
        return UserPrompt()
    elif menuprompt == '2':
        return "Exiting application. Goodbye!"
    else:
        print("That is not a valid option.  Please choose either Option 1, or Option 2.\n")
        return Menu()

print(Menu())
