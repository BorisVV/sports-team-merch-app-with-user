

import time

class Validations(object):
    ' This class is to check the users inputs and validat data'

    # Format Date to make sure user enters the right format.
    def date_validation():
        ''' This validates the date that the user entered. '''
        while True:
            date = input('Enter the date (mm/dd/yyy):\n')
            try:
                # This formats the Date.
                valid_date = time.strptime(date, '%m/%d/%Y')
                if valid_date: # If Date is formatted correctly, loop breaks
                    break
            except:
                print('Invalid data!')
                continue
        return date


    # Validates numeric values.
    def int_validation(message):
        'This checks for int validation'
        while True:
            try:
                userInput = int(input(message)) # This uses a variable with a message.
            except ValueError:
                print("Not a number! Please enter again" )
                continue
            else:
                return userInput # If true it breaks.
                break


    def int_validation(message):
        'This checks and see if the input is a float'
        while True:
           try:
              userInput = int(input(message)) # This uses a variable to diaplay the message.
           except ValueError:
              print("Not a number! Please enter again" )
              continue
           else:
              return userInput # If true breaks and returns the input.
              break
