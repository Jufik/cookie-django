from rest_framework import (
    mixins,
    viewsets,
    permissions
)

from .models import User
from .serializers import UserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filter_fields = ['id']
    # filter_class = UserFilter
    # search_fields = []
    # ordering_fields = []

    def get_queryset(self, *args, **kwargs):
        return super(UserViewSet, self).get_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(UserViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        return super(UserViewSet, self).perform_create(serializer)
