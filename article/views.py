from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from article.models import Article, Category, Comment, Like, Share
from article.serializer import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateSerializer, \
    ArticleUpdateSerializer, ArticleDestroySerializer, CategoryListSerializer, \
    CommentCreateSerializer, CommentUpdateSerializer, LikeSerializer, ShareSerializer, CommentDestroySerializer
from permissin import ArticleCreatePermission, IsAuthorOrReadOnly


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer

    def get(self, request, *args, **kwargs):
        article_category = request.GET.get('category', None)
        if article_category:
            self.queryset = self.queryset.filter(
                category__name__icontains=article_category
            )

        article_name = request.GET.get('name', None)
        if article_name:
            self.queryset = self.queryset.filter(
                title__icontains=article_name
            )

        article_text = request.GET.get('text', None)
        if article_text:
            self.queryset = self.queryset.filter(
                text__icontains=article_text
            )

        return super().get(request, *args, **kwargs)


class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create_like(self, article):
        # Создаем сериализатор для объекта лайка, используя данные из запроса
        serializer_like = LikeSerializer(data=self.request.data)
        # Проверяем, что данные валидны
        serializer_like.is_valid(raise_exception=True)
        # Сохраняем лайк, связывая его с пользователем и статьей
        serializer_like.save(user=self.request.user, article=article)

        serializer_share = ShareSerializer(data=self.request.data)
        serializer_share.is_valid(raise_exception=True)
        serializer_share.save(user=self.request.user, article=article)


    def get(self, request, *args, **kwargs):
        # Вызываем метод get() суперкласса для получения статьи
        response = super().get(request, *args, **kwargs)
        # Получаем объект статьи
        article = self.get_object()
        # Получаем все лайки, связанные со статьей
        likes = article.likes.all()
        shares = article.shares.all()
        # Создаем сериализатор для списка лайков
        like_serializer = LikeSerializer(likes, many=True)
        share_serializer = ShareSerializer(shares, many=True)
        # Получаем данные статьи, используя сериализатор для детального представления
        response_data = self.serializer_class(article).data
        # Добавляем данные о лайках в объект ответа
        response_data['likes'] = like_serializer.data
        response_data['shares'] = share_serializer.data
        # Возвращаем объект ответа, содержащий данные о статье и ее лайках
        return Response(response_data)


class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated, ArticleCreatePermission]

    def perform_create(self, serializer):
        # Получаем изображение из request.FILES
        image = self.request.FILES.get('image')
        serializer.save(image=image)


class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class ArticleDestroyView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDestroySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]


class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDestroySerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.request.data.get('article')
        article = Article.objects.get(id=article_id)
        serializer.save(
            user=self.request.user,
            article=article
        )


class ShareCreateView(CreateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.request.data.get('article')
        article = Article.objects.get(id=article_id)
        serializer.save(
            user=self.request.user,
            article=article
        )


class LikedArticleAPIView(ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        liked_articles = Article.objects.filter(likes__user=self.request.user)
        serializer = self.serializer_class(liked_articles, many=True)
        return Response(serializer.data)

