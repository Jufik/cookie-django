from rest_framework import (
    mixins,
    viewsets,
    permissions,
    filters
)
from django_filters.rest_framework import DjangoFilterBackend

from vqapps.mediamanager.permissions import IsAuthorOrReadOnly
from vqapps.mediamanager.serializers import MediaSerializer
from vqapps.mediamanager.models import Media


class MediaViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  # mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Media.objects.select_related('author').all()
    ordering = ['-created']
    serializer_class = MediaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ['product']
    # filter_class = MediaFilter
    # search_fields = []
    # ordering_fields = []

    def get_queryset(self, *args, **kwargs):
        return super(MediaViewSet, self).get_queryset(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(MediaViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(MediaViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(MediaViewSet, self).create(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return super(MediaViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(MediaViewSet, self).destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)