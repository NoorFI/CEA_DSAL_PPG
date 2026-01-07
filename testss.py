from library_system import LibrarySystem
import random

# ----------------------------
# Helper functions
# ----------------------------
def print_books(library, isbns):
    """Print book details given a list of ISBNs"""
    if not isbns:
        print("  No books found.")
        return
    for isbn in isbns:
        node = library.catalog.search(library.root, isbn)
        if node:
            bd = node.book_data
            print(f"  {isbn} | {bd['title']} | {bd['author']} | {bd['year']} | Copies: {bd['available_copies']}")
        else:
            print(f"  {isbn} | (not found in catalog)")

def print_members(library):
    """Print all members and their borrowed books"""
    for bucket in library.members.table:
        cur = bucket
        while cur:
            print(f"  {cur.member_id} | {cur.name} | Borrowed: {cur.borrowed}")
            cur = cur.next

# ----------------------------
# Test suite
# ----------------------------
if __name__ == "__main__":

    library = LibrarySystem()

    print("\n=== Test 1: Empty Library Checks ===")
    print("Search ISBN000:", library.search_by_isbn("ISBN000"))
    print("Search title:", library.search_by_title("Nothing"))
    print("Borrow when no members:", library.borrow_book("ID", "ISBN000"))
    print("Return when empty:", library.return_book("ID", "ISBN000"))

    print("\n=== Test 2: Add 20 Members ===")
    for i in range(1, 21):
        mid = f"2024-EE-{i:03d}"
        library.add_member(mid, f"User{i}", "Student")

    print("\nAll Members:")
    print_members(library)

    print("\n=== Test 3: Add 50 Books ===")
    authors = ["John Doe", "Jane Smith", "Alan Turing", "Ada Lovelace", "Tim Berners-Lee"]
    categories = ["Programming", "CS", "Math", "AI", "Networks"]

    for i in range(1, 51):
        isbn = f"ISBN{i:03d}"
        title = f"Book{i}"
        author = random.choice(authors)
        year = random.randint(1990, 2024)
        category = random.choice(categories)
        copies = random.randint(1, 5)
        library.add_book(isbn, title, author, year, category, copies)

    print("\nTotal Books (50 expected):")
    print_books(library, library.list_all_books())

    print("\n=== Test 4: Search Tests ===")
    print("Search by ISBN = ISBN010:", library.search_by_isbn("ISBN010"))
    print("Search by title = Book20:", library.search_by_title("Book20"))

    print("\nBooks by Alan Turing:")
    author_books = library.search_by_author("Alan Turing")
    author_isbns = [b.isbn for b in author_books]  # convert to ISBNs
    print_books(library, author_isbns)

    print("\nBooks by Unknown Author:")
    author_books = library.search_by_author("Nobody")
    author_isbns = [b.isbn for b in author_books]
    print_books(library, author_isbns)

    print("\n=== Test 5: Borrow Books ===")
    print("User001 borrows ISBN001 5 times (stock & limit test)")
    for _ in range(5):
        print("  Borrow:", library.borrow_book("2024-EE-001", "ISBN001"))

    print("\nUser002 tries borrowing ISBN001 (may be unavailable):")
    print("  Borrow:", library.borrow_book("2024-EE-002", "ISBN001"))

    print("\nCheck members after borrowing:")
    print_members(library)

    print("\n=== Test 5B: Borrow Limit Enforcement ===")
    print("User003 borrows ISBN010:", library.borrow_book("2024-EE-003", "ISBN010"))
    print("User003 tries another ISBN020:", library.borrow_book("2024-EE-003", "ISBN020"))

    print("\n=== Test 6: Return Books ===")
    print("User001 returns ISBN001 twice:")
    print("  Return:", library.return_book("2024-EE-001", "ISBN001"))
    print("  Return:", library.return_book("2024-EE-001", "ISBN001"))

    print("\nBooks after return:")
    print_books(library, library.list_all_books())

    print("\n=== Test 7: Reporting Functions ===")
    # Books borrowed by User001
    u = library.members.search("2024-EE-001")
    print("\nBooks borrowed by User001:", u.borrowed)
    
    # Books by Jane Smith
    jane_books = library.search_by_author("Jane Smith")
    jane_isbns = [b.isbn for b in jane_books]
    print("\nBooks by Jane Smith:")
    print_books(library, jane_isbns)

    # Available books
    available_books = library.list_available_books()
    available_isbns = [b.isbn for b in available_books]
    print("\nAvailable books (>0 copies):")
    print_books(library, available_isbns)

    # All books sorted by ISBN
    print("\nAll books sorted by ISBN:")
    print_books(library, library.list_all_books())

    print("\n=== Test 8: Edge Cases ===")
    print("Borrow with non-existent user:", library.borrow_book("NO-ID", "ISBN001"))
    print("Borrow non-existent book:", library.borrow_book("2024-EE-003", "NO-ISBN"))
    print("Return book user never borrowed:", library.return_book("2024-EE-004", "ISBN002"))

    print("\nAll Tests Completed!\n")
