from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Entrypoint(APIView):
    def get(self, request):
        """
        Display a welcome message.

        Returns:
        --------
        response:
            - success: Response (Rest Framework) containing a welcome message
        """

        return Response({"message": "Welcome to Restosaurus' Server 🚀"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Echo the request body.

        Returns:
        --------
        response:
            - success: Response (Rest Framework) containing the request body
        """

        return Response(request.data, status=status.HTTP_204_NO_CONTENT)
