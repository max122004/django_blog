from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from authentication.models import User


class ArticleDetailPermission(BasePermission):
    message = 'Adding vacancies for non ht user not allowed.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class ArticleCreatePermission(BasePermission):
    message = 'Adding vacancies for non ht user not allowed.'

    def has_permission(self, request, view):
        if request.user.role == User.HR:
            return True
        else:
            return False


class IsAuthorOrReadOnly(BasePermission):
    """
    Проверка на автора статьи
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user