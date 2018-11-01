from . import models


class TextProviderBackend:

    def get_text(self, identifier):
        text_instance = models.Text.objects.filter(pk=identifier).first()
        if text_instance:
            return text_instance.text
        else:
            return None
