"""
Products application views module
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Category, Price, Product, Size, Type, Coffee, Offer, Review
from profiles.models import Reward

from .forms import CoffeeForm, ProductForm, PriceForm, ReviewForm
from .helpers import get_product_offer_str


def all_products(request):
    """ A view to show all products """
    # Get all Products
    products = Product.objects.filter(discontinued=False)
    query = None
    categories = None
    category = None
    # Get all Categories
    categories_all = Category.objects.all()
    # Get Offers to be dislayed in banner
    product_offers = Offer.objects.filter(display_in_banner=True)
    # Return Offer string
    product_offer_str = get_product_offer_str(product_offers, "  -  ")
    if request.GET:
        # If Category specified
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            # Get Products filtered by Category
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            category = categories[0]
        # If query specified
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                # Error message
                messages.error(request, "Please enter search criteria!")
                # Redirect to all products
                return redirect(reverse('products'))
            queries = Q(name__icontains=query) | Q(
                description_short__icontains=query)
            # Get Products filtered by query
            products = products.filter(queries)
            # Check if any Products match query
            if (len(products)) == 0:
                # Warning message
                messages.warning(
                    request, "Your search didn't return any products.")
                # Redirect to all products
                return redirect(reverse('products'))
    # Sort Products by name
    products = products.order_by("name")
    # Set context
    context = {
        'products': products,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'search_term': query,
        'category': category,
        'categories_all': categories_all,
    }
    # Render product page
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    # Get Product
    product = get_object_or_404(Product, pk=product_id)

    # Get Categories
    categories_all = Category.objects.all()
    # Get Product Category
    product_category = get_object_or_404(Category, name=product.category)
    # Get Product Sizes
    product_sizes = Size.objects.filter(category=product.category)
    # Get Product Types
    product_types = Type.objects.filter(category=product.category)
    # Get Product Prices
    product_prices = Price.objects.filter(product=product)
    # Get Product Reviews
    product_reviews = Review.objects.filter(
        product=product).order_by("-rating")[:10]
    user_review = None
    # If user is authenticated, get User Review
    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            product=product, user=request.user).first()

    # Build dictionary of sizes and prices for the product
    product_price_dict = {}
    for priceobj in product_prices:
        product_price_dict[priceobj.get_size()] = priceobj.get_price()

    # Get Offers to display in banner
    product_offers = Offer.objects.filter(display_in_banner=True)
    # Get Offer string
    product_offer_str = get_product_offer_str(product_offers, "  -  ")
    # Set context
    context = {
        'product': product,
        'product_category': product_category,
        'product_sizes': product_sizes,
        'product_types': product_types,
        'product_prices': product_prices,
        'product_price_dict': product_price_dict,
        'product_reviews': product_reviews,
        'user_review': user_review,
        'product_offers': product_offers,
        'product_offer_str': product_offer_str,
        'categories_all': categories_all,
    }
    # Get Coffee details
    coffee_details = Coffee.objects.filter(product=product).first()
    # If Product is a Coffee
    if coffee_details:
        # Add Coffee details to context
        context['coffee_detail'] = coffee_details
    # Render Product detail page
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a new product """
    # If user is not a superuser
    if not request.user.is_superuser:
        # Error message
        messages.error(
            request,
            'Sorry, only store adminitrators can do that.',
            extra_tags='admin'
        )
        # Redirect to all Products
        return redirect(reverse('products'))

    if request.method == 'POST':
        # Instantiate ProductForm from POST and FILES data
        product_form = ProductForm(request.POST, request.FILES)
        # If form is valid
        if product_form.is_valid():
            # Create new Product object
            new_product = product_form.save(commit=False)
            new_product.save()
            addstr = "Product"
            # If new Product is a Coffee
            if new_product.category.name == 'Coffee':
                # Instantiate CoffeeForm from POST data
                coffee_form = CoffeeForm(request.POST)
                # If form is valid
                if coffee_form.is_valid():
                    # Create new Cofee object
                    new_coffee = coffee_form.save(commit=False)
                    new_coffee.product = new_product
                    new_coffee.save()
                    addstr = addstr + ", coffee details"
                else:
                    # Error message
                    messages.error(
                        request,
                        'Failed to add Coffee details. \
                            Please check product form.',
                        extra_tags='admin'
                    )

            # Add prices to database for new product
            # using default prices stored in Size model
            # Get Sizes
            product_sizes = Size.objects.filter(category=new_product.category)
            # Loop through Product Sizes
            for product_size in product_sizes:
                # Get Category name
                cname = new_product.category.name.upper()
                # Get Product name
                pname = new_product.name.upper()
                # Get Product Size
                psize = product_size.size
                # Set SKU
                product_sku = (cname + "-" + pname + "-" + psize)
                product_sku = ''.join(filter(None, product_sku.split(' ')))
                # Create new Price object
                new_price = Price(
                    product=new_product, price=product_size.default_price,
                    size=product_size, sku=product_sku)
                new_price.save()
            addstr = addstr + " and prices"
            # Success message
            messages.success(
                request,
                f'{addstr} added: {new_product.friendly_name}.',
                extra_tags='admin'
            )
            # Redirect to Product detail
            return redirect(reverse('product_detail', args=[new_product.id]))
        # Error message
        else:
            messages.error(
                request,
                'Failed to add product. Please check product form.',
                extra_tags='admin'
            )
    else:
        # Instantiate blank ProductForm
        product_form = ProductForm
        # Instantiate blank CoffeeForm
        coffee_form = CoffeeForm

    # Get all Categories
    categories_all = Category.objects.all()
    # Set template
    template = "products/add_product.html"
    # Set context
    context = {
        'product_form': product_form,
        'coffee_form': coffee_form,
        'categories_all': categories_all,
    }
    # Render add product page
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit an existing product """
    # If user is not a superuser
    if not request.user.is_superuser:
        # Error message
        messages.error(
            request,
            'Sorry, only store adminitrators can do that.',
            extra_tags='admin'
        )
        # Redirect to all products
        return redirect(reverse('products'))
    # Get Product object
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Instantiate ProductForm from POST and Files data and Product object
        product_form = ProductForm(
            request.POST, request.FILES, instance=product)
        # If form is valid
        if product_form.is_valid():
            # Save Product
            product_form.save()
            updatestr = "Product "
            # If Product is a Coffee
            if product.category.name == "Coffee":
                # Get Coffee object
                coffee = get_object_or_404(Coffee, product=product)
                # Instantiate CoffeeForm from POST data and COffee Object
                coffee_form = CoffeeForm(request.POST, instance=coffee)
                # If form is valid
                if coffee_form.is_valid():
                    # Save Coffee object
                    coffee_form.save()
                    updatestr = updatestr + "and coffee details "
                else:
                    # Error message
                    messages.error(
                        request,
                        'Failed to update coffee details. \
                            Please check product form.',
                        extra_tags='admin'
                    )
            # Success message
            messages.success(
                request,
                f'{updatestr}updated: {product.friendly_name}.',
                extra_tags='admin'
            )
            # Redirect to Product detail page
            return redirect(
                reverse('product_detail', args=[product.id])
            )
        # Error message
        else:
            messages.error(
                request,
                'Failed to update product. Please check product form.',
                extra_tags='admin'
            )
    # Instantiate ProductForm from Product object
    product_form = ProductForm(instance=product)
    coffee_form = None
    # If Product os a Coffee
    if product.category.name == "Coffee":
        # Get Coffee object
        coffee = get_object_or_404(Coffee, product=product)
        # Instantiate CoffeeForm from Coffee object
        coffee_form = CoffeeForm(instance=coffee)
    # Get all Categories
    categories_all = Category.objects.all()
    # Set template
    template = "products/edit_product.html"
    # Set context
    context = {
        'product': product,
        'product_form': product_form,
        'coffee_form': coffee_form,
        'categories_all': categories_all,
    }
    # Render Product edit page
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete an existing product """
    # If user is not a superuser
    if not request.user.is_superuser:
        # Error message
        messages.error(
            request,
            'Sorry, only store administrators can do that.',
            extra_tags='admin'
        )
        # Redirect to all Products
        return redirect(reverse('products'))

    # Get Product object
    product = get_object_or_404(Product, pk=product_id)
    deleteflag = False
    # If Product exists
    if product:
        deletestr = "Product"
        deleteflag = True
    # If Product is a Coffee
    if product.category.name == "Coffee":
        # Get Coffee object linked to Product
        coffee = Coffee.objects.filter(product=product)
        # If Coffee exists
        if coffee:
            deletestr = deletestr + ", coffee details"
            # Delete Coffee
            coffee.delete()
            deleteflag = True
    # Get Price objects linked to Product
    prices = Price.objects.filter(product=product)
    # If Prices exist
    if prices:
        deletestr = deletestr + ", prices "
        # Delete Prices
        prices.delete()
    # Get Review objects linked to Product
    reviews = Review.objects.filter(product=product)
    # If Reviews exist
    if reviews:
        deletestr = deletestr + ", reviews"
        # Delete Reviews
        reviews.delete()

    if deleteflag:
        # Success message
        messages.success(
            request,
            f'{deletestr} deleted: {product.friendly_name}.',
            extra_tags='admin'
        )
        # Delete Product
        product.delete()
    else:
        # Error message
        messages.error(
            request,
            f'Error - product {product.friendly_name} not found in database!',
            extra_tags='admin'
        )
    # Redirect to all Products
    return redirect(reverse('products'))


