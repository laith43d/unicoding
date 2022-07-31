class Balance:
    def __init__(self, balances):
        balanceIQD = 0
        balanceUSD = 0
        for i in balances:
            if i['currency'] == 'USD':
                balanceUSD = i['sum']
            if i['currency'] == 'IQD':
                balanceIQD = i['sum']

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

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)


def zero_balances():
    return [
        {
            "currency": "USD",
            "sum": "0.0"
        },
        {
            "currency": "IQD",
            "sum": "0.0"
        }
    ]
