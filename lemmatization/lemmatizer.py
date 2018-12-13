from .models import lookup_form
from .morpheus import morpheus


text = """
Καὶ τῇ ἡμέρᾳ τῇ τρίτῃ γάμος ἐγένετο ἐν Κανὰ τῆς Γαλιλαίας
"""


for token in text.split():
    print(token, lookup_form(token), morpheus(token, "grc"))
