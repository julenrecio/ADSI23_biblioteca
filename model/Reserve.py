class Reserve:
    def __init__(self, userId, bookId, reserveDate, returned):
        self.userId = userId
        self.bookId = bookId
        self.reserveDate = reserveDate
        self.returned = returned

    def __str__(self):
        return f'{self.userId} - {self.bookId} - {self.reserveDate} - {self.returned}'
