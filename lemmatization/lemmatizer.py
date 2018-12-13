from .models import lookup_form
from .morpheus import morpheus

"""
Just test examples for now.
"""

print("est", lookup_form("est"), morpheus("est", "lat"))

# est set() ['edo1', 'sum1']

print("ἤρχοντο", lookup_form("ἤρχοντο"), morpheus("ἤρχοντο", "grc"))

# ἤρχοντο {'ἄρχω', 'ἔρχομαι'} ['ἄρχω', 'ἔρχομαι']

text = """
Καὶ τῇ ἡμέρᾳ τῇ τρίτῃ γάμος ἐγένετο ἐν Κανὰ τῆς Γαλιλαίας
"""

for token in text.split():
    print(token, lookup_form(token), morpheus(token, "grc"))

# Καὶ {'καί'} ['καί']
# τῇ {'ὁ'} ['ὁ', 'τῇ']
# ἡμέρᾳ {'ἡμέρα'} ['ἥμερος', 'ἡμέρα']
# τῇ {'ὁ'} ['ὁ', 'τῇ']
# τρίτῃ {'τρίτος'} ['τρίτος']
# γάμος {'γάμος'} ['γάμος']
# ἐγένετο {'γίνομαι'} ['γίγνομαι']
# ἐν {'ἐν'} ['ἐν', 'εἰς']
# Κανὰ {'Κανά'} []
# τῆς {'ὁ'} ['ὁ']
# Γαλιλαίας {'Γαλιλαία'} []

# TODO: hook this up to the lemma lattices
