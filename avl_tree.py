class BookNode: #basic variables
    def __init__ (self , isbn, book_data):
        self.isbn = isbn
        self.book_data = book_data
        self.left = None
        self.right = None
        self.height = 1
        
        
class BookCatalog: #avl tree
    def get_height(self, BookNode):
        if not BookNode:
            return 0
        return BookNode.height
    
    def get_balance(self, BookNode):
        if not BookNode:
            return 0 
        return self.get_height(BookNode.left) - self.get_height(BookNode.right)

    def rotate_right(self, y):
        #checking the node's position
        x = y.left
        T2 = x.right
        #implementing the rotation
        x.right = y
        y.left = T2
        #rebalancing 
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x #new root

    def rotate_left(self, x):
        #checking the node's position
        y = x.right
        T2 = y.left
        #implementing the rotation
        y.left = x
        x.right = T2
        #rebalancing 
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y #new root
    
    def insert(self, root, isbn, book_data):
        #insertion
        if not root:
            return BookNode(isbn, book_data)
        if isbn < root.isbn:
            root.left = self.insert(root.left, isbn, book_data)
        elif isbn > root.isbn:
            root.right = self.insert(root.right, isbn, book_data)
        else:
            return root 
        #rebalance it again
        root.height = 1 + max(self.get_height(root.left),self.get_height(root.right))
        balance_factor = self.get_balance(root)
        
        #balance cases:
        #left left case
        if balance_factor > 1 and isbn < root.left.isbn:
            return self.rotate_right(root)
        #right right case
        if balance_factor < -1 and isbn > root.right.isbn:
            return self.left_rotate(root)
        #left right case
        if balance_factor > 1 and isbn > root.left.isbn:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        #right left case
        if balance_factor < -1 and isbn < root.right.isbn:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        
        return root
    
    def search(self,root,isbn):
        if root is None:
            return False
        if isbn == isbn.key:
            return True
        elif isbn< root.key:
            return self.search(root.left, isbn)
        else:
            return self.search(root.right, isbn)

    result =[]     
    def inorder_traversal(self, node, result ):
        if node is None:
            return None
        self.inorder_traversal(node.left, result)
        result.append(node.isbn)
        self.inorder_traversal(node.right, result)
        return result
