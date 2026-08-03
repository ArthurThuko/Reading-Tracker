from book import Book

class Audio_Book(Book):
    def __init__(self, title, pages, author, duration_minutes):
        super().__init__(title, pages, author)
        self.duration_minutes = duration_minutes
        
    def __repr__(self):
        return f"Audio_Book(title='{self.title}', pages={self.pages}, current_page={self.current_page}, author={self.author}, duration_minutes={self.duration_minutes})"