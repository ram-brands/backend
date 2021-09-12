from logging import getLogger

from rest_framework.decorators import api_view

from core.responses import AttachmentHttpResponse, HttpResponse

from .models import Run

logger = getLogger(__name__)


@api_view(["GET"])
def input_file(request, pk):
    run = Run.objects.get(pk=pk)
    return AttachmentHttpResponse(content=run.input_file, name=run.input_name)


@api_view(["GET"])
def output_file(request, pk):
    run = Run.objects.get(pk=pk)
    return AttachmentHttpResponse(content=run.output_file, name="output.zip")


@api_view(["POST"])
def confirmation(request, pk):
    run = Run.objects.get(pk=pk)
    run.status = request.data["status"]
    run.save()
    return HttpResponse()
