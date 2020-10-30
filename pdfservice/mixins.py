import io

from django.http import FileResponse

from .utils import generate_pdf


class PDFResponseMixin:
    """
    Renders a template to a PDF file.
    """
    filename = "export.pdf"

    # If True, renders PDF in the browser
    inline = False

    # Command-line options to pass to the PDF service
    # http://pdf-service-a.us1.eldarioncloud.com/#endpoint-render
    cmd_options = {}

    # IF True, the absolute static paths replace relative static paths
    fix_static_paths = True

    def get_cmd_options(self):
        return self.cmd_options

    def get_filename(self):
        return self.filename

    def generate_pdf(self, context, params):
        resp = generate_pdf(
            self.template_name,
            context,
            params,
            self.request,
            fix_static_paths=self.fix_static_paths
        )
        # stream response
        return io.BytesIO(resp.content)

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a PDF response with a template rendered with the given context.
        """
        filename = response_kwargs.pop("filename", None)
        cmd_options = response_kwargs.pop("cmd_options", None)

        if self.request.GET.get("as", "pdf") == "html":
            return super().render_to_response(context, **response_kwargs)

        if filename is None:
            filename = self.get_filename()

        if cmd_options is None:
            cmd_options = self.get_cmd_options()

        content = self.generate_pdf(context, params=cmd_options)
        response = FileResponse(
            content,
            as_attachment=not self.inline,
            filename=filename,
            **response_kwargs
        )
        return response
