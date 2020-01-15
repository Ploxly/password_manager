import random
import shane_char 
import re

account_dict = {}
account_info_dict = {}

#<---- FIRST MAJOR FUNCTION ---->
# Creates an account
def account_create():

    print("-"*18, "\nAccount Creation!"), print("-"*18)

    while True:
        username = input("Enter a Username:\n")
        if len(username) < 5:
            print("Username has to be 5 characters or more.")
            continue
        else:
            account_info_dict["Username"] = username
            break

    if password_randomizer_query() == 'no':
        while True:
            password = input("Enter a Password:\n")
            if len(password) < 6:
                print("Password has to be 6 characters or more.")
                continue
            else:
                account_info_dict["Password"] = password
                break
    
    account_dict[username] = account_info_dict

    security_questions()

    account_save()

    return 

# Asks user to pick a question and saves the answer
def security_questions():
     sec_questions_dict = {
         "1":"What's your pet's name",
         "2":"What's your mother's middle name",
         "3":"What's your best friend's nickname",
         "4":"Which hospital were you born in"
      }

     print("-"*26)
     for key,val in sec_questions_dict.items():
         print(key,":",val)
     print("-"*26)

     security_choice = input("Please choose a security question (Type in corresponding number):\n")

     value = sec_questions_dict[security_choice]
     print(value)
     question_answer = input("")

     account_info_dict["Security Question"] = value
     account_info_dict["Security Answer"] = question_answer

     return value, question_answer

# Asks to generate a randomized password
def password_randomizer_query():
    accepted_answers = 'yes','no'

    while True:
        rand_answer = input("Do you want a randomized password? ('yes' or 'no'):\n")
        if rand_answer == 'yes':
            gen_pass = random_pass()
            account_info_dict["Password"] = gen_pass
            print("Your random pass is: " + gen_pass)
            break
        elif rand_answer == 'no':
            break
        elif rand_answer != accepted_answers:
            print("Incorrect use.")

    return rand_answer

# Generates a randomized password using letters and digits
def random_pass():
    string = shane_char.ascii_characters_and_num()
    letters_and_num = string.letters + string.digits
    rand_password = random.choice(string.lowercase)
    rand_password += random.choice(string.uppercase)
    rand_password += random.choice(string.digits)
    rand_password += random.choice(string.special_characters)

    for characters in range(6):
        rand_password += random.choice(letters_and_num)

    password_list = list(rand_password)
    random.SystemRandom().shuffle(password_list)
    rand_password = ''.join(password_list)

    return rand_password

# Saves and stores account
def account_save():

    account_file = open('account.txt','w')
    account_file.write(str(account_dict))
    account_file.close()

    return account_dict

#lists account dict
# def list_account():
#     account_file_read = open('account.txt','r')
#     print(account_file_read.read())
#     account_file_read.close()

# Recover exisiting account
def account_recovery():
    account_dict_file = open('account.txt','r')

    for line in account_dict_file:
        word = re.split('\{|: |, |\}', line)
        name = word[1]
        username = name.replace("'","")
        pass_w = word[6]
        password = pass_w.replace("'","")
        sec_ques = word[8]
        security_question = sec_ques.replace('"',"")
        sec_answ = word[10]
        security_answer = sec_answ.replace("'","")
    
    attempts = 4

    while True:
        print("Enter a username: ")
        user_answer = input("")

        if user_answer == username:
            while True:
                print(security_question)
                question_answer = input("")
                if question_answer == security_answer:
                    print("Your password is: "+password)
                    break
                elif attempts == 0:
                    print("You have exceeded max attempts.")
                    break
                else:
                    attempts -= 1
                    print("You have "+ str(attempts) +" attempt(s) left.")        
            break
        else:
            print("Username not found!")
            continue

    account_dict_file.close()

    return

#<---- SECOND MAJOR FUNCTION ---->
# Login to existing account
def login():
    account_dict_file = open('account.txt','r')

    attempts = 4
    for line in account_dict_file:
        word = re.split('\{|: |, |\}', line)
        name = word[1]
        username = name.replace("'","")
        pass_w = word[6]
        password = pass_w.replace("'","")

    while True:
        print("Enter your username: ")
        user_input_username = input("")

        if user_input_username == username:
            while True:
                print("Enter your password: ")
                user_input_password = input("")
                if user_input_password == password:
                    password_manager()
                    break
                elif attempts == 0:
                    print("You have exceeded max password attempts!")
                    break
                else:
                    attempts -= 1
                    print("Password not found!")
                    print("You have "+ str(attempts) +" attempt(s) left.")
            break

        else:
            print("Username not found!")
            continue

    account_dict_file.close()
    
    return
    
#<---- THIRD MAJOR FUNCTION ---->
# Manages and Rates your passwords.
def password_manager():

    if password_randomizer_query() == 'no':
        while True:
            password = input("Enter a Password:\n")
            # Fail Case 1
            if len(password) < 6:
                print("Password has to be 6 characters or more.")
                continue
            # Fail Case 2
            elif any(character.isdigit() for character in password) == False:
                print("Password has to include at least one digit/number.")
                continue
            # Fail Case 3
            elif bool(re.match("^[a-zA-Z0-9_]*$", password)) == True:
                print("Password has to include at least one special character")
                continue
            else:
                account_info_dict["Password"] = password
                password_rating(password)
                print("Would you like to save your password? (Type 'yes' or 'no'): ")
                save_query = input("")
                if save_query == 'yes':
                    password_save()
                    print("Password Saved.")
                    break
                elif 'no':
                    continue
                else:
                    break
    else:
        while True:
            print("Would you like to save your password?(Type 'yes' or 'no'): ")
            save_query = input("")
            if save_query == 'yes':
                password_save()
                print("Password Saved.")
                break
            elif 'no':
                password_randomizer_query()
                continue
            else:
                break


# Saves your passwords
def password_save():

    account_file = open('password.txt','w')
    account_file.write(str(account_info_dict))
    account_file.close()

    return account_info_dict

# Gives the password a rating
def password_rating(string):
    import collections
    repeat_dict = collections.defaultdict(int)

    for characters in string:
        repeat_dict[characters] += 1

    for characters in sorted(repeat_dict, key=repeat_dict.get, reverse=True):
        if repeat_dict[characters] > len(string)//2:
            print("*WARNING* This password is Bad!")
            break
        elif repeat_dict[characters] == 1:
            print("This password is Safe!")
            break
        else:
            print("This password is Okay.")
            break

# Lists the password
def list_password():
    account_file = open('password.txt','r')
    print(str(account_file.read()))
    account_file.close()

# Main Function
def main():

    print("-"*29, "\nWelcome to Password Manager!"), print("-"*29)
    print('*IMPORTANT* Type "recovery" if you want to recover your password!')
    answer = input("Do want to create an account? Type 'yes' or 'no': ")

    if answer == 'yes':
        account_create()
    elif answer == 'no':
        login()
    elif answer == 'recovery':
        account_recovery()
    elif answer == 'read':
        list_password()
    else:
        print("Incorrect use.")
        
main()
