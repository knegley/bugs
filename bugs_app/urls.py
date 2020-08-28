from django.urls import path
from bugs_app import views
urlpatterns = [
    path('', views.home_view, name="home"),
    path("status/<str:status>/<int:ticket_id>/", views.status_view),
    path("ticket/<int:ticket_id>/ticket/<str:ticket_author>/",
         views.author_view, name="author"),
    path("ticket/<int:ticket_id>/edit/", views.edit_ticket_view),
    path("ticket/<int:ticket_id>/", views.ticket_detailed_view, name="ticket"),
    path("addticket/", views.add_ticket_view, name="add_ticket"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
