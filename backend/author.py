class Author:
    def __init__(self, name, country):
        self.name = name
        self.country = country

    def __repr__(self):
        return f"Author(name='{self.name}', country='{self.country}')"