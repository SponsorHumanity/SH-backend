#jagged = [[1], [2, 3], [4, 5, 6]]
jagged = [
        [10, 1],
        [25, 2], 
        [50, 5],
        [100, 2],
        [125, 1],
        [150, 1]
]


for value in jagged:                                                           
      i = 0                                                                   
      j = 0                                                                   
      if isinstance(value, list):                                             
          for other in value:                                                 
              #print("jagged[%s][%s] = %s" % (i, j, other))  
              print("jagged[%d] = %d" % (i, other))                                              
              i += 1                                                          
              #j += 1 

print( "done!" )
if ( jagged[0][0] == 10):
    print( jagged[0][0])
print( jagged[1][0])
print( jagged[2][0])


# a[0][0] = 1
# a[1][0] = 2
# a[1][1] = 3
# a[2][0] = 4
# a[2][1] = 5
# a[2][2] = 6