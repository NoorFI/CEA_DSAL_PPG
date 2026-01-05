class Node:
    def __init__(self,book_t,isbn,next=None):
        self.book_t=book_t
        self.isbn=isbn
        self.next=next

class Title:
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

class Author:
    def __init__(self, m = 267):
        self.m = m
        self.table=[None for _ in range(m)]
        self.n=0
    
    def hashfunc(self, author):
        author = author.strip().lower()
        sum=0

        for char in author:
            sum += ord(char)

        return sum % self.m 
    
    def add(self, author, isbn):
        index = self.hashfunc(author)
        
        current = self.table[index]

        while current:
            if current.book_t == author:
                new_isbn = Node(isbn, None, current.isbn)
                current.isbn = new_isbn
                return
            current = current.next
        
        isbn_node = Node(isbn, None)
        new_node = Node(author, isbn_node, self.table[index])
        self.table[index] = new_node
        self.n += 1

    def search(self, author):
        index = self.hashfunc(author)

        current = self.table[index]

        while current:
            if current.book_t == author:
                return current.isbn
            current = current.next

        return None
    
    def delete_Author(self, author):
        index = self.hashfunc(author)

        current = self.table[index]
        prev = None

        while current:
          if current.book_t == author:
            if prev:
              prev.next = current.next
            else:
              self.table[index] = current.next
            self.n -= 1
            return True
          prev = current
          current = current.next

        return False

class MemberNode:
    def __init__(self, member_id, name, borrowed=None, next=None):
        self.member_id = member_id
        self.name = name
        self.borrowed = borrowed if borrowed else []
        self.next = next

class Member:
    def __init__(self, m = 50):
        self.m = m
        self.table = [None] * m
        self.n = 0

    def hashfunc(self, member_id):
        member_id = member_id.strip().lower()
        sum=0

        for char in member_id:
            sum += ord(char)

        return sum % self.m
    
    def add(self, member_id, name):
        index = self.hashfunc(member_id)
        current = self.table[index]

        while current:
            if current.member_id == member_id:
                print("Member already exists")
                return False
            current = current.next
        
        new_node = MemberNode(member_id, name, next=self.table[index])
        self.table[index] = new_node
        self.n += 1
        return True
    
    def search(self, member_id):
        index = self.hashfunc(member_id)
        current = self.table[index]

        while current:
            if current.member_id == member_id:
                return current
            current = current.next

        return None
    
    def delete(self, member_id):
        index = self.hashfunc(member_id)

        current = self.table[index]
        prev = None

        while current:
          if current.member_id == member_id:
            if prev:
              prev.next = current.next
            else:
              self.table[index] = current.next
            self.n -= 1
            return True
          prev = current
          current = current.next

        return False