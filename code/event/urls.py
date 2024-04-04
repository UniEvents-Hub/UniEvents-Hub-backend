from django.urls import path
from .views import EventListCreateAPIView, EventRetrieveAPIView, EventListAPIView, EventUpdateAPIView, UserEventRetrieveAPIView, TicketCreateAPIView,UserTicketAPIView
from .views import SavedCreateAPIView,UserSavedAPIView,UserUnsaveAPIView

urlpatterns = [
    path('eventcreate/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('eventslist/', EventListAPIView.as_view(), name='event-list'),
    path('specificevent/', EventRetrieveAPIView.as_view(), name='event-detail'),
    path('userspecificevent/', UserEventRetrieveAPIView.as_view(), name='event-detail'),   
    path('eventupdate/<int:pk>/', EventUpdateAPIView.as_view(), name='event-update'),
    path('buyticket/', TicketCreateAPIView.as_view(), name="buy-ticket"),
    path('getticket/', UserTicketAPIView.as_view(), name="get-ticket"),
    path('eventsave/', SavedCreateAPIView.as_view(), name="save-event"),
    path('getsaved/', UserSavedAPIView.as_view(), name="user-saved"),
    path('eventunsave/<int:pk>/', UserUnsaveAPIView.as_view(), name="unsave-event")       
]
