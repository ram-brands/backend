from rest_framework.decorators import api_view

from core.responses import AttachmentHttpResponse

from .models import Run


@api_view(["GET"])
def input_file(request, pk):
    run = Run.objects.get(pk=pk)
    return AttachmentHttpResponse(content=run.input_file, name=run.input_name)


@api_view(["GET"])
def output_file(request, pk):
    run = Run.objects.get(pk=pk)
    return AttachmentHttpResponse(data=run.output_file, name="output.zip")
