from django.urls import path
from . import views
from .views import(
  HouseDetailView, HousingListView
)

app_name = 'house'

urlpatterns = [
  path('list_house/', HousingListView.as_view(), name='list_house'),
  path('post_house_comments/<int:pk>', views.post_house_comments, name='post_house_comments'), 
  path('detail_house/<int:pk>', HouseDetailView.as_view(), name='detail_house'), 
]