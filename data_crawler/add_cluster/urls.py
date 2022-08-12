from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
#from add_cluster. views import dcrawler

urlpatterns = [

    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='add_cluster/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='add_cluster/logout.html'), name="logout"),
    #path('add_cluster/', views.searchcluster),
    path('Createclusterapi', views.save_cluster, name="save_cluster"),
    path('add_cluster/', views.insert_clusters, name="add_cluster"),
    path('search', views.search, name="search"),
    path('new_url', views.new_url, name="new_url"),
    #path('search_result', views.search_result),
    #path('add_cluster/',views.storedata, name="storedata"),
    #path('add_cluster/', views.searchresult),
    #path('add_cluster/', dcrawler.as_view())
]