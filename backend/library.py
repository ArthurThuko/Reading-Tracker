class Library:
    def __init__(self):
        self.books = []
        
    def add_book(self, book):
        self.books.append(book)
        
    @property
    def average_progress(self):
        if not self.books:
            return 0
        total_progress = sum(book.progress_percentage for book in self.books)
        return total_progress / len(self.books)