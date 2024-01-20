from django.urls import path
from .views import (news_detail,
                    news_list,
                    HomePageViwe,
                    ContactPageView,
                    pageNotView,
                    aboutPageView,
                    LocalNewsView,
                    ForeignNewsView,
                    TechnologyNewsView,
                    SportNewsView,
                    getAllCategory)

urlpatterns = [
    path('', HomePageViwe.as_view(), name='home_page'),
    path("news/", news_list, name="all_news_list"),
    path("news/<slug:news>/", news_detail, name="news_detail_page"),
    path("contact-us/", ContactPageView.as_view(), name="contact_page"),
    path("404/", pageNotView, name="page_not_found"),
    path("about/", aboutPageView, name="about_page"),
    path('local-news/', LocalNewsView.as_view(), name="local_news_page"),
    path('foreign/', ForeignNewsView.as_view(), name="foreign_news_page"),
    path('technology/', TechnologyNewsView.as_view(), name="technology_news_page"),
    path('sport/', SportNewsView.as_view(), name="sport_news_page"),
    path('categoryall/', getAllCategory, name="categoryall_page"),

]




