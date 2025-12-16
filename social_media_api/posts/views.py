from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Comment, Like
from notifications.models import Notification
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # get the list of users the current user is following
        following_users = self.request.user.following.all()

        # filter posts where the author is in that list
        # order by created_at descending (newest first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        # Automatically assign the logged-in user as the author
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        # Create Notification
        post = comment.post
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb="commented on your post",
                target=comment
            )


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        # check if already liked
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create Notification (only if not liking your own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        # try to delete the like
        deleted_count, _ = Like.objects.filter(user=request.user, post=post).delete()

        if deleted_count == 0:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)
