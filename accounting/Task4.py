class Balance:
    def __init__(self, balances):
        balanceUSD = 0
        balanceIQD = 0
        if balances:
            balance1 = balances[0] 
            #-----------One currency----------- 
            if len(balances) == 1:
                if balance1['currency'] == 'USD':
                    balanceUSD =  balance1['sum']
                else:
                    balanceIQD =  balance1['sum']   

            #-----------Two currencies---------
            elif len(balances) == 2:
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
        result = [False] * 2
        if self.balanceUSD > other.balanceUSD : result[0] = True 
        if self.balanceIQD > other.balanceIQD : result[1] = True 
        return tuple(result)

    def is_zero(self):
        return (self.balanceUSD == 0) and (self.balanceIQD == 0)

balance1 = Balance([
                   {'currency':'USD','sum':100},
                   {'currency':'IQD','sum':200}
                  ])

balance2 = Balance([
                    {'currency':'USD','sum':500},
                    {'currency':'IQD','sum':100}
                  ]) 


print("{:25}{}".format("balance1 > balance2 => ", balance1 > balance2))
print("{:25}{}".format("balance1 < balance2 => ", balance1 < balance2))
print("{:20}{:5}{}".format("balance1 == 0","=>", balance1.is_zero()))
print("{:25}{}".format("balance1 + balance2 => ", balance1 + balance2))