@login_required
def edit_prices(request, product_id):
    """ Edit existing prices """

    # If user is not a superuser
    if not request.user.is_superuser:
        # Error message
        messages.error(
            request, 'Sorry, only store administrators can do that.'
        )
        # Redirect to all Products
        return redirect(reverse('products'))
    # Get Product object
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # Instantiate PriceForm based on POST data
        price_form = PriceForm(request.POST)
        # If form is valid
        if price_form.is_valid():
            # Get Size and new Price from cleaned form data
            size = price_form.cleaned_data.get('size')
            new_price = price_form.cleaned_data.get('price')
            # Update Price object
            priceobj = get_object_or_404(Price, product=product, size=size)
            priceobj.price = new_price
            priceobj.save()
            # Success message
            messages.success(
                request,
                f'Price updated: {product.friendly_name}.',
                extra_tags='admin'
            )
            # Redirect to Product detail
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Return error message
            messages.error(
                request,
                'Failed to update Price. Please check price form.',
                extra_tags='admin'
            )

    # Instantiate PriceForm based on Product object
    price_form = PriceForm(instance=Product)
    # Get first Size
    first_size = Size.objects.filter(category=product.category).first()
    # Set size field in form to first size
    price_form.fields['size'].initial = first_size
    # Get first Price
    first_price = Price.objects.filter(
        product=product, size=first_size).first()
    # Set price field in form to first Price
    price_form.fields['price'].initial = first_price.price
    # Get all Categories
    categories_all = Category.objects.all()
    # Build dictionary of sizes and prices for the product
    product_prices = Price.objects.filter(product=product)
    product_price_dict = {}
    for priceobj in product_prices:
        product_price_dict[priceobj.get_size()] = priceobj.get_price()
    # Set template
    template = "products/edit_prices.html"
    # Set context
    context = {
        'product': product,
        'price_form': price_form,
        'categories_all': categories_all,
        'product_price_dict': product_price_dict,
    }
    # Render edit Prices page
    return render(request, template, context)


