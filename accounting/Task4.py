#class balance
from unittest import result


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
    def __Gthan__ (self, other):
        IQD = True
        USD = True
        if self.balanceIQD > other.balanceIQD:
            IQD = True
        else:
            IQD = False
        if self.balanceUSD > other.balanceUSD:
            USD = True
        else:
            USD = False
        return {'IQD': IQD, 'USD': USD}
    
    #Smaller than function
    def __Sthan__ (self, other):
        IQD = True
        USD = True
        if self.balanceIQD < other.balanceIQD:
            IQD = True
        else:
            IQD = False
        if self.balanceUSD < other.balanceUSD:
            USD = True
        else:
            USD = False
        return {'IQD': IQD, 'USD': USD}

    #is zero?
    def __iszero__(self):
        IQD = True
        USD = True
        if self.balanceIQD == 0 and self.balanceUSD==0:
            return True
        else:
            return False

#test the sol:
balance1= [{'currency': 'USD', 'sum': 200}, {'currency': 'IQD','sum': 50000 }]
balance2= [{'currency': 'USD', 'sum': 100}, {'currency': 'IQD','sum': 100000 }]
balance3= [{'currency': 'USD', 'sum': 0}, {'currency': 'IQD','sum': 0 }]

balance1_object = Balance(balance1)
balance2_object = Balance(balance2)
balance3_object = Balance(balance3)


result = balance1_object.__Gthan__(balance2_object)
print(result) #output: {'IQD': False, 'USD': True}

result = balance1_object.__Sthan__(balance2_object)
print(result) #output: {'IQD': True, 'USD': False}

print(balance1_object.__iszero__()) #output: False
print(balance2_object.__iszero__()) #output: False
print(balance3_object.__iszero__()) #output: True
