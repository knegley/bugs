from django.urls import path
from bugs_app import views
urlpatterns = [
    path('', views.home_view, name="home"),
    path("ticket/<int:ticket_id>/edit", views.edit_ticket_view),
    path("ticket/<int:ticket_id>/", views.ticket_detailed_view, name="ticket"),
    path("add_ticket/", views.add_ticket_view, name="add_ticket"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
