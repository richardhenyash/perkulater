from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import UserForm, UserProfileForm


def profile(request):
    """
    Display the signed in user's profile
    """
    user_profile = get_object_or_404(UserProfile, user=request.user)
    userobj = User.objects.get(username=request.user)
    print(userobj)
    print(userobj.first_name)

    user_profile_form = UserProfileForm(instance=user_profile)
    user_form = UserForm(instance=userobj)
    orders = user_profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'orders': orders,
    }
    return render(request, template, context)
