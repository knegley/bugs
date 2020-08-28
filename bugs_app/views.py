from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.decorators import login_required
from bugs_app.forms import LogInForm, AddTicketForm, EditTicketForm
from django.contrib.auth import login, logout, authenticate
from bugs_app.models import Ticket

# Create your views here.


def home_view(request):
    user = request.user
    tickets = Ticket.objects.all() or None
    # name = request.user.get_full_name() or None
    if tickets is not None:
        tickets = [ticket for ticket in tickets]
        new_tickets = [
            ticket for ticket in tickets if ticket.ticket_status == "New"] or None
        done_tickets = [
            ticket for ticket in tickets if ticket.ticket_status == "Done"] or None
        in_progress_tickets = [
            ticket for ticket in tickets if ticket.ticket_status == "In_Progress"] or None
        invalid_tickets = [
            ticket for ticket in tickets if ticket.ticket_status == "Invalid"] or None
        return render(request, "home.html", {"user": user, "tickets": tickets,
                                             "new_tickets": new_tickets,
                                             "invalid_tickets": invalid_tickets,
                                             "in_progress_tickets":
                                             in_progress_tickets,
                                             "done_tickets": done_tickets})
    return render(request, "home.html")


def login_view(request):
    form = LogInForm()
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=username, password=password)
            # breakpoint()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("home"))
    return render(request, "login.html", {"form": form})


@ login_required
def add_ticket_view(request):
    form = AddTicketForm()
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # breakpoint()
            title = data.get("title")
            description = data.get("description")
            user_filed = request.user.get_full_name()
            ticket_status = "New"
            user_assigned = None
            user_completed = None
            Ticket.objects.create(title=title, description=description,
                                  user_filed=user_filed,
                                  user_assigned=user_assigned,
                                  user_completed=user_completed,
                                  ticket_status=ticket_status,
                                  author=request.user)
            return HttpResponseRedirect(reverse("home"))
            # breakpoint()

            # print(data)
    return render(request, "add_ticket.html", {"form": form})


@ login_required
def ticket_detailed_view(request, ticket_id):
    ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detailed.html", {"ticket": ticket})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@ login_required
def edit_ticket_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    initial_data = {"title": ticket.title, "description": ticket.description}
    form = AddTicketForm(initial=initial_data)
    # breakpoint()
    if request.user.is_superuser:
        initial_data = {"title": ticket.title, "time": ticket.time,
                        "user_assigned": ticket.user_assigned,
                        "description": ticket.description,
                        "user_filed": ticket.user_filed,
                        "user_completed": ticket.user_completed,
                        "ticket_status": ticket.ticket_status}
        form = EditTicketForm(initial=initial_data)

        if request.method == "POST":
            form = EditTicketForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                title = data.get("title")
                description = data.get("description")
                user_assigned = data.get("user_assigned")
                ticket_status = data.get("ticket_status")
                user_comleted = data.get("user_completed")

                if ticket_status == "In_Progress":
                    ticket.ticket_status = ticket_status
                    ticket.description = description
                    ticket.user_assigned = user_assigned
                    ticket.user_completed = None
                    ticket.title = title
                    ticket.save()
                # breakpoint()

                elif ticket_status == "Done":
                    ticket.ticket_status = ticket_status
                    ticket.description = description
                    ticket.user_assigned = None
                    ticket.user_completed = user_comleted
                    ticket.title = title
                    ticket.save()

                elif ticket_status == "Invalid":
                    ticket.ticket_status = ticket_status
                    ticket.description = description
                    ticket.user_assigned = None
                    ticket.user_completed = None
                    ticket.title = title
                    ticket.save()
                else:
                    pass

                return HttpResponseRedirect(redirect_to=reverse("ticket", args=[ticket_id]))
                # return render(request, "ticket_detailed_view.html", {"ticket": ticket})

    elif request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data.get("title")
            description = data.get("description")
            ticket.title = data.get("title")

            ticket.save()
            print(data)
            # breakpoint()

        return HttpResponseRedirect(redirect_to=reverse("ticket", args=[ticket_id]))
        # return HttpResponseRedirect(redirect_to=f"ticket/{ticket_id}")
    else:
        pass

    return render(request, "add_ticket.html", {"form": form})


def author_view(request, ticket_author, ticket_id):
    name = ticket_author
    # print(ticket_author)
    # print(ticket_author)

    # for ticket in Ticket.objects.all():
    #     print(ticket.user_filed)

    # x = Ticket.objects.filter(id=ticket_id).first()
    # print(x.author.get_full_name())
    # print(x.user_filed)
    # print(x)
    # breakpoint()

    tickets_by_author = [ticket.title for ticket in Ticket.objects.all(
    ) if ticket.user_filed == ticket_author]

    in_progress_tickets = [ticket.title for ticket in Ticket.objects.all(
    ) if ticket.ticket_status == "In_Progress"]

    completed = [ticket.title for ticket in Ticket.objects.all()
                 if ticket.ticket_status == "Done" and ticket.user_completed == ticket_author]
    assigned = [ticket.title for ticket in Ticket.objects.all()
                if ticket.user_assigned == ticket_author]
    print(assigned)

    print(tickets_by_author)
    return render(request, "author_ticket_view.html",
                  {"name": name, "tickets": tickets_by_author,
                   "completed": completed, "in_progress": in_progress_tickets,
                   "assigned": assigned})
