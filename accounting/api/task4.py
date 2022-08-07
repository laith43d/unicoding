
class Balance:

    def __init__(self, balances):
        balance1 = balances[0]
        balance2 = balances[1]

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
#Old
    def __Othan__ (self, other):
        if self.balanceIQD > other.balanceIQD:
            theIQD = True
        else:
            theIQD = False
        if self.balanceUSD > other.balanceUSD:
            theUSD = True
        else:
            theUSD = False
        return {'BalanceIQD': theIQD, 'BalanceUSD': theUSD}

    #Younger
    def __Ythan__ (self, other):
        if self.balanceIQD < other.balanceIQD:
            theIQD = True
        else:
            theIQD = False
        if self.balanceUSD < other.balanceUSD:
            theUSD = True
        else:
            theUSD = False
        return {'BalanceIQD': theIQD, 'BalanceUSD': theUSD}

    # zero
    def __isZero__(self):
        if self.balanceIQD == 0 and self.balanceUSD==0:
            return True
        else:
            return False
