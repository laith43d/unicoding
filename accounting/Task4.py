#class balance

class Balance:

    def __init__(self, balances):
        balance1 = balances[0]
        balance2 = balances[1]
        balanceIQD = 0
        balanceUSD = 0

        if balance1['currency'] == 'USD':
            balanceUSD = balance1['sum']
            balanceIQD = balance2['sum']
        else:
            balanceUSD = balance2['sum']
            balanceIQD = balance1['sum']
       
        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

    def __add__(self, other):
        
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        result=[{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]

        return result

    #Grater than function
    def __gt__(self, other):
        if (isinstance(other, Balance)):
            IQD=  self.balanceIQD > other.balanceIQD
            USD = self.balanceUSD > other.balanceUSD
            return (IQD,USD)
    
    #less than function
    def __lt__(self, other):
        if (isinstance(other, Balance)):
            IQD=  self.balanceIQD < other.balanceIQD
            USD = self.balanceUSD < other.balanceUSD
            return (IQD,USD)

    #is zero?
    def iszero(self):
        if (isinstance(self,Balance)):
            return self.balanceIQD ==0 and self.balanceUSD==0

    

#test the sol:
balance1= [{'currency': 'USD', 'sum': 200}, {'currency': 'IQD','sum': 50000 }]
balance2= [{'currency': 'USD', 'sum': 100}, {'currency': 'IQD','sum': 100000 }]
balance3= [{'currency': 'USD', 'sum': 0}, {'currency': 'IQD','sum': 0 }]

balance1_object = Balance(balance1)
balance2_object = Balance(balance2)
balance3_object = Balance(balance3)

print(balance1_object > balance2_object) #output: (False, True)
print(balance1_object < balance2_object) #output: (True, False)
print(balance1_object.iszero())  #output: False
print(balance3_object.iszero())  #output: True

