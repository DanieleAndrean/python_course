def askInput(*inputcontrol):
######################################################à
# INPUTS: inputcontrol (list)   
#              inputcontrol[0] string containing expected input type 
#                   Possible values: "int" or "str"
#
#              inputcontrol[1] string containing input message displayed to the user
#
#              inputcontrol[2] list of input possible values (optional)

# OUTPUTS: userIn (matches inputcontrol[0]= expected input type) 

# RAISED EXCEPTIONS:
#       -TypeError: the type of data inserted by does not match the expected input type
#       -SyntaxError: the expected input specified in the function call is wrong
#       -Exception: the user input value is not among the possible input values

    typ=inputcontrol[0]
    message=inputcontrol[1]
    
    userIn=input(message)
    #cheking input type
    match typ:
        case "int":
            try:
                userIn=int(userIn)
            except: 
                raise TypeError("Incorrect input type, expected: "+typ)

        case "str":
            try:
                userIn=int(userIn)
            except: 
                pass
            else:
                raise TypeError("Incorrect input type, expected: "+typ)


        case _:
            raise SyntaxError("Error recognizing input type: "+typ)

    #checking input values if restrictions are present
    if len(inputcontrol)==3:
        values=inputcontrol[2]
        if userIn not in values:
             raise Exception("Incorrect input value")
    
    return userIn

#main function to test askInput() with examples on how to handle errors
def main():

# examples of askInput call with exception handling

#error messages can be customized according to the needs

    okInput=False #loop conditional variable
    while(not okInput): #exit loop when input is correct

        try:
            usrIn=askInput("str","give me a string: \n")
        except TypeError: #the user inserted the wrong input type
            print("Incorrect input type, retry \n") 
        except SyntaxError: #we specified the wrong expected input type
            print("Error specifying the required input type, make sure it corresponds to \"int\" or \"str\" \n")
            break #exit cycle as the error is in the code
        except Exception: #user inserted the wrong values
            print("Incorrect value inserted, retry \n")
        else: # everything is ok
            okInput=True #loop exit condition

#example with int expected type
    okInput=False
    while(not okInput):

        try:
            usrIn=askInput("int","give me a number: \n")
        except TypeError:
            print("Incorrect input type, retry \n")
        except SyntaxError:
            print("Error specifying the required input type, make sure it corresponds to \"int\" or \"str\" \n")
        except Exception:
            print("Incorrect value inserted, retry \n")
        else:
            okInput=True

#example with only a list of possible numerical values
    okInput=False
    while(not okInput):

        try:
            usrIn=askInput("int","choose 1 2 or 3: \n",[1,2,3])
        except TypeError:
            print("Incorrect input type, retry \n")
        except SyntaxError:
            print("Error specifying the required input type, make sure it corresponds to \"int\" or \"str\" \n")
        except Exception:
            print("Incorrect value inserted, retry \n")
        else:
            okInput=True

#example with only a list of possible string values
    okInput=False
    while(not okInput):

        try:
            usrIn=askInput("str","choose \"a\" \"two\"  or 3: \n",["a","two","3"])
        except TypeError:
            print("Incorrect input type, retry \n")
        except SyntaxError:
            print("Error specifying the required input type, make sure it corresponds to \"int\" or \"str\" \n")
        except Exception:
            print("Incorrect value inserted, retry \n")
        else:
            okInput=True

if __name__ == "__main__": 
    main()