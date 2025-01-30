from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import BlogSerializer
from django.shortcuts import get_object_or_404
from .models import Blog

class BlogsView(APIView):
    def post(self, request):
        serialized_blog = BlogSerializer(data=request.data)
        if serialized_blog.is_valid():
            serialized_blog.save()
            return Response(serialized_blog.data, status=status.HTTP_200_OK)
        return Response(serialized_blog.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        blog_id = self.kwargs['id']
        blog = get_object_or_404(Blog, id=blog_id)
        serialized_blog = BlogSerializer(blog, data=request.data, partial=True)  
        if serialized_blog.is_valid():
            serialized_blog.save()   
            return Response(serialized_blog.data, status=status.HTTP_200_OK)
        return Response(serialized_blog.errors, status=status.HTTP_400_BAD_REQUEST)
    
