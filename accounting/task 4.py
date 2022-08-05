from decimal import Decimal


class Balance:

    def __init__(self, balances):

        try:
            balance1 = balances[0]
        except IndexError:
            balance1 = {'currency': 'USD', 'sum': 0}
        try:
            balance2 = balances[1]
        except IndexError:
            if balance1['currency'] == 'USD':
                balance2 = {'currency': 'IQD', 'sum': Decimal(0)}
            else:
                balance2 = {'currency': 'USD', 'sum': Decimal(0)}

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
    def __lt__(self, other):
        if self.balanceIQD <other.balanceIQD:
            IQDS=True
        else:
            IQDS=False
        if self.balanceUSD <other.balanceUSD:
            USDS=True
        else:
            USDS=False
        return [USDS,IQDS]
    def iszero(self):
        IQDSS = False
        USDSS = False
        if self.balanceIQD==0:
            IQDSS = True
        if self.balanceUSD==0:
            USDSS=True
        return [USDSS,IQDSS]

a=Balance([{
            'currency': 'USD',
            'sum': 1000
        }, {
            'currency': 'IQD',
            'sum': 1000
        }])
b=Balance([{
            'currency': 'USD',
            'sum': 1
        }, {
            'currency': 'IQD',
            'sum': 0
        }])
#we miss laith and ali
#laith and ali > rest of the trainers