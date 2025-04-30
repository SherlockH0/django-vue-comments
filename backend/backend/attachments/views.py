from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UploadSerializer


class UploadAttachmentView(APIView):
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser,)

    def put(self, request: Request, format=None) -> Response:
        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attachment = serializer.save()
        return Response(status=201, data={"id": attachment.pk})
