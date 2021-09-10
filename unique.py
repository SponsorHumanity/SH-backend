# Python test program to check if two
# to get unique values from list
# using traversal
 
# function to get unique values
def getUnique(list1):
 
    # intilize a null list
    unique_list = []
     
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list 
    #for x in unique_list:
    #  print (x)
    unique_list.sort()
    return( unique_list )
     
   

if __name__ == '__main__':
  #driver code
  list1 = [10, 25, 75, 100, 50, 75, 50, 150]
  print("the unique values from 1st list is")
  ul = []
  ul = getUnique(list1)
  ul.sort()
  print( ul )
  
  list2 =[1, 2, 1, 1, 3, 4, 3, 3, 5]
  print("\nthe unique values from 2nd list is")
  ul = getUnique(list2)
  print( ul)
