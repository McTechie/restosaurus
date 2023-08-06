from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Entrypoint(APIView):
    permission_classes = ()
    def get(self, request):
        """
        Display a welcome message.

        Returns:
        --------
        response:
            - success: Response (Rest Framework) containing a welcome message
        """

        return Response({"message": "Welcome to Restosaurus' Server 🚀"}, status=status.HTTP_200_OK)
