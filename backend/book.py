class Book:
    def __init__(self, id: int, name: str):
        self.id = id
        self.title = name
    
    def __repr__(self):
        return f"Book(name='{self.name}')"

    @property
    def progress_percentage(self):
        if self.pages == 0:
            return 0
        return (self.current_page / self.pages) * 100