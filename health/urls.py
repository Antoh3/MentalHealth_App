from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = 'health'



urlpatterns = [
    path('',views.home_view, name='home'),
    path('patient_home/',views.patient_redirect_home, name='patient_home'),
    path('login/',views.login_view, name="login"),
    path('patient_signup/',views.patient_signup_view, name="patient_signup"),
    path('counselor_signup/',views.counselor_signup_view, name="counselor_signup"),
    path('counselor_login/',views.counselor_login_view, name="counselor_login"),

    path("chat_with_ai/", views.chatbot_redirect, name="chat_with_ai"),



    path('patient_list/',views.patient_list, name="patient_list"),
    path('session_details/<int:id>',views.session_details, name="session_details"),
    path('patient_session_details/<int:id>',views.patient_session_details, name="patient_session_details"),
    path('patient_new_session/',views.new_session, name="patient_new_session"),
    path('patient_book_session/',views.book_session, name="patient_book_session"),
    path('patient_remarks/<int:id>',views.patient_appintment_remark, name="patient_remarks"),
    path('recommend_user/<int:id>',views.recommenduser, name="recommend_user"),
    path('view_session/',views.view_session, name="view_session"),
    path('all_sessions/',views.all_sessions_data, name="all_sessions"),
    path('all_patient_sessions/',views.all_patient_session_data, name="all_patient_sessions"),
    path('completed_sessions/',views.completed_sessions, name="completed_sessions"),
    path('cancelled_sessions/',views.canceled_sessions, name="cancelled_sessions"),
    path('approved_sessions/',views.approved_sessions, name="approved_sessions"),
    path('search_sessions/',views.user_search_sessions, name="search_sessions"),
    path('patient_search_sessions/',views.patient_search_sessions, name="patient_search_sessions"),
    path('profile/',views.profile, name="profile"),

    path("counselor_home/", views.counselor_home, name="counselor_home"),
    path("chat/<str:user_type>/<int:user_id>/<int:receiver_id>/", views.chat_page, name="chat_view"),
    path("counselor_chat/<str:user_type>/<int:user_id>/<int:receiver_id>/", views.chat_page, name="chat_view"),
    path("long-poll-messages/<str:user_type>/<int:user_id>/", views.long_poll_messages, name="long_poll_messages"),
    path("send-message/", views.send_message, name="send_message"),
    path("get-messages/<str:user_type>/<int:user_id>/", views.get_messages, name="get_messages"),

    path('comm/',views.comm_view, name="comm"),
    path('videos/',views.videos_view, name="videos"),
    path('books/',views.books_view, name="books"),
    path('test11/',views.test, name="test11")
]
#