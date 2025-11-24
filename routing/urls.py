from django.urls import path
from .views import RouteView

urlpatterns = [
    path('plan-route/', RouteView.as_view(), name='plan_route'),
]
