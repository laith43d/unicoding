
class Balance:
    def __init__(self, balances):
        balance1 = balances[0]
        balance2 = balances[1]

        if balance1['currency'] == 'USD':
            balanceUSD = balance1['sum']
            balanceIQD = balance2['sum']
        else:
            balanceIQD = balance1['sum']
            balanceUSD = balance2['sum']

        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD

    def __add__(self, other):
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]
    def __gt__(self, other):
        
        if self.balanceUSD > other.balanceUSD :
            StaUSD = True
        else:
            StaUSD = False
        if self.balanceIQD > other.balanceIQD :
            StaIQD = True
        else:
            StaIQD = False
        return {'USD':StaUSD},{'IQD':StaIQD}
            

    def __lt__(self,other):
        
        if self.balanceUSD < other.balanceUSD :
            StaUSD = True
        else:
            StaUSD = False
        if self.balanceIQD < other.balanceIQD :
            StaIQD = True
        else:
            StaIQD = False
        return {'USD':StaUSD},{'IQD':StaIQD}
        
    def is_zero(self):
        if self.balanceIQD == 0 and self.balanceUSD == 0 :
            return True
        else:
            return False
    #Here Is The Test <:
list1= [{
            'currency': 'USD',
            'sum': 200
        }, {
            'currency': 'IQD',
            'sum': 2000000
        }]
list2=[{'currency': 'USD',
            'sum': 400
        }, {
            'currency': 'IQD',
            'sum': 2000020
        }]
Obj1 = Balance(list1)
Obj2 = Balance(list2)

result = Obj1.__gt__(Obj2)
print(result)
result2 = Obj1.__lt__(Obj2)
print(result2)
result3 = Obj1.is_zero()
print(result3)
result4 = Obj2.is_zero()
print(result4)
