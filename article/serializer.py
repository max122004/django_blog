from rest_framework import serializers

from article.models import Article, Category, Comment, Like, Share


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['title', 'image', 'created']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created']


# вот это необходимо разобрать
class ArticleDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    shares_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'author', 'category', 'comments', 'image', 'likes_count', 'shares_count']

    def get_likes_count(self, obj):
        # В данном случае obj будет представлять одну конкретную статью
        # (экземпляр модели Article), для которой нужно подсчитать
        # количество лайков.
        return obj.likes.count()

    def get_shares_count(self, obj):
        return obj.shares.count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all()
    )

    class Meta:
        model = Like
        fields = ['user', 'article', 'created']


class ShareSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all()
    )

    class Meta:
        model = Share
        fields = ['user', 'article', 'created']


class ArticleCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'text', 'category', 'image')

    def create(self, validated_data):
        article = Article.objects.create(**validated_data)
        return article


class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'text', 'author', 'image']

    def save(self):
        article = super().save()
        article.save()
        return article


class ArticleDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id']


class CategoryListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validate_data):
        comments = Comment.objects.create(**validate_data)
        comments.save()
        return comments


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['text']

    def save(self):
        comment = super().save()
        comment.save()
        return comment


class CommentDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id']

