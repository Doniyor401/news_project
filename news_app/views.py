from urllib import request

from django.shortcuts import render, get_object_or_404, Http404
from .models import News, Category
from django.views.generic import ListView, DetailView, TemplateView
from .forms import ContactForm
from django.http import HttpResponse
# Create your views here.


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

    context = {
        "news": news
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
class HomePageViwe(ListView):
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


def getAllCategory(request):
    cat = Category.objects.all()

    context = {
        "category": cat
    }
    return context