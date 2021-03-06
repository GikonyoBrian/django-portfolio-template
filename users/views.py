import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views import View
from users import models
from users.forms import UpdateProfileForm 

User = get_user_model()

class Landing(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/dashboard/overview")
        else:
            return render(request, 'landing.html', {"url": settings.DOMAIN_URL})

class UserPortfolio(View):
    def get(self, request, username):
        return render(request, 'portfolio.html', {})

class Login(View):
    def post(self, request):
        email_or_username = request.POST.get("email_or_username")
        password = request.POST.get("password")
        try:
            user_obj = User.objects.get(email=email_or_username)
            user = authenticate(request, username=user_obj.email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "status": "login_success",
                    "url": settings.DOMAIN_URL + "/dashboard/overview"
                })
            else:
                return JsonResponse({
                    "status": "login_error",
                    "message": "Email or password was incorrect."
                })
        except User.DoesNotExist:
            try:
                user_obj = User.objects.get(username=email_or_username)
                user = authenticate(request, username=user_obj.email, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        "status": "login_success",
                        "url": settings.DOMAIN_URL + "/dashboard/overview"
                    })
                else:
                    return JsonResponse({
                        "status": "login_error",
                        "message": "Email or password was incorrect."
                    })
            except User.DoesNotExist:
                return JsonResponse({
                        "status": "login_error",
                        "message": "Email or password was incorrect."
                    })

class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You were logged out successfully.")
        return redirect("/")

class Dashboard(View):
    def get(self, request):
        return render(request, 'dashboard.html', {"page": "home", "title": "Home - Portfolio Dash"})

class Skills(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        skills = user.profile.skills.all()
        return render(request, 'dashboard.html', {"page": "skills", "skills": skills, "title": "Skills - Portfolio Dash"})

class Quotes(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        quotes = user.profile.quotes.all()
        return render(request, 'dashboard.html', {"page": "quotes", "quotes": quotes, "title": "Quotes - Portfolio Dash"})

class Projects(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        projects = user.profile.projects.all()
        return render(request, 'dashboard.html', {"page": "projects", "projects": projects, "title": "Projects - Portfolio Dash"})

class Interests(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        interests = user.profile.interests.all()
        return render(request, 'dashboard.html', {"page": "interests", "interests": interests, "title": "Interests - Portfolio Dash"})

class FunFacts(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        fun_facts = user.profile.fun_facts.all()
        return render(request, 'dashboard.html', {"page": "fun_facts", "fun_facts": fun_facts, "title": "Fun Facts - Portfolio Dash"})

class Repositories(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        repositories = user.profile.repositories.all()
        return render(request, 'dashboard.html', {"page": "repositories", "repositories": repositories, "title": "Repositories - Portfolio Dash"})

class Socials(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        socials = user.profile.socials.all()
        return render(request, 'dashboard.html', {"page": "socials", "socials": socials, "title": "Socials - Portfolio Dash"})

class Articles(View):
    def get(self, request):
        email = request.user
        user = User.objects.get(email=email)
        articles = user.profile.articles.all()
        return render(request, 'dashboard.html', {"page": "articles", "articles": articles, "title": "Articles - Portfolio Dash"})

class AddItem(View):
    def post(self, request):
        page = request.POST.get("page")
        email = request.user
        user = User.objects.get(email=email)
        if page == "skills":
            name = request.POST.get("name")
            percentage = request.POST.get("percentage")
            skill = models.Skills.objects.create(name=name, percentage=percentage)
            user.profile.skills.add(skill)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "quotes":
            quote = request.POST.get("quote")
            quoter = request.POST.get("quoter")
            quote = models.Quotes.objects.create(quote=quote, quoter=quoter)
            user.profile.quotes.add(quote)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "projects":
            name = request.POST.get("name")
            site = request.POST.get("site")
            url = request.POST.get("url")
            project = models.Projects.objects.create(name=name, site=site, url=url)
            user.profile.projects.add(project)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "interests":
            name = request.POST.get("name")
            interest = models.Interests.objects.create(name=name)
            user.profile.interests.add(interest)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "fun_facts":
            fact = request.POST.get("fact")
            who_by = request.POST.get("by_who")
            fun_fact = models.FunFacts.objects.create(fact=fact, who_by=who_by)
            user.profile.fun_facts.add(fun_fact)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "repositories":
            repository_name = request.POST.get("repository_name")
            site = request.POST.get("site")
            url = request.POST.get("url")
            repo = models.Repositories.objects.create(repository_name=repository_name, site=site, url=url)
            user.profile.repositories.add(repo)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "socials":
            name = request.POST.get("name")
            site = request.POST.get("site")
            url = request.POST.get("url")
            social = models.Social.objects.create(name=name, site=site, url=url)
            user.profile.socials.add(social)
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "articles":
            title = request.POST.get("title")
            url = request.POST.get("url")
            article = models.Articles.objects.create(title=title, url=url)
            user.profile.articles.add(article)
            user.save()
            return JsonResponse({
                "status": "success",
            })

class DeleteItem(View):
    def post(self, request):
        page = request.POST.get("page")
        item_id = request.POST.get("id")
        email = request.user
        user = User.objects.get(email=email)
        if page == "skills":
            skill = models.Skills.objects.get(pk=item_id)
            user.profile.skills.remove(skill)
            skill.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "quotes":
            quote = models.Quotes.objects.get(pk=item_id)
            user.profile.quotes.remove(quote)
            quote.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "projects":
            project = models.Projects.objects.get(pk=item_id)
            user.profile.projects.remove(project)
            project.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "interests":
            interest = models.Interests.objects.get(pk=item_id)
            user.profile.interests.remove(interest)
            interest.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "fun_facts":
            fun_fact = models.FunFacts.objects.get(pk=item_id)
            user.profile.fun_facts.remove(fun_fact)
            fun_fact.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "repositories":
            repo = models.Repositories.objects.get(pk=item_id)
            user.profile.repositories.remove(repo)
            repo.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "socials":
            social = models.Social.objects.get(pk=item_id)
            user.profile.socials.remove(social)
            social.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })
        elif page == "articles":
            article = models.Articles.objects.get(pk=item_id)
            user.profile.articles.remove(article)
            article.delete()
            user.save()
            return JsonResponse({
                "status": "success",
            })

class GetProfile(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        return render(request, 'profile.html', {"title": user.get_full_name() + " - Portfolio Dash"})

class UpdateProfile(View):
    def post(self, request, username):
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile_no = request.POST.get("mobile_no")
        secondary_email = request.POST.get("secondary_email")
        secondary_mobile_no = request.POST.get("secondary_mobile_no")
        bio = request.POST.get("bio")
        date_of_birth = datetime.datetime.strptime(request.POST.get("date_of_birth"),'%Y-%m-%d')
        try:
            user = User.objects.get(username=username)
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.email = email
            user.save()
            updated_form = UpdateProfileForm({
                "secondary_email": secondary_email,
                "mobile_no": mobile_no,
                "secondary_mobile_no": secondary_mobile_no,
                "bio": bio,
                "date_of_birth": date_of_birth, 
                },
                request.FILES, instance=user.profile)
            if updated_form.is_valid():
                updated_form.save()
                return  JsonResponse({
                    "status": "success",
                    "url": user.profile.profile_picture.url
                })
            else:
                return  JsonResponse({
                    "status": "error",
                })
        except User.DoesNotExist:
            return  JsonResponse({
                "status": "error",
            })