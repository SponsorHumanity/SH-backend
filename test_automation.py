import logging
import time
#import walmartautomation
import krogerautomation
import publixautomation
import wholefoodsautomation

#logger = logging.getLogger('dev')
#logger.setLevel(logging.INFO)

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

for x in range(4):
  print( 'Iteration #', x )

  #krogerautomation.error_handles('10','cbogusky@hotmail.com' )
  
  #status = walmartautomation.error_handles('10','cbogusky@hotmail.com', 'clay bogusky' )
  #print( "Walmart status = ", status )
  #time.sleep( 20 )
  #walmartautomation.cleanUp()

  
  # Get preferred gift card from Person 
  krogerautomation.error_handles('10','cbogusky@hotmail.com' )
  #walmartautomation.PurchaseWalmartcard('10','cbogusky@hotmail.com', 'clay bogusky' )
  time.sleep( 10 )
  publixautomation.error_handles('10','cbogusky@hotmail.com' )
  time.sleep( 10 )
  wholefoodsautomation.error_handles('10','cbogusky@hotmail.com' )
  time.sleep( 10 )


