from django.urls import path

from .views import (AdsListView, AdCreateView, AdEditView,
                    RepliesListView, ReplyDeleteView, reply_approve_view,
                    ad_detail_view, AdsListByCategoryView, subscribe, unsubscribe)

urlpatterns = [
    path('', AdsListView.as_view(), name='ads_list'),
    path('<int:pk>', ad_detail_view, name='adv_detail'),
    path('create/', AdCreateView.as_view(), name='adv_create'),
    path('<int:pk>/edit/', AdEditView.as_view(), name='adv_edit'),
    path('replies/', RepliesListView.as_view(), name='replies_list'),
    path('replies/<int:pk>/approve/', reply_approve_view, name='reply_approve'),
    path('replies/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
    path('category/<int:pk>', AdsListByCategoryView.as_view(), name='category_list'),
    path('category/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('category/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe')
]