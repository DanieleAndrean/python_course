import copy
class Item:
    def __init__(self,itDict,quantity):
        self.name=itDict["name"]
        self.quantity=quantity
        self.maxNum=itDict["maxNum"]
    
    def __str__(self):

        itstr="Item:\t"+self.name+"\tQuantity:\t"+str(self.quantity)
        return itstr
    #increases the Item quantity by the specified number
    def restore(self,*numOb):
        #if numOb is not empty
        if numOb:
            self.quantity+=numOb[0]
            if self.quantity>self.maxNum:
                self.quantity=self.maxNum
        else:
            self.quantity=self.maxNum
            
    
    #decreases the Item quantity by the specified number
    def decIt(self,numOb):

        self.quantity-=numOb
    
    #returns the Item's quantity
    def getNumIt(self):

        return copy.deepcopy(self.quantity)
    