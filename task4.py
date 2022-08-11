iqd = 50
usd = 40
def __gt__(self, other):
    IQD = bool(self.balanceiqd > other.balanceIQD)
    USD = bool(self.balanceUSD > other.balanceUSD)
    return IQD, USD


def __lt__(self, other):
    IQD = bool(self.balanceiqd < other.balanceIQD)
    USD = bool(self.balanceUSD < other.balanceUSD)
    return IQD, USD


def other_than_gt_and_ls(self, other):
    if self.balanceIQD > other.balanceIQD and self.balanceUSD < other.balanceUSD:
        return True, False
    else:
        return False, True


def is_zero(self):
    if self.balanceIQD == 0 and self.balanceUSD == 0:
        return True
    else:
        return False

print(iqd.__lt__(50))