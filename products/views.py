from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Category, Price, Product, Size, Type, Coffee, Offer
from .forms import CoffeeForm, ProductForm
from .helpers import get_product_offer_str


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    categories = None
    category = None
    categories_all = Category.objects.all()
    product_offers = Offer.objects.filter(display_in_banner=True)
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
    product_sizes = Size.objects.filter(category=product.category)
    product_types = Type.objects.filter(category=product.category)
    product_prices = Price.objects.filter(product=product)

    # Build dictionary of sizes and prices for the product
    product_price_dict = {}
    for priceobj in product_prices:
        product_price_dict[priceobj.get_size()] = priceobj.get_price()

    product_offers = Offer.objects.filter(display_in_banner=True)
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

    coffee_details = Coffee.objects.filter(product=product).first()

    if coffee_details:
        context['coffee_detail'] = coffee_details

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a new product """

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.save()
            if new_product.category.name == 'Coffee':
                coffee_form = CoffeeForm(request.POST)
                if coffee_form.is_valid():
                    new_coffee = coffee_form.save(commit=False)
                    new_coffee.product = new_product
                    new_coffee.save()
                else:
                    messages.error(request, 'Failed to add Coffee details. Please check product form.')

            # Add prices to database for new product
            # using default prices stored in Size model
            product_sizes = Size.objects.filter(category=new_product.category)
            for product_size in product_sizes:
                product_sku = (
                    new_product.category.name.upper() + "-" +
                    new_product.name.upper() + "-" +
                    product_size.size)
                product_sku = ''.join(filter(None, product_sku.split(' ')))
                new_price = Price(
                    product=new_product, price=product_size.default_price,
                    size=product_size, sku=product_sku)
                new_price.save()

            friendly_name = request.POST.get('friendly_name', '')
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


def edit_product(request, product_id):
    """ Add an existing product """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_form = ProductForm(
            request.POST, request.FILES, instance=product)
        coffee_update = False
        product_update = False
        if product_form.is_valid():
            product_form.save()
            product_update = True
            if product.category.name == "Coffee":
                coffee = get_object_or_404(Coffee, product=product)
                coffee_form = CoffeeForm(request.POST, instance=coffee)
                if coffee_form.is_valid():
                    coffee_form.save()
                    coffee_update = True
                else:
                    messages.error(
                        request, 'Failed to update Coffee details. Please check product form.')

            if product_update and coffee_update:
                messages.success
                (request, f'Succesfully updated product and coffee details for {product.friendly_name}!')
            elif product_update:
                messages.success(
                    request, f'Succesfully updated product details for {product.friendly_name}!')

            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request, 'Failed to update product. Please check product form.')

    product_form = ProductForm(instance=product)
    coffee_form = None
    if product.category.name == "Coffee":
        coffee = get_object_or_404(Coffee, product=product)
        coffee_form = CoffeeForm(instance=coffee)


    categories_all = Category.objects.all()
    template = "products/edit_product.html"
    context = {
        'product': product,
        'product_form': product_form,
        'coffee_form': coffee_form,
        'categories_all': categories_all,
        'on_admin_page': True,
    }
    return render(request, template, context)

