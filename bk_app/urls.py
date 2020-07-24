from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.do_login, name='login'),
    path('stock/', views.stock, name='stock'),
    path('deals/', views.deals, name='deals'),
    path('menu/', views.menu, name='menu'),
    path('orders/', views.orders, name='orders'),

    path('do_logout/', views.do_logout, name='do_logout'),

    path('add_stock_item/', views.add_stock_item, name='add_stock_item'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('add_deal/', views.add_deal, name='add_deal'),
    path('add_deal_item/<str:pk>/', views.add_deal_item, name='add_deal_item'),
    path('add_order/', views.add_order, name='add_order'),

    path('view_deal/<str:pk>/', views.view_deal, name='view_deal'),
    path('view_order/<str:pk>/', views.view_order, name='view_order'),
]
