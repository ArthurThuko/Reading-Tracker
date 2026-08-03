class Book:
    def __init__(self, title, pages, author):
        self.title = title
        self.pages = pages
        self.author = author
        self.current_page = 0
    
    def __repr__(self):
        return f"Book(title='{self.title}', pages={self.pages}, current_page={self.current_page}, author={self.author})"

    @property
    def progress_percentage(self):
        if self.pages == 0:
            return 0
        return (self.current_page / self.pages) * 100