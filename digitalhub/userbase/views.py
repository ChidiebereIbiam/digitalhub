from django.shortcuts import render, redirect
from digitalhub.authentication.forms import UserEditForm
from .forms import CompanyForm
from .models import Company
from django.contrib.auth.decorators import login_required

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


def subscription(request):
    pass


def invoices(request):
    pass


def payment_method(request):
    pass
