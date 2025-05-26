from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ResourceView(APIView):
    # permission_classes = []  # No permissions required for this example

    def get(self, request):
        """
        Example GET endpoint that returns a simple message.
        """
        print(getattr(request, 'user', None))  # Debugging line to check user
        return Response({"message": "This is a protected resource."}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Example POST endpoint that echoes back the received data.
        """
        data = request.data
        return Response({"received_data": data}, status=status.HTTP_201_CREATED)
