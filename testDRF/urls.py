from django.urls import path
from .views import recipients_list
from views import recipients_detail
from views import product_sets_list
from views import product_sets_detail

urlpatterns = [
    path('recipients/', recipients_list, name='recipients_list'),
    path('recipients/<int:pk>', recipients_detail, name='recipients_detail'),
    path('product-sets/', product_sets_list, name='product-sets_list'),
    path('product-sets/<int:pk>', product_sets_detail, name='product-sets_detail'),

]
