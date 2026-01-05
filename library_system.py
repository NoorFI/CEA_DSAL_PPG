from avl_tree import BookCatalog
from hash_table import Title, Author, Member

class Book:
    def __init__(self, isbn, title, author, year, category, copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.copies = copies

class LibrarySystem:
    def __init__(self):
        self.catalog = BookCatalog()
        self.root = None
        self.title_index = Title(267)
        self.author_index = Author(267)
        self.members = Member(50)

    def add_book(self, isbn, title, author, year, category, copies):
        book = Book(isbn, title, author, year, category, copies)

        self.root = self.catalog.insert(self.root, isbn, book)
        self.title_index.insert(title, isbn)
        self.author_index.add(author, isbn)

    def add_member(self, member_id, name):
        return self.members.add(member_id, name)
    
    def search_by_isbn(self, isbn):
        return self.catalog.search(self.root, isbn)

    def search_by_title(self, title):
        isbn = self.title_index.contains(title)
        if not isbn:
            return None
        return self.catalog.search(self.root, isbn)

    def search_by_author(self, author):
        isbn_list = self.author_index.search(author)
        if not isbn_list:
            return []

        books = []
        current = isbn_list

        while current:
            book = self.catalog.search(self.root, current.isbn)
            if book:
                books.append(book)
            current = current.next

        return books
    
    def borrow_book(self, member_id, isbn):
        member = self.members.search(member_id)
        if not member:
            print("Member not found")
            return False

        if len(member.borrowed) >= 5:
            print("Borrow limit reached")
            return False

        book = self.catalog.search(self.root, isbn)
        if not book:
            print("Book not found")
            return False

        if book.available_copies <= 0:
            print("Book unavailable")
            return False

        # Update system
        book.available_copies -= 1
        member.borrowed.append(isbn)
        return True
    
    def return_book(self, member_id, isbn):
        member = self.members.search(member_id)
        if not member or isbn not in member.borrowed:
            print("Invalid return")
            return False

        book = self.catalog.search(self.root, isbn)
        if not book:
            return False

        member.borrowed.remove(isbn)
        book.available_copies += 1
        return True

    def list_all_books(self):
        return self.catalog.inorder_traversal(self.root)
