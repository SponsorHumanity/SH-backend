def dpMakeChange(coinValueList,change,minCoins,coinsUsed):
   # Sanity check the amount (don't want to deal with coin values = 1)
   _invalid_amt = 0
   if (change == 0):
      return ( 0 )
   for coin in coinValueList:
      if ( change < coin ):
         #print( "invalid")
         _invalid_amt += 1
   if ( _invalid_amt == len( coinValueList ) ):
      return( 0 )

   for cents in range(change+1):
      coinCount = cents
      newCoin = 1
      for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents-j] + 1 < coinCount:
               coinCount = minCoins[cents-j]+1
               newCoin = j
      minCoins[cents] = coinCount
      coinsUsed[cents] = newCoin
   return ( len( minCoins ) )

def printCoins(coinsUsed,change):
   _coinList = []

   coin = change
   #print( 'length of array:', len(coinsUsed))
   while coin > 0:
      thisCoin = coinsUsed[coin]
      #print('coin=', thisCoin)
      _coinList.append( thisCoin )
      coin = coin - thisCoin

   return( _coinList )

if __name__ == '__main__':
    amnt = 150
    clist = [ 15, 25, 35, 50, 350 ]
    _offerSearchList = []
    coinsUsed = [0]*(amnt+1)
    coinCount = [0]*(amnt+1)

    print("Making change for",amnt,"requires")
    _status = dpMakeChange(clist,amnt,coinCount,coinsUsed)
    if ( _status == 0 ):
         print( "Can't make change for ", amnt, ' from this list of coins', clist )
         exit( 1 )
    print("The list:")
    _offerSearchList = printCoins(coinsUsed,amnt)
    print( _offerSearchList )
    #print("The used list is as follows:")
    #print(coinsUsed)

