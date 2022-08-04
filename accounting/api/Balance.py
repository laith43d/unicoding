from decimal import Decimal


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

        if self.balanceUSD > other.balanceUSD and self.balanceIQD > other.balanceIQD:
            return [True,True]

        elif self.balanceUSD < other.balanceUSD and self.balanceIQD < other.balanceIQD:
            return [False,False]

        elif self.balanceUSD < other.balanceUSD and self.balanceIQD > other.balanceIQD:
            return [False, True]

        elif self.balanceUSD > other.balanceUSD and self.balanceIQD < other.balanceIQD:
                return [True, False]

    def isZero(self):
        if self.balanceUSD==0 and  self.balanceIQD==0:
            return True
        return False

    def total_balance(self):
            children = self.children.all()
            if len(children) == 0:
                return self.balance()
            total = []
            for child in list(children):
                c_balance = child.balance()
                totals_balance = Balance(c_balance)
                total.append(totals_balance)
            return sum(total)

"""o1=Balance([{'currency':"USD",'sum':1500000000},{'currency':"IQD",'sum':1500000000}])
o2=Balance([{'currency':"USD",'sum':15000000},{'currency':"IQD",'sum':15000000}])
print(o1 > o2)
print(o1.isZero())"""
