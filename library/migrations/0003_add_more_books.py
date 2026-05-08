from django.db import migrations


BOOKS = [
    (
        "Roman",
        "Pride and Prejudice",
        "Jane Austen",
        "A beloved classic about family, manners, pride, and the slow discovery of love.",
        "books/pride_and_prejudice.jpg",
    ),
    (
        "Science-fiction",
        "Dune",
        "Frank Herbert",
        "A sweeping science-fiction epic about politics, survival, ecology, and destiny on the desert planet Arrakis.",
        "books/dune.jpg",
    ),
    (
        "Fantasy",
        "The Name of the Wind",
        "Patrick Rothfuss",
        "A lyrical fantasy about a gifted young musician and magician telling the story of his extraordinary life.",
        "books/the_name_of_the_wind.jpg",
    ),
    (
        "Economy",
        "Zero to One",
        "Peter Thiel",
        "A focused business book about startups, innovation, monopoly thinking, and building something truly new.",
        "books/zero_to_one.jpg",
    ),
    (
        "Philosophy",
        "Meditations",
        "Marcus Aurelius",
        "A timeless collection of Stoic reflections on discipline, humility, resilience, and living with purpose.",
        "books/meditations.jpg",
    ),
    (
        "Technology",
        "The Pragmatic Programmer",
        "Andrew Hunt and David Thomas",
        "A practical software craftsmanship guide about writing flexible, maintainable, and thoughtful code.",
        "books/the_pragmatic_programmer.jpg",
    ),
    (
        "Personal Development",
        "Mindset",
        "Carol S. Dweck",
        "A powerful book about fixed and growth mindsets, learning, effort, and personal progress.",
        "books/mindset.jpg",
    ),
    (
        "Psychology",
        "Thinking, Fast and Slow",
        "Daniel Kahneman",
        "A psychology classic explaining the two systems of thought behind judgment, bias, and decision-making.",
        "books/thinking_fast_and_slow.jpg",
    ),
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
        ("library", "0002_seed_books"),
    ]

    operations = [
        migrations.RunPython(add_books, migrations.RunPython.noop),
    ]
