import time

for i in range( 10 ):
  time.sleep( .01 )
  # Option 1
  unix_time_ms_1 = int(time.time_ns() / 1000000)
  # Option 2
  unix_time_ms_2 = int(time.time() * 1000)
  #print( unix_time_ms_1 )
  print( unix_time_ms_2 )

  