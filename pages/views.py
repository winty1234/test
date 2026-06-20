from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .form import RegisterForm, ApplicationForm, ReviewForm
from .models import Application


def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, "form.html", context={
        'form': form,
        "heading": "Регистрация",
        "submit_text": "Зарегестрироваться",
        "extra_link": "login",
        "extra_link_text": "Уже есть аккаунт? Войти"
    })


@login_required
def application_create(request: HttpRequest):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    return render(request, "form.html", context={
            "form": form,
            "heading": "Создать заявку",
            "submit_text": "Создать"
        })

@login_required
def review(request: HttpRequest, application_id: int):
    application = get_object_or_404(Application, pk=application_id, user=request.user)

    # Отзыв можно оставить только после смены статуса заявки администратором
    if application.status == Application.Status.NEW:
        return redirect("dashboard")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.application = application
            review.save()
            return redirect("dashboard")
    else:
        form = ReviewForm()

    return render(request, "form.html", context={
        "form": form,
        "heading": "Оставить отзыв",
        "submit_text": "Отправить",
    })


class DashboardView(LoginRequiredMixin, ListView):
    model = Application
    paginate_by = 2
    template_name = "dashboard.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_obj = context.get('page_obj')

        if page_obj:
            print(dir(page_obj))

        return context