@login_required
def review_product(request, product_id):
    """ Review a Product """

    # Get Product object
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Get User Review for Product
        product_review = Review.objects.filter(
            product=product, user=request.user).first()
        # If Review exists
        if product_review:
            new_review = False
            # Instantiate ReviewForm from POST data and review object
            review_form = ReviewForm(request.POST, instance=product_review)
        else:
            new_review = True
            # Instantiate ReviewForm from POST data
            review_form = ReviewForm(request.POST)
        # If form is valid
        if review_form.is_valid():
            # If Review is new
            if new_review:
                # Create Review object
                review = review_form.save(commit=False)
                # Set Product
                review.product = product
                # Set User
                review.user = request.user
                # Save review
                review.save()
                # Get review offer if it exists and apply it to Reward
                review_offer = Offer.objects.filter(
                    description="Review").first()
                if review_offer:
                    # Get User Reward
                    reward = Reward.objects.filter(user=request.user).first()
                    # If Reward exists
                    if reward:
                        # Set discount
                        reward.discount = review_offer.discount
                        reward.save()
                        discount = round(review_offer.discount, 0)
                        rewardstr = f'Thanks for being a great customer - \
                            you have earned {discount}% \
                            off your next order!'
                    else:
                        # Create reward object
                        reward = Reward(
                            user=request.user,
                            discount=review_offer.discount)
                        reward.save()
                        rewardstr = ""
                # Success message
                messages.success(
                    request,
                    f'Review added for product: {product.friendly_name}.\
                    {rewardstr}',
                    extra_tags='admin'
                )
            else:
                # Update Review
                review_form.save()
                # Success messsage
                messages.success(
                    request,
                    f'Review updated for product: {product.friendly_name}.',
                    extra_tags='admin'
                )
            # Redirect to Product detial page
            return redirect(reverse('product_detail', args=[product.id]))

        else:
            # If rating not set
            if not review_form['rating'].value():
                # Error message
                messages.error(
                    request,
                    'Error - please rate product to add review.',
                    extra_tags='admin'
                )
            else:
                # Error message
                messages.error(
                    request,
                    'Failed to add or edit review. Please check review form.',
                    extra_tags='admin'
                )

    else:
        # Get Review object
        product_review = Review.objects.filter(
            product=product, user=request.user).first()
        # If Review exists
        if product_review:
            # Instatiate ReviewForm from Review object
            review_form = ReviewForm(instance=product_review)
        else:
            # Instatiate blank ReviewForm
            review_form = ReviewForm
    from_profile = False
    # Get referer
    referer = (request.META.get('HTTP_REFERER', '/'))
    # Set from_profile if referred from Profile page
    if referer:
        rarray = referer.split('/')
        if rarray:
            rarray.reverse()
            if len(rarray) > 1:
                if rarray[1] == "profile":
                    from_profile = True
    # Get all Categories
    categories_all = Category.objects.all()
    # set semplate
    template = "products/review_product.html"
    # Set context
    context = {
        'product': product,
        'product_review': product_review,
        'review_form': review_form,
        'categories_all': categories_all,
        'from_profile': from_profile
    }
    # Render Product review page
    return render(request, template, context)


@login_required
def delete_review(request, product_id, user_id):
    """ Delete an existing Review """
    # Get Product object
    product = get_object_or_404(Product, pk=product_id)
    # Get User object
    user = get_object_or_404(User, pk=user_id)
    # Get Review object for Product and User
    review = get_object_or_404(Review, product=product, user=user)
    # If user is not a superuser
    if not request.user.is_superuser:
        # Error message
        messages.error(
            request,
            'Sorry, only store administrators can do that.',
            extra_tags='admin'
        )
        # Redirect to Product detail page
        return redirect(reverse('product_detail', args=[product.id]))
    # Delete Rdview
    review.delete()
    # Success message
    messages.success(
        request,
        f'User { user.username} review deleted for product: \
            {product.friendly_name}.',
        extra_tags='admin'
    )
    # Redirect to Product detail page
    return redirect(reverse('product_detail', args=[product.id]))


@login_required
def review_product_all(request):
    """
    Review all products - redirects user to view all products
    """
    # Redirect to all Products
    return redirect(reverse('products'))
