from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Category, Price, Product, Size, Type, Coffee, Offer
from .forms import CoffeeForm, ProductForm, PriceForm
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


@login_required
def add_product(request):
    """ Add a new product """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store adminitrators can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.save()
            addstr = "Product "
            if new_product.category.name == 'Coffee':
                coffee_form = CoffeeForm(request.POST)
                if coffee_form.is_valid():
                    new_coffee = coffee_form.save(commit=False)
                    new_coffee.product = new_product
                    new_coffee.save()
                    addstr = addstr + ", coffee details "
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
            addstr = addstr + "and prices "

            messages.success(
                request, f'{addstr}added: {new_product.friendly_name}.')
            return redirect(reverse('product_detail', args=[new_product.id]))
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


@login_required
def edit_product(request, product_id):
    """ Edit an existing product """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store adminitrators can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product_form = ProductForm(
            request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            updatestr = "Product "

            if product.category.name == "Coffee":
                coffee = get_object_or_404(Coffee, product=product)
                coffee_form = CoffeeForm(request.POST, instance=coffee)
                if coffee_form.is_valid():
                    coffee_form.save()
                    updatestr = updatestr + "and coffee details "
                else:
                    messages.error(
                        request, 'Failed to update coffee details. Please check product form.')

            messages.success(
                request, f'{updatestr}updated: {product.friendly_name}.')
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

@login_required
def delete_product(request, product_id):
    """ Delete an existing product """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store administrators can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    deleteflag = False
    if product:
        deletestr = "Product "
        deleteflag = True
    if product.category.name == "Coffee":
        coffee = Coffee.objects.filter(product=product)
        if coffee:
            deletestr = deletestr + ", coffee details "
            coffee.delete()
            deleteflag = True
    prices = Price.objects.filter(product=product)
    if prices:
        deletestr = deletestr + "and prices "
        prices.delete()
    if deleteflag:
        messages.success(
            request, f'{deletestr}deleted: {product.friendly_name}.')
        product.delete()
    else:
        messages.error(request, f'Error - product {product.friendly_name} not found in database!')

    return redirect(reverse('products'))


@login_required
def edit_prices(request, product_id):
    """ Edit existing prices """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store administrators can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        price_form = PriceForm(request.POST)
        if price_form.is_valid():
            size = price_form.cleaned_data.get('size')
            new_price = price_form.cleaned_data.get('price')
            priceobj = get_object_or_404(Price, product=product, size=size)
            priceobj.price = new_price
            priceobj.save()
            messages.success(
                request, f'Price updated: {product.friendly_name}.')
        else:
            messages.error(
                request, 'Failed to update Price. Please check price form.')
        
        return redirect(reverse('product_detail', args=[product.id]))

    price_form = PriceForm(instance=Product)
    first_size = Size.objects.filter(category=product.category).first()
    price_form.fields['size'].initial = first_size
    first_price = Price.objects.filter(product=product, size=first_size).first()
    price_form.fields['price'].initial = first_price.price
    categories_all = Category.objects.all()
    # Build dictionary of sizes and prices for the product
    product_prices = Price.objects.filter(product=product)
    product_price_dict = {}
    for priceobj in product_prices:
        product_price_dict[priceobj.get_size()] = priceobj.get_price()

    template = "products/edit_prices.html"
    context = {
        'product': product,
        'price_form': price_form,
        'categories_all': categories_all,
        'product_price_dict': product_price_dict,
        'on_admin_page': True,
    }
    return render(request, template, context)
