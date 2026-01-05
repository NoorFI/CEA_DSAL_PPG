class Node:
    def __init__(self,book_t,isbn,next=None):
        self.book_t=book_t
        self.isbn=isbn
        self.next=next
class Title_Index:
    def __init__(self,m):
       
        self.array=[None]*m 
        self.m=m
        self.n=0
        self.lf=self.n/self.m
    def hashfunc(self,book_t):
         book_t=book_t.strip().lower()
         sum=0
         for char in book_t:
                 sum=ord(char)+sum 
         return sum%self.m 
    def insert(self,book_t,isbn):
          book_t=book_t.strip().lower()
          index=self.hashfunc(book_t)
          current=self.array[index]
          while current:
                 if current.book_t == book_t:                
                   return
                 current = current.next
          new_node = Node(book_t, isbn,self.array[index])
          self.array[index] = new_node
          self.n += 1
          lf=self.n/self.m
          if lf>0.75 :
               print ("need to resize")   
               self.resize()   
    def resize(self):
          old_array=self.array
          self.m=self.m*2
          self.array = [None]*self.m
          self.n = 0
          for head in old_array:
            current = head
            while current is not None:
                self.insert(current.book_t, current.isbn)
                current = current.next


    def contains(self,book_t):
         book_t=book_t.strip().lower()
         index=self.hashfunc(book_t)
         current = self.array[index]
         while current is not None:
            if current.book_t == book_t:
                return True
            current = current.next
         return False

        
    def delete(self,book_t):
        book_t=book_t.strip().lower()
        index=self.hashfunc(book_t)
        current = self.array[index]
        prev = None
        if current is None:
            print("invalid entry")
            return False
        while current is not None:
                   if current.book_t == book_t:
                     if prev is None:
                        self.array[index] = current.next
                     else:
                        prev.next = current.next
                     self.n -= 1
                     return True
                   prev = current
                   current = current.next
        return False

                  
                   return
                 prev = current"""  
        





