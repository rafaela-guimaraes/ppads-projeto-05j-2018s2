from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('create_entry/', views.CreateEntry.as_view(), name='create_entry'),
    path('update_entry/<int:pk>', views.UpdateEntry.as_view(), name='update_entry'),
    path('list_entry/', views.ListEntry.as_view(), name='list_entry'),
    path('entries_statement/', views.EntriesStatement.as_view(), name='entries_statement'),
    path('entries_by_category/', views.EntriesByCategory.as_view(), name='entries_by_category'),
    path('delete/<int:pk>/', views.DeleteEntry.as_view(), name='delete_entry'),
]