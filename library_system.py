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
            return False

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

#testing:
if __name__ == "__main__":

    library = LibrarySystem()

    print("===== ADD MEMBERS =====")
    assert library.add_member("2024-EE-001", "Ali", "Student") is True
    assert library.add_member("2024-EE-002", "Sara", "Student") is True
    assert library.add_member("2024-EE-001", "Duplicate", "Student") is False
    print("Members added successfully")

    print("\n===== ADD BOOKS =====")
    assert library.add_book("ISBN001", "Python 101", "John Doe", 2021, "Programming", 3) is True
    assert library.add_book("ISBN002", "Data Structures", "Jane Smith", 2020, "CS", 2) is True
    assert library.add_book("ISBN003", "Advanced Python", "John Doe", 2022, "Programming", 1) is True

    # Duplicate ISBN
    assert library.add_book("ISBN001", "Duplicate Book", "Someone", 2023, "Test", 1) is False
    print("Books added successfully")

    print("\n===== SEARCH BY ISBN =====")
    book = library.search_by_isbn("ISBN001")
    assert book is not None
    assert book.book_data["title"] == "Python 101"

    assert library.search_by_isbn("INVALID") is None
    print("Search by ISBN passed")

    print("\n===== SEARCH BY TITLE =====")
    book = library.search_by_title("Python 101")
    assert book is not None
    assert book.isbn == "ISBN001"

    assert library.search_by_title("Nonexistent Title") is None
    print("Search by title passed")

    print("\n===== SEARCH BY AUTHOR =====")
    books = library.search_by_author("John Doe")
    assert len(books) == 2

    books = library.search_by_author("Unknown Author")
    assert books == []
    print("Search by author passed")

    print("\n===== BORROW BOOK =====")
    assert library.borrow_book("2024-EE-001", "ISBN001") is True
    assert library.borrow_book("2024-EE-001", "ISBN001") is True
    assert library.borrow_book("2024-EE-001", "ISBN001") is True

    # No copies left
    assert library.borrow_book("2024-EE-002", "ISBN001") is False

    member = library.members.search("2024-EE-001")
    assert len(member.borrowed) == 3

    book = library.search_by_isbn("ISBN001")
    assert book.book_data["available_copies"] == 0
    print("Borrow system passed")

    print("\n===== RETURN BOOK =====")
    member = library.members.search("2024-EE-001")
    borrowed_before = len(member.borrowed)

    book = library.search_by_isbn("ISBN001")
    copies_before = book.book_data["available_copies"]

    assert library.return_book("2024-EE-001", "ISBN001") is True

    member = library.members.search("2024-EE-001")
    book = library.search_by_isbn("ISBN001")

    assert len(member.borrowed) == borrowed_before - 1
    assert book.book_data["available_copies"] == copies_before + 1

    print("Return system passed")

