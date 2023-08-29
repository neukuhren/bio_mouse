classrooms={'Ytyth': 0,'YTyth': 1,'YTYth': 2,'ytytH': 3,'ytyth': 4}
 
# class to be searched
class_room='ytYTH'
for idx in range(0, len(classrooms)+1):
    if classrooms[class_room.casefold()]:
        print(classrooms[idx])

 
#function to search item
# def search_classroom():
#    for classes in classrooms:
#        if class_room.casefold()==classes.casefold():
#            return True
 
#    else:
#        return False
 
# if search_classroom():
   
#   # If function returns true
#    print('Classroom you are searching is ')
 
# else:
   
#   # If function returns false
#    print('Classroom you are searching is no')