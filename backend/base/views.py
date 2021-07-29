from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ProtectedDataView(GenericAPIView):
    """Return protected data main page."""

    authentication_classes = ()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = {"data": "THIS IS THE PROTECTED STRING FROM SERVER"}

        return Response(data, status=status.HTTP_200_OK)
