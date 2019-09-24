import sys
import pprint
pprint.pprint(sys.path)

from decimal import getcontext, Decimal
getcontext().prec = 1
Decimal(0.1) + Decimal(0.5)

