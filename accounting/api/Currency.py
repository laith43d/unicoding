
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
        result=[{
            'currency': 'USD',
            'sum': self.balanceUSD
        }, {
            'currency': 'IQD',
            'sum': self.balanceIQD
        }]
#task 4 
        def currency(self,other):
            IQD=True
            USD=True
            if  self.balanceIQD ==0 and self.balanceUSD == 0:
                IQD=False
                USD=False
            else:
                if self.balanceIQD>other.balanceIQD :
                    IQD=True
                elif self.balanceIQD<other.balanceIQD:
                    IQD=False
                if self.balanceUSD>other.balanceUSD:
                    USD=True
                elif self.balanceUSD<other.balanceUSD:
                    USD=False
            return{'IQD':IQD,'USD':USD}