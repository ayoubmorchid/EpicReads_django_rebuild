from django.db import migrations


BOOKS = [
    ("Roman", "To Kill a Mockingbird", "Harper Lee", "A moving novel about justice, childhood, courage, and moral growth in a small Southern town.", "books/to_kill_a_mockingbird.jpg"),
    ("Roman", "Jane Eyre", "Charlotte Bronte", "A classic story of independence, resilience, mystery, and love.", "books/jane_eyre.jpg"),
    ("Roman", "The Book Thief", "Markus Zusak", "A powerful historical novel about words, friendship, and survival during wartime.", "books/the_book_thief.jpg"),
    ("Science-fiction", "Brave New World", "Aldous Huxley", "A dystopian science-fiction classic about comfort, control, technology, and freedom.", "books/brave_new_world.jpg"),
    ("Science-fiction", "Foundation", "Isaac Asimov", "A landmark science-fiction saga about empire, mathematics, history, and the future of civilization.", "books/foundation.jpg"),
    ("Science-fiction", "Neuromancer", "William Gibson", "A cyberpunk novel about hackers, artificial intelligence, and a high-tech underground world.", "books/neuromancer.jpg"),
    ("Fantasy", "Mistborn", "Brandon Sanderson", "An inventive fantasy about rebellion, metals-based magic, and a world covered in ash.", "books/mistborn.jpg"),
    ("Fantasy", "The Way of Kings", "Brandon Sanderson", "An epic fantasy about honor, war, broken kingdoms, and extraordinary powers.", "books/the_way_of_kings.jpg"),
    ("Fantasy", "A Game of Thrones", "George R. R. Martin", "A political fantasy of noble houses, dangerous ambition, and a kingdom on the edge of war.", "books/a_game_of_thrones.jpg"),
    ("Economy", "The Lean Startup", "Eric Ries", "A modern business book about building products, testing ideas, and learning quickly.", "books/the_lean_startup.jpg"),
    ("Economy", "Good to Great", "Jim Collins", "A business classic about discipline, leadership, and how companies move from average to excellent.", "books/good_to_great.jpg"),
    ("Economy", "The Intelligent Investor", "Benjamin Graham", "A foundational investing book about value, discipline, risk, and long-term thinking.", "books/the_intelligent_investor.jpg"),
    ("Philosophy", "The Republic", "Plato", "A foundational philosophical dialogue about justice, society, education, and the ideal state.", "books/the_republic.jpg"),
    ("Philosophy", "Sophie's World", "Jostein Gaarder", "A novel-style introduction to the history of philosophy and big questions about life.", "books/sophies_world.jpg"),
    ("Technology", "Code Complete", "Steve McConnell", "A detailed guide to writing better software through practical construction and engineering habits.", "books/code_complete.jpg"),
    ("Technology", "Design Patterns", "Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides", "A classic software engineering book about reusable object-oriented design solutions.", "books/design_patterns.jpg"),
    ("Technology", "The Clean Coder", "Robert C. Martin", "A professional guide to discipline, responsibility, communication, and craftsmanship in software work.", "books/the_clean_coder.jpg"),
    ("Personal Development", "The 7 Habits of Highly Effective People", "Stephen R. Covey", "A personal development classic about principles, priorities, leadership, and character.", "books/the_7_habits.jpg"),
    ("Personal Development", "Grit", "Angela Duckworth", "A book about passion, perseverance, effort, and long-term achievement.", "books/grit.jpg"),
    ("Psychology", "Influence", "Robert B. Cialdini", "A psychology book about persuasion, decision-making, and the principles that shape human behavior.", "books/influence.jpg"),
]


def add_books(apps, schema_editor):
    Category = apps.get_model("library", "Category")
    Book = apps.get_model("library", "Book")

    for category_name, title, author, description, image in BOOKS:
        category, _ = Category.objects.get_or_create(name=category_name)
        Book.objects.get_or_create(
            title=title,
            defaults={
                "author": author,
                "category": category,
                "description": description,
                "image": image,
                "available": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0003_add_more_books"),
    ]

    operations = [
        migrations.RunPython(add_books, migrations.RunPython.noop),
    ]
