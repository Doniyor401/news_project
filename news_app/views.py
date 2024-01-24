from urllib import request
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from .models import News, Category
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import ContactForm, CommentForm
from django.http import HttpResponse
from config.custom_permissions import OnlyLoggedSuperUser
from hitcount.models import HitCount
from hitcount.views import HitCountMixin, HitCountDetailView
from hitcount.utils import get_hitcount_model


# Create your views here.


@login_required
def news_list(request):
    # news_list = News.objects.filter(status=News.Status.Published)
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }
    return render(request, "news/news_list.html", context=context)
# class NewsListView(ListView):
#     template_name = "news/news_list.html"
#
#     def get(self, request):
#         news_list = News.published.all()
#         context = {
#             "news_list": news_list
#         }
#         return render(request, self.template_name, context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    #hitcount logic - ya'ni nechta odam korganini qilish eng tepada from qib olingani joylari bor
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi comment obyektini yaratamiz lk malumotlar bazasiga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # coment egasini sorov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            new_comment.save()
            # bu kod bilan commenti yuborganimizdan song coment yozadigan joyni tozalab qoysak boladi. Oxirgi yozganimiz turmidi shunda
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        "news": news,
        "comments": comments,
        "comment_count": comment_count,
        "new_comment": new_comment,
        "comment_form": comment_form,
    }

    return render(request, "news/news_detail.html", context)





# class NewsDetailView(DetailView):
#     template_name = "news/news_detail.html"
#
#     def get(self, request, id):
#         news = get_object_or_404(News, id=id, status=News.Status.Published)
#         context = {
#             "news": news
#         }
#         return render(request, self.template_name, context)


# @login_required
# def homePageView(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-publish_time')[:5]
#     local_one = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:1]
#     local_news = News.published.all().filter(category__name="Mahalliy")[1:6]
#     context = {
#         "news_list": news_list,
#         "categories": categories,
#         "local_news": local_news,
#         "local_one": local_one,
#     }
#     return render(request, "news/home.html", context)
class HomePageView(ListView):
    model = News
    template_name = "news/home.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['mahalliy_xabarlar'] = News.published.filter(category__name="Mahalliy").order_by('-publish_time')[:5]
        context['xorij_xabarlari'] = News.published.filter(category__name="Xorij").order_by('-publish_time')[:5]
        context['sport_xabarlari'] = News.published.filter(category__name="Sport").order_by('-publish_time')[:5]
        context['texnologiya_xabarlar'] = News.published.filter(category__name="Texnologiya").order_by('-publish_time')[:5]
        # context['local_news'] = News.published.all().filter(category__name="Mahalliy")[1:6]
        return context


# @login_required
# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur</h2>")
#     context = {
#         "form": form
#     }
#     return render(request, "news/contact.html", context)

class ContactPageView(TemplateView):
    template_name = "news/contact.html"

    def get(self, request,  *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2> Biz bilan bog'langaninigz uchun tashakkur! </h2>")
        context = {
            "form": form
        }
        return render(request, "news/contact.html", context)


def aboutPageView(request):
    context = {

    }
    return render(request, "news/about.html")


@login_required
def pageNotView(request):
    context = {

    }
    return render(request, "news/404.html")


class LocalNewsView(ListView):
    model = News
    template_name = "news/mahaliy.html"
    context_object_name = "mahalliy_yangiliklar"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Mahalliy")
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = "news/xorij.html"
    context_object_name = "xorij_yangiliklar"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Xorij")
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = "news/texnologiya.html"
    context_object_name = "texnologik_yangiliklar"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Texnologiya")
        return news


class SportNewsView(ListView):
    model = News
    template_name = "news/sport.html"
    context_object_name = "sport_yangiliklar"

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="Sport")
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = News
    template_name = 'crud/news_cread.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')


     # bundan oldingi classda onsonro yoli bol 1 ta .py faylda yozilib xammasiga inherit qilingani OnlyLoggedSuperUser db yozilgani
    def test_func(self):
        return self.request.user.is_superuser


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_user = User.objects.filter(is_superuser=True)

    context = {
        'admin_user': admin_user
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

