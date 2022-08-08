
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

    def is_zero(self):
        if self.balanceIQD == 0 and self.balanceUSD == 0 :
            return True
        else:
            return False    
    #Here Is The Test <: 

list1=[{
        'currency': 'USD',
        'sum': 500
    }, {
        'currency': 'IQD',
        'sum': 0
    }]
list2=[{
    'currency': 'USD',
    'sum': 400
        },{
        'currency': 'IQD',
        'sum': 2000020
    }]
Obj1 = Balance(list1)
Obj2 = Balance(list2)

print('Obj1 > Obj2 =>',Obj1 > Obj2) #OUTPUT:Obj1 > Obj2 => ({'USD': True}, {'IQD': False})
print('Obj2 > Obj1 =>',Obj2 > Obj1) #OUTPUT:Obj2 > Obj1 => ({'USD': False}, {'IQD': True})

print('Obj1 < Obj2 =>',Obj1 < Obj2) #OUTPUT:Obj1 < Obj2 => ({'USD': False}, {'IQD': True})
print('Obj2 < Obj1 =>',Obj2 < Obj1) #OUTPUT:Obj2 < Obj1 => ({'USD': True}, {'IQD': False})

print('Obj1 ==0 =>',Obj1.is_zero()) #OUTPUT:Obj1 ==0 => False
print('Obj2 ==0 =>',Obj2.is_zero()) #OUTPUT:Obj2 ==0 => False
            
''''''''''
    #Another Sol For Task4,From Internet 
    def __gt__(self, other):
        if (isinstance(other,Balance)):
            StaUSD = self.balanceUSD > other.balanceIQD
            StaIQD = self.balanceIQD > other.balanceUSD
            return {'USD':StaUSD},{'IQD':StaIQD}
     
    
        
    def __lt__(self, other):
        if (isinstance(other,Balance)):
            StaUSD = self.balanceUSD < other.balanceIQD
            StaIQD = self.balanceIQD < other.balanceUSD
            return {'USD':StaUSD},{'IQD':StaIQD}
    
    def is_zero(self):
        return self.balanceIQD == 0 and self.balanceUSD == 0 
    
   '''''''''
