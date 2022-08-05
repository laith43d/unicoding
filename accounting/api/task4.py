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


#Task-4
    def check1(self , other):
        if self.balanceUSD > other.balanceUSD:
            result_OF_USD = True
        else:
            result_OF_USD = False

        if self.balanceIQD > other.balanceIQD:
            result_OF_IQD = True
        else:
            result_OF_IQD = False

        return {result_OF_USD , result_OF_IQD}

    def check2(self , other):
        if self.balanceUSD < other.balanceUSD:
            result_OF_USD = True
        else:
            result_OF_USD = False

        if self.balanceIQD < other.balanceIQD:
            result_OF_IQD = True
        else:
            result_OF_IQD = False

        return {result_OF_USD , result_OF_IQD}

    def is_the_sklolo_zero(self):
        if self.balanceIQD  == 0 and self.balanceUSD == 0:
            return True
        else:
            return False
