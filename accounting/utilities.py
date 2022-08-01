class Balance:
    def __init__(self, balances):
        balanceUSD, balanceIQD = 0, 0

        for bal in balances:
            if bal['currency'] == 'USD':
                balanceUSD = bal['sum']
            else:
                balanceIQD = bal['sum']

        self.balanceUSD, self.balanceIQD = balanceUSD, balanceIQD

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

    def __radd__(self, other):
        return self if other == 0 else self.__add__(other)