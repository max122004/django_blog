from django.urls import path

from article import views

urlpatterns = [
    path('', views.ArticleListView.as_view()),
    path('<int:pk>/', views.ArticleDetailView.as_view()),
    path('create/', views.ArticleCreateView.as_view()),
    path('<int:pk>/update/', views.ArticleUpdateView.as_view()),
    path('<int:pk>/delete/', views.ArticleDestroyView.as_view()),
    path('category/', views.CategoryListView.as_view()),
    path('comment/create/', views.CommentCreateView.as_view()),
    path('<int:pk>/comment/update/', views.CommentUpdateView.as_view()),
    path('<int:pk>/comment/delete/', views.CommentDeleteView.as_view()),
    path('like/create/', views.LikeCreateView.as_view()),
    path('liked/', views.LikedArticleAPIView.as_view()),
    path('share/create/', views.ShareCreateView.as_view())
]