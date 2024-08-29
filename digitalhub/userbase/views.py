from django.shortcuts import render, redirect
from digitalhub.authentication.forms import UserEditForm, ProfilePictureForm
from .forms import CompanyForm
from .models import Company
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from digitalhub.payment.models import Subscription, Invoice, PaymentMethod
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


@login_required
def edit_profile(request):
    user = request.user
    
    try:
        company = user.company
    except Company.DoesNotExist:
        company = None

    if request.method == "POST":
        user_edit_form = UserEditForm(request.POST, instance=user)
        company_form = CompanyForm(request.POST, instance=company)

        if user_edit_form.is_valid() and company_form.is_valid():
            user_edit_form.save()
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            return redirect("edit_profile")
    else:
        user_edit_form = UserEditForm(instance=user)
        company_form = CompanyForm(instance=company)

    return render(
        request,
        "userbase/edit_profile.html",
        {"user_edit_form": user_edit_form, "company_form": company_form},
    )


@login_required
def user_change_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            profile_image = form.cleaned_data['profile_image']
            user_profile = request.user
            user_profile.profile_image = profile_image
            user_profile.save()

            return JsonResponse({'status': 'success', 'message': 'Profile picture updated successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


def subscription(request):
    subscription_list = Subscription.objects.filter(user=request.user)
    
    paginator = Paginator(subscription_list, 10)
    page = request.GET.get('page')
    
    try:
        subscriptions = paginator.page(page)
    except PageNotAnInteger:
        subscriptions = paginator.page(1)
    except EmptyPage:
        subscriptions = paginator.page(paginator.num_pages)
    
    return render(request, 'userbase/subscription.html', {"subscriptions": subscriptions, "paginator": paginator})


def invoice(request):
    invoice_list = Invoice.objects.filter(user=request.user)
    
    paginator = Paginator(invoice_list, 10)
    page = request.GET.get('page')
    
    try:
        invoices = paginator.page(page)
    except PageNotAnInteger:
        invoices = paginator.page(1)
    except EmptyPage:
        invoices = paginator.page(paginator.num_pages)
    
    return render(request, 'userbase/invoice.html', {"invoices": invoices, "paginator": paginator})



def payment_method(request):
    pass
