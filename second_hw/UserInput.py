import os
def askInput(*inputcontrol):
######################################################à
# INPUTS: inputcontrol (list)   
#              inputcontrol[0] string containing expected input type 
#                   Possible values: "int", "str" or ""
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

        case "":
            userIn=None

        case _:
            raise SyntaxError("Error recognizing input type: "+typ)

    #checking input values if restrictions are present
    if len(inputcontrol)==3:
        values=inputcontrol[2]
        if userIn not in values and len(values)>0 :
             raise Exception("Incorrect input value")
    
    return userIn

def inputLoop(*inputcontrol):
#####################################################################
#INPUTS: inputcontrol   (list) 
#   inputcontrol[0]=string containing input type "int", "str" or ""

#   inputcontrol[1]=input message displayed to the user

#   inputcontrol[2]=list of strings containing custom error messages
        #first error message: Error on wrong input type
        #second error message: Error on input value (if the user can only select between specified values)

    #inputcontrol[3]=list of input possible values (optional)
#######################################################################    
    typ=inputcontrol[0]
    msg=inputcontrol[1]
    errmsg=inputcontrol[2] 
    vals=[]
    if len(inputcontrol)==4:
        vals=inputcontrol[3]
        
    
    #User is asked to provide the correct input untill it succeeds
    okInput=False
    while(not okInput):
        os.system("cls")
        try:
            userIn=askInput(typ,msg,vals)
        except TypeError:
            askInput("",errmsg[0]+"\nPress Enter to retry:")
        except SyntaxError: # Coding error, wrong expected type specifiec
            raise Exception("Error specifying the required input type, make sure it corresponds to \"int\", \"str\" or "" \n")
        except Exception:
            askInput("",errmsg[1]+"\nPress Enter to retry:")
        else:
            okInput=True
    
    return userIn



def main():
#######################################################
# Main with usage examples, not needed when importing
#########################################################
    okInput=False
    while(not okInput):

        try:
            usrIn=askInput("str","give me a string: \n")
        except TypeError:
            print("Incorrect input type, retry \n")
        except SyntaxError:
            print("Error specifying the required input type, make sure it corresponds to \"int\" or \"str\" \n")
        except Exception:
            print("Incorrect value inserted, retry \n")
        else:
            okInput=True

    errms=["You must provide a number",""]
    usrIn=inputLoop("int","Give me a number: \n",errms)
    print(str(usrIn))

    errms=["You must provide a number","You can only choose among the specified values"]
    usrIn=inputLoop("int","choose 1 2 or 3: \n",errms,[1,2,3])
    print(str(usrIn))

    #type "" can be useful to ask the user to press Enter 
    askInput("","Press Enter to continue:")

if __name__ == "__main__": 
    main()