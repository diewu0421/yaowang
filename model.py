from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

book_author = db.Table("book_author",
                       db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
                       db.Column("author_id", db.Integer, db.ForeignKey("author.id"))
                       )


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    authors = db.relationship("Author", backref="books", secondary=book_author)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    age = db.Column(db.Integer)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.String(1000))


    def __repr__(self):
        return self.content

    def __str__(self):
        return self.content
