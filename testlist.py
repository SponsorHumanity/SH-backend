
from collections import Counter

A = [ 5,  10,  10, 10, 10, 10, 125  ] # coins
C = [ 0,  0,  0,  0,  0,   0,   0 ]

B = [10, 10, 25, 5, 10, 100, 150, 50, 10, 125] # _offer_list
B1 =[11, 22, 33, 44, 55,  66,  77, 88, 99,   1 ] # timestamp
B2 =[ 0,  0,  0,  0,  0,   0,   0,  0,  0,   0 ] # reserved

def findts( dollar, ndx ):
  while ndx < len( B ):
    if ( (dollar == B[ndx]) and (B2[ndx]== 0)):
      B2[ndx] = 1
      return( B1[ndx] )
    ndx += 1
  return( 0 )

for _a, a in enumerate( A):
  ts = findts(a, 0 )
  C[_a] = ts
  print( ts )

print ( C )