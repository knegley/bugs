from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from bugs_app.forms import LogInForm, AddTicketForm
from django.contrib.auth import login, logout, authenticate
from bugs_app.models import Ticket, CustomUser
# Create your views here.


@login_required
def home_view(request):
    user = request.user
    tickets = Ticket.objects.all() or None
    return render(request, "home.html", {"user": user, "tickets": tickets})


def login_view(request):
    form = LogInForm()
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
    return render(request, "login.html", {"form": form})


@login_required
def add_ticket_view(request):
    form = AddTicketForm()
    if request.method == "POST":
        form = LogInForm(request.Post)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            breakpoint()
    return render(request, "add_ticket.html", {"form": form})


@login_required
def ticket_detailed_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detailed.html", {"ticket": ticket})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def edit_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    initial_data = {"title": ticket.title, "time": ticket.time,
                    "description": ticket.description,
                    "user_filed": ticket.user_filed,
                    "user_completed": ticket.user_completed,
                    "ticket_status": ticket.ticket_status,
                    "author": ticket.author}
    form = AddTicketForm(initial=initial_data)

    print(ticket)
    if request.method == "POST":
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            breakpoint()
        return HttpResponseRedirect(redirect_to=f"ticket/{ticket_id}")
    return render(request, "add_ticket", {"form": form})
