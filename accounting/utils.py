class Balance:
    def __init__(self, balances):
        balance_iqd = 0
        balance_usd = 0
        for balance in balances:
            if balance['currency'] == 'USD':
                balance_usd = balance['sum']
            if balance['currency'] == 'IQD':
                balance_iqd = balance['sum']

        self.balanceUSD = balance_usd
        self.balanceIQD = balance_iqd

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

    def __gt__(self, other):
        return self.balanceUSD > other.balanceUSD, self.balanceIQD > other.balanceIQD

    def __lt__(self, other):
        return self.balanceUSD < other.balanceUSD, self.balanceIQD < other.balanceIQD

    def is_zero(self):
        return self.balanceUSD == 0 and self.balanceIQD == 0


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
