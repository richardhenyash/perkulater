from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Size, Type, Price, Coffee, Offer
from .forms import CoffeeForm, ProductForm
from .helpers import get_product_offer_str


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    categories = None
    category = None
    categories_all = Category.objects.all()
    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")
    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            category = categories[0]

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search criteria!")
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(description_short__icontains=query)
            products = products.filter(queries)
            if (len(products)) == 0:
                messages.warning(request, "Your search didn't return any products.")
                return redirect(reverse('products'))

    products = products.order_by("name")
    
    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'search_term': query,
        'category': category,
        'categories_all': categories_all,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    categories_all = Category.objects.all()
    product_category = get_object_or_404(Category, name=product.category)
    product_sizes = get_list_or_404(Size, category=product.category)
    product_types = get_list_or_404(Type, category=product.category)
    product_prices = get_list_or_404(Price, product=product)

    # Build dictionary of sizes and prices for the product
    product_price_dict = {}
    for priceobj in product_prices:
        product_price_dict[priceobj.get_size()] = priceobj.get_price()

    product_offers = get_list_or_404(Offer, display_in_banner=True)
    product_offer_str = get_product_offer_str(product_offers, "  -  ")

    context = {
        'product': product,
        'product_category': product_category,
        'product_sizes': product_sizes,
        'product_types': product_types,
        'product_prices': product_prices,
        'product_price_dict': product_price_dict,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'categories_all': categories_all,
    }

    coffee_detail = get_object_or_404(Coffee, product=product)

    if coffee_detail:
        context['coffee_detail'] = coffee_detail

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product """

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            friendly_name = request.POST.get('friendly_name', '')
            print(friendly_name)
            messages.success(request, f"Succesfully added product {friendly_name}!")
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please check product form.')
    else:
        product_form = ProductForm
        coffee_form = CoffeeForm

    categories_all = Category.objects.all()
    template = "products/add_product.html"
    context = {
        'product_form': product_form,
        'coffee_form': coffee_form,
        'categories_all': categories_all,
        'on_admin_page': True,
    }
    return render(request, template, context)
