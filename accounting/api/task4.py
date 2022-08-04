from decimal import Decimal


class Balance:
    def __init__(self, balances):
        if len(balances) == 2 :
            balance1 = balances[0]
            balance2 = balances[1]

            if balance1['currency'] == 'USD':
                balanceUSD = balance1['sum']
                balanceIQD = balance2['sum']
            else:
                balanceIQD = balance1['sum']
                balanceUSD = balance2['sum']
        elif len(balances) == 1:
            balance1 = balances[0]
            if balance1['currency'] == 'USD':
                balanceUSD = balance1['sum']
                balanceIQD = 0
            else:
                balanceIQD = balance1['sum']
                balanceUSD = 0
        else:
            balanceUSD = 0
            balanceIQD = 0
        self.balanceUSD = balanceUSD
        self.balanceIQD = balanceIQD  
    def __add__(self, other):
        self.balanceIQD += other.balanceIQD
        self.balanceUSD += other.balanceUSD
        return [{
            'currency': 'IQD',
            'sum': self.balanceIQD
        }, {
            'currency': 'USD',
            'sum': self.balanceUSD
        }]
    def __lt__(self, other):
        if self.balanceIQD < other.balanceIQD :print(True)
        else:print(False)
        if self.balanceUSD < other.balanceUSD :print(True)
        else:print(False)
    def __gt__(self, other):
        if self.balanceIQD > other.balanceIQD :print(True)
        else:print(False)
        if self.balanceUSD > other.balanceUSD :print(True)
        else:print(False)
    def is_zero(self):
        if self.balanceIQD == 0 and self.balanceUSD == 0:print(True)
        else:print(False)
m = [{'currency': 'IQD', 'sum': Decimal(0)},{'currency': 'USD', 'sum': Decimal(20)}]
z = [{'currency': 'IQD', 'sum': Decimal(10)},{'currency': 'USD', 'sum': Decimal(0)}]
Balance(m).is_zero()
print('________________')
Balance(m) > Balance(z)
print('________________')
Balance(m) < Balance(z)
