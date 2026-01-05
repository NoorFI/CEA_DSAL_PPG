class Node:
    def __init__(self,item,value,next):
        self.item=item
        self.value=value
        self.next=next
class Title_Index:
    def __init__(self):
       
        self.array=[[] for _ in range(m)]#shortcut in python 
        self.m=m
        self.n=0
        self.lf=self.n/self.m
    def hashfunc(book_t,m):
         book_t=book_t.strip()
         book_t=book_t.lower()
         sum=0
         for char in book_t:
                 sum=ord(char)+sum 
         return sum%m 
    def insert(self,book_t,isbn=None):
          index=Title_Index.hashfunc(book_t,self.m)
          if len(self.array[index]) == 0:
            new_node = Node(book_t,isbn)
            self.array[index].append(new_node)
            self.n += 1
          else:
               current = self.array[index][0]
               prev = None
               while current is not None:
                 if current.book_t == book_t:
                  
                   return
                 prev = current
                 current = current.next
               new_node = Node(book_t, isbn)
               prev.next = new_node
               self.n += 1
          lf=self.n/self.m
          if lf>0.75 :
               print ("need to resize")   
               self.resize()   
    def resize(self):
          old_array=self.array
          self.m=self.m*2
          self.array = [[] for _ in range(self.m)]
          self.n = 0
          for bucket in old_array:
            if len(bucket) > 0:
                cores_bucket = bucket[0]
                while cores_bucket is not None:
                    self.insert(cores_bucket.book_t, cores_bucket.isbn)
                    cores_bucket = cores_bucket.next   


    def contains(self,book_t):
         index=Title_Index.hashfunc(book_t,self.m)
         if len(self.array[index]) > 0:
            cores_bucket = self.array[index][0] 
         else:
            cores_bucket = None
         while cores_bucket is not None:
            if cores_bucket.book_t == book_t:
                return True
            cores_bucket = cores_bucket.next   
         return False
    def delete(self,book_t):
        index=Title_Index.hashfunc(book_t,self.m)
        if len(self.array[index]) == 0:
            print("invalid entry")
        else:
               current = self.array[index][0]
               prev = None
               while current is not None:
                if current.book_t == book_t:
                   prev.next = current.next
                   self.n -= 1
                   return True
                prev = current
                current = current.next
               return False   
