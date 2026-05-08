from django.db import migrations


BOOKS = [
    ("Roman", "The Great Gatsby", "F. Scott Fitzgerald", "A classic novel about wealth, love, ambition, and the American dream.", "books/book1.png"),
    ("Personal Development", "Atomic Habits", "James Clear", "A practical guide to building good habits and breaking bad ones.", "books/book2.png"),
    ("Fantasy", "Harry Potter", "J.K. Rowling", "A fantasy story about magic, friendship, courage, and adventure.", "books/HARRY.jpg"),
    ("Economy", "Rich Dad Poor Dad", "Robert Kiyosaki", "A book about money, investing, financial education, and mindset.", "books/book4.png"),
    ("Philosophy", "The Alchemist", "Paulo Coelho", "A philosophical story about dreams, destiny, and personal journey.", "books/book3.png"),
    ("Technology", "Clean Code", "Robert C. Martin", "A programming book about writing readable, maintainable, and clean code.", "books/book5.png"),
    ("Personal Development", "Think and Grow Rich", "Napoleon Hill", "A personal development book about success, goals, and mindset.", "books/HOOVER.jpg"),
    ("Psychology", "The Psychology of Money", "Morgan Housel", "A book about financial behavior, money decisions, and long-term thinking.", "books/KINGDOM.jpg"),
    ("Personal Development", "Deep Work", "Cal Newport", "A productivity book about focus, discipline, and meaningful work.", "books/HOLLOW.jpg"),
    ("Science-fiction", "1984", "George Orwell", "A dystopian novel about surveillance, power, control, and freedom.", "books/UNIVERSE.jpg"),
    ("Fantasy", "The Hobbit", "J.R.R. Tolkien", "A fantasy adventure about Bilbo Baggins and his unexpected journey.", "books/ROBERTS.jpg"),
    ("Economy", "Start With Why", "Simon Sinek", "A business and leadership book about purpose and inspiration.", "books/XOXO.jpg"),
]


def seed_books(apps, schema_editor):
    Category = apps.get_model("library", "Category")
    Book = apps.get_model("library", "Book")

    categories = {}
    for category_name, *_ in BOOKS:
        categories[category_name], _ = Category.objects.get_or_create(name=category_name)

    for category_name, title, author, description, image in BOOKS:
        Book.objects.get_or_create(
            title=title,
            defaults={
                "author": author,
                "category": categories[category_name],
                "description": description,
                "image": image,
                "available": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_books, migrations.RunPython.noop),
    ]
