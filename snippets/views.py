from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm

from snippets.models import Snippet
from snippets.tasks import sendEmailInSnippetCreation

def is_snippet_owner_test(snippet_id, user):    
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        return snippet.user == user
    except Snippet.DoesNotExist:
        return False


class SnippetAdd(LoginRequiredMixin, CreateView):
#    TODO: Implement this class to handle snippet creation, only for authenticated users.
    model = Snippet
    fields = [
        "name",
        "description",
        "snippet",
        "language",
        "public"
    ]
    template_name= "snippets/snippet_add.html"
    login_url = "/login/"

    def get_success_url(self):
        return f'/snippets/snippet/{self.object.pk}/'    

    def form_valid(self, form):
        # Usually we don´t set the in fronentd app, we have to take it from the request
        user = self.request.user
        snippet = form.save(commit=False)
        snippet.user = user
        snippet.save()

        # sends email after snippet creation using celery
        sendEmailInSnippetCreation.delay_on_commit(
            snippet.name,
            snippet.description,
            snippet.user.email,
            )
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        kwargs = {
            **kwargs,
            "action": "Crear"
        }
        return super().get_context_data(**kwargs)        
        

class SnippetEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#    TODO: Implement this class to handle snippet editing. Allow editing only for the owner.
    
    login_url = "/login/"
    model = Snippet
    fields = fields = [
        "name",
        "description",
        "snippet",
        "language",
        "public"
    ]
    template_name= "snippets/snippet_add.html"

    def get_success_url(self):
        return f'/snippets/snippet/{self.object.pk}/'
    
    def test_func(self):
        snippet_id = self.kwargs.get("pk")
        return is_snippet_owner_test(snippet_id, self.request.user)
    
    def get_context_data(self, **kwargs):
        kwargs = {
            **kwargs,
            "action": "Editar"
        }
        return super().get_context_data(**kwargs)


class SnippetDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#    TODO: Implement this class to handle snippet deletion. Allow deletion only for the owner.
    model = Snippet
    success_url = "/"
    login_url = "/login/"

    def test_func(self):
        snippet_id = self.kwargs.get("pk")
        return is_snippet_owner_test(snippet_id, self.request.user)


class SnippetDetails(UserPassesTestMixin, DetailView):
    model = Snippet
    login_url = "/login/"
    template_name= "snippets/snippet.html"
    raise_exception = True
    
    # if the user is not the owner of the snippet we can not see it
    def test_func(self):
        snippet_id = self.kwargs.get("pk")
        try:
            snippet = Snippet.objects.get(id=snippet_id)            
            return snippet.public or self.request.user == snippet.user            
        except Snippet.DoesNotExist:
            return False

class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        # TODO: Fetch user snippets based on username and public/private logic
        # snippets = Snippet.objects.filter(...)

        snippets = Snippet.objects.filter(
            user__username=username
        )
        if username!=request.user.username:
            snippets = snippets.filter(public=True)

        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )  # Placeholder


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        snippets = Snippet.objects.filter(
            language__slug=language,
            public=True
        )
        return render(request, "index.html", {"snippets": snippets})  # Placeholder


# could be a better implementation
#class Login(auth_views.LoginView):
#    template_name= "login.html"
#    next_page= "index"

class Login(View):
    #TODO: Implement login view logic with AuthenticationForm and login handling.    
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return HttpResponseRedirect("/")
        form = AuthenticationForm({})     
        return render(request, "login.html", {"form":form})
    
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():            
            auth_login(request, form.get_user())
            return HttpResponseRedirect("/")
        return render(request, "login.html", {"form":form})


# could be a better implementation
#class Logout(auth_views.LogoutView):
#    template_name= "logout.html"
#    next_page= "index"
        
class Logout(View):

    def get(self, request, *args, **kwargs):
        return render(request, "logout.html")

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        return HttpResponseRedirect("/")
    

class Index(View):
    def get(self, request, *args, **kwargs):
        # TODO: Fetch and display all public snippets
        snippets = Snippet.objects.filter(
            public = True
        )
        return render(request, "index.html", {"snippets": snippets})  # Placeholder
