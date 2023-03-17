def askInput(*inputcontrol):
    #inputcontrol[0]=string containing input type "int" or "str"
    #inputcontrol[1]=input message displayed to the user
    #inputcontrol[2]=list of input possible values (optional)
     
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

def main():

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

if __name__ == "__main__": 
    main()