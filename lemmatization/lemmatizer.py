from .models import lookup_form
from .morpheus import morpheus

from vocab_list.models import VocabularyList


"""
Just test examples for now.
"""

print("est", lookup_form("est"), morpheus("est", "lat"))

# est set() ['edo1', 'sum1']

print("ἤρχοντο", lookup_form("ἤρχοντο"), morpheus("ἤρχοντο", "grc"))

# ἤρχοντο {'ἄρχω', 'ἔρχομαι'} ['ἄρχω', 'ἔρχομαι']

text = """Καὶ τῇ ἡμέρᾳ τῇ τρίτῃ γάμος ἐγένετο ἐν Κανὰ τῆς Γαλιλαίας"""

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

text = """ἐξῆλθον ἐκ τῆς πόλεως καὶ ἤρχοντο πρὸς αὐτόν"""

for token in text.split():
    print(token, lookup_form(token), morpheus(token, "grc"))

# ἐξῆλθον {'ἐξέρχομαι'} ['ἐξέρχομαι']
# ἐκ {'ἐκ'} ['ἐκ']
# τῆς {'ὁ'} ['ὁ']
# πόλεως {'πόλις'} ['πόλις']
# καὶ {'καί'} ['καί']
# ἤρχοντο {'ἔρχομαι', 'ἄρχω'} ['ἄρχω', 'ἔρχομαι']
# πρὸς {'πρός'} ['πρός']
# αὐτόν {'αὐτός'} ['αὐτός']

gnt80 = VocabularyList.objects.get(pk=1)

entry = gnt80.entries.get(lemma="ἄρχω")
print(entry.lemma, entry.gloss)

# ἄρχω I reign, rule

entry = gnt80.entries.get(lemma="ἔρχομαι")
print(entry.lemma, entry.gloss)

# ἔρχομαι I come, go


# TODO: hook all this up to the lemma lattices
