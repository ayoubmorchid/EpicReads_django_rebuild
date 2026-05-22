from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookForm, RegisterForm
from .models import Book, Category


def home(request):
    featured_books = Book.objects.select_related("category")[:5]
    selling_books = Book.objects.select_related("category")[5:10]
    categories = Category.objects.prefetch_related("books")[:6]
    return render(
        request,
        "library/home.html",
        {
            "featured_books": featured_books,
            "selling_books": selling_books,
            "categories": categories,
            "total_books": Book.objects.count(),
            "total_categories": Category.objects.count(),
        },
    )


def book_list(request):
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")
    books = Book.objects.select_related("category")
    categories = Category.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(description__icontains=query)
        )

    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        books = books.filter(category=selected_category)

    favorite_ids = set(request.session.get("favorites", []))
    favorite_books = Book.objects.filter(pk__in=favorite_ids).select_related("category")
    paginator = Paginator(books, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    querystring = request.GET.copy()
    querystring.pop("page", None)

    return render(
        request,
        "library/books.html",
        {
            "books": page_obj.object_list,
            "categories": categories,
            "query": query,
            "selected_category": selected_category,
            "favorite_ids": favorite_ids,
            "favorite_books": favorite_books,
            "page_obj": page_obj,
            "querystring": querystring.urlencode(),
        },
    )


def book_detail(request, pk):
    book = get_object_or_404(Book.objects.select_related("category"), pk=pk)
    recommended_books = (
        Book.objects.select_related("category")
        .exclude(pk=book.pk)
        .filter(category=book.category)[:4]
    )
    return render(
        request,
        "library/book_detail.html",
        {"book": book, "recommended_books": recommended_books},
    )


@login_required
def book_create(request):
    form = BookForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        book = form.save()
        messages.success(request, "Book added successfully.")
        return redirect("book_detail", pk=book.pk)
    return render(request, "library/book_form.html", {"form": form, "title": "Add Book"})


@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=book)
    if form.is_valid():
        book = form.save()
        messages.success(request, "Book updated successfully.")
        return redirect("book_detail", pk=book.pk)
    return render(request, "library/book_form.html", {"form": form, "title": "Edit Book"})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect("book_list")
    return render(request, "library/book_confirm_delete.html", {"book": book})


def about(request):
    return render(request, "library/about.html")


def contact(request):
    if request.method == "POST":
        messages.success(request, "Form submitted successfully!")
        return redirect("contact")
    return render(request, "library/contact.html")


@login_required
def checkout(request):
    book_id = request.GET.get("book")

    if book_id:
        book = get_object_or_404(Book, pk=book_id, available=True)
        cart = request.session.get("cart", {})
        cart_key = str(book.pk)
        cart[cart_key] = cart.get(cart_key, 0) + 1
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request, f"{book.title} added to your cart.")
        return redirect("checkout")

    cart = request.session.get("cart", {})
    book_ids = [int(book_id) for book_id in cart.keys()]
    books = Book.objects.filter(pk__in=book_ids).select_related("category")
    books_by_id = {book.pk: book for book in books}

    cart_items = []
    total = 0
    for book_id_text, quantity in cart.items():
        book = books_by_id.get(int(book_id_text))
        if not book:
            continue
        price = 120
        subtotal = price * quantity
        total += subtotal
        cart_items.append(
            {
                "book": book,
                "quantity": quantity,
                "price": price,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "library/checkout.html",
        {"cart_items": cart_items, "total": total},
    )


@login_required
def cart_update(request, pk):
    if request.method != "POST":
        return redirect("checkout")

    cart = request.session.get("cart", {})
    cart_key = str(pk)
    action = request.POST.get("action")

    if cart_key not in cart:
        return redirect("checkout")

    if action == "increase":
        cart[cart_key] += 1
    elif action == "decrease":
        cart[cart_key] -= 1
        if cart[cart_key] <= 0:
            cart.pop(cart_key, None)
    elif action == "remove":
        cart.pop(cart_key, None)

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("checkout")


@login_required
def favorite_toggle(request, pk):
    if request.method != "POST":
        return redirect("book_list")

    book = get_object_or_404(Book, pk=pk)
    favorites_list = request.session.get("favorites", [])

    if book.pk in favorites_list:
        favorites_list.remove(book.pk)
        messages.success(request, f"{book.title} removed from favorites.")
    else:
        favorites_list.append(book.pk)
        messages.success(request, f"{book.title} added to favorites.")

    request.session["favorites"] = favorites_list
    request.session.modified = True
    return redirect(request.POST.get("next") or "book_list")


def payment(request):
    return render(request, "library/payment.html")


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Registered successfully!")
        return redirect("home")
    return render(request, "registration/register.html", {"form": form})
