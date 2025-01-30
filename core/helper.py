from rest_framework.response import Response
from rest_framework import status

def create_response(success: bool, message: str, data=None, http_status=status.HTTP_200_OK):
    return Response(
        {
            "success": success,
            "message": message,
            "data": data,
        },
        status=http_status,
    )
