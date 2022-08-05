
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

    def __gt__(self, other):

        print(self.balanceUSD > other.balanceUSD)
        print(self.balanceIQD > other.balanceIQD)

    def __ls__(self, other):

        print(self.balanceUSD < other.balanceUSD)
        print(self.balanceIQD < other.balanceIQD)

    def is_zero(self):

        if(self.balanceUSD == 0 and self.balanceIQD == 0):
            return True
        else:
            return False

print(20*'-' + 'is_zero' + 20*'-')

print(Balance.is_zero(Balance(([{
    'currency': 'USD',
    'sum': 0
}, {
    'currency': 'IQD',
    'sum': 0
}]))))






print(20*'-' + '>' + 20*'-')

Balance([{
            'currency': 'USD',
            'sum': 200
        }, {
            'currency': 'IQD',
            'sum': 300
        }])> Balance([{
            'currency': 'USD',
            'sum': 500
        }, {
            'currency': 'IQD',
            'sum': 255
        }])
      
print(20*'-' + '<' + 20*'-')

Balance([{
            'currency': 'USD',
            'sum': 600
        }, {
            'currency': 'IQD',
            'sum': 300
        }])< Balance([{
            'currency': 'USD',
            'sum': 500
        }, {
            'currency': 'IQD',
            'sum': 255
        }])
      