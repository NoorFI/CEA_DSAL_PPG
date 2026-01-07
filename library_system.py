from avl_tree import BookCatalog
from hash_table import Title, Author, Member


class LibrarySystem:
    def __init__(self):
        self.catalog = BookCatalog()
        self.root = None
        self.title_index = Title(267)
        self.author_index = Author(267)
        self.members = Member(50)
        self.book_count = 0

    def add_book(self, isbn, title, author, year, category, copies):
        if self.book_count >= 200:
            return False

        if self.catalog.search(self.root, isbn):
            return False

        self.root = self.catalog.insert(
            self.root, isbn, title, author, year, category, copies
        )

        self.title_index.insert(title, isbn)
        self.author_index.add(author, isbn)
        self.book_count += 1
        return True

    def add_member(self, member_id, name, member_type):
        return self.members.add(member_id, name, member_type)

    def search_by_isbn(self, isbn):
        return self.catalog.search(self.root, isbn)

    def search_by_title(self, title):
        isbn = self.title_index.contains(title)
        return self.catalog.search(self.root, isbn) if isbn else None

    def search_by_author(self, author):
        isbn_list = self.author_index.search(author)
        books = []
        while isbn_list:
            book = self.catalog.search(self.root, isbn_list.isbn)
            if book:
                books.append(book)
            isbn_list = isbn_list.next
        return books

    def borrow_book(self, member_id, isbn):
        member = self.members.search(member_id)
        book = self.catalog.search(self.root, isbn)

        if not member or not book:
            return False

        if len(member.borrowed) >= 5:
            return "Borrow Limit Reached"

        if book.book_data["available_copies"] <= 0:
            return False

        book.book_data["available_copies"] -= 1
        member.borrowed.append(isbn)
        return True

    def return_book(self, member_id, isbn):
        member = self.members.search(member_id)
        book = self.catalog.search(self.root, isbn)

        if not member or isbn not in member.borrowed or not book:
            return False

        member.borrowed.remove(isbn)
        book.book_data["available_copies"] += 1
        return True

    def list_all_books(self):
        return self.catalog.inorder_traversal(self.root)
    
    def list_books_borrowed_by_member(self, member_id):
        member = self.members.search(member_id)
        if not member:
            return []

        books = []
        for isbn in member.borrowed:
            book = self.catalog.search(self.root, isbn)
            if book:
                books.append(book)
        return books

    def list_available_books(self):
        all_isbns = self.catalog.inorder_traversal(self.root)
        available_books = []

        for isbn in all_isbns:
            book = self.catalog.search(self.root, isbn)
            if book and book.book_data["available_copies"] > 0:
                available_books.append(book)

        return available_books

