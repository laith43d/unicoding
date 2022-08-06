class Balance:
          def __init__(self, amount1=None,cur1=None,amount2=None,cur2=None):
                    if amount1==None:
                              amount1=0
                              cur1='USD'
                    if amount2==None and cur1=='USD':
                              amount2=0
                              cur2='IQD'
                    elif amount2==None and cur1=='IQD':
                              amount2=0
                              cur2='USD'
                    self.amount1 = amount1
                    self.amount2 = amount2
                    self.cur1=cur1
                    self.cur2=cur2
          def __eq__(self, other):
                    if self.cur1 != other.cur1:
                              return f'Error! Defrent Currency type'
                    if self.cur2 != other.cur2:
                              return f'Error! Defrent Currency type'
                    return f'({self.amount1 == other.amount1} , {self.amount2==other.amount2})'
          def __lt__(self, other):
                    if self.cur1 != other.cur1:
                              return f'Error! Defrent Currency type'
                    if self.cur2 != other.cur2:
                              return f'Error! Defrent Currency type'
                    return f'({self.amount1 < other.amount1} , {self.amount2<other.amount2})'
          def __gt__(self, other):
                    if self.cur1 != other.cur1:
                              return f'Error! Defrent Currency type'
                    if self.cur2 != other.cur2:
                              return f'Error! Defrent Currency type'
                    return f'({self.amount1 > other.amount1} , {self.amount2>other.amount2})'
          def is_zero(self):
                    if self.amount1==0:
                              a=True
                    elif self.amount1!=0:
                              a=False
                    if self.amount2==0:
                              b=True
                    elif self.amount2!=0:
                              b=False
                    if a==True and b==True:
                              return True
                    elif a==False and b==False:
                              return False
                    return f'({a} , {b})'


a=Balance(200,'USD')
b=Balance(200,'USD',2000,'IQD')
print(a == b)
print(a < b)
print(a > b)
print(a.is_zero())