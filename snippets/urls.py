from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),    
    path("login/", views.Login.as_view(), name="login"),
    #path("logout/", views.Logout.as_view(
    #    next_page= "login"
    #), name="logout"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path(
        "snippets/lang/<slug:language>/",
        views.SnippetsByLanguage.as_view(),
        name="language",
    ),
    path(
        "snippets/user/<slug:username>/",
        views.UserSnippets.as_view(),
        name="user_snippets",
    ),
    path("snippets/snippet/<int:pk>/", views.SnippetDetails.as_view(), name="snippet"),
    path("snippets/add/", views.SnippetAdd.as_view(), name="snippet_add"),
    path("snippets/edit/<int:pk>/", views.SnippetEdit.as_view(), name="snippet_edit"),
    path(
        "snippets/delete/<int:pk>/",
        views.SnippetDelete.as_view(),
        name="snippet_delete",
    ),
]
