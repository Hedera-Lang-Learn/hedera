import json
from html.parser import HTMLParser
from io import StringIO

from lemmatization.lemmatizer import Lemmatizer


class EditedTextHtmlParser(HTMLParser):

    def __init__(self, token_lemma_dict=None, lang=None):
        self.current_tag = None
        self.current_attrs = {}
        self.current_data = ""
        self.lemmatized_text_data = []
        self.token_lemma_dict = token_lemma_dict
        self.lemmatizer = Lemmatizer(lang)
        self.initial = ""
        return super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            self.current_tag = "span"
            """
            Note: the fed in data could be two different types from a tuple of (key, dict) or (key, bool)
            handle_endtag() will require a key:value pair containing either of the structure below:
                [('data-token', '{"glossed": "glossed-automatic", "initial": "", "lemma_id": 1372, "resolved": "resolved-automatic", "gloss_ids": [84128, 68154], "word_normalized": "Arma"}')]
                [('follower', 'true')]
            """
            key, value = attrs[0]
            if key in "follower":
                self.current_attrs = {key: value}
            else:
                self.current_attrs = json.loads(value)

    def handle_endtag(self, tag):
        # Add new initial if self.initial is set
        if len(self.lemmatized_text_data) == 1 and self.initial:
            lemmatized_text_data_initial = self.lemmatized_text_data[0]["initial"]
            if lemmatized_text_data_initial != self.initial:
                lemmatized_text_data_initial = self.initial
                # Reset self.initial
                self.initial = ""
        if "follower" in self.current_attrs:
            self.separate_true_followers(self.current_data)
        #Note: sometimes the current_tag/self.current_attrs will be empty/None when there is a newline/break
        elif self.current_data is not None and self.current_tag is not None:
            self.lemmatized_text_data.append(
                {
                    **self.current_attrs,
                    "word": self.current_data,
                    "following": "",
                }
            )
        self.current_tag = None
        self.current_attrs = {}
        self.current_data = ""

    def handle_data(self, data):
        if ("follower" in self.current_attrs):
            self.current_data = data
        else:
            try:
                if(
                    (self.current_tag is None) or
                    (self.current_tag == "span" and self.current_attrs == {}) or
                    (self.current_attrs["lemma_id"] not in self.token_lemma_dict[data])
                ):
                    self.lemmatize_chunk(data)
                else:
                    self.current_data = data
            except KeyError:
                self.lemmatize_chunk(data)

    def separate_true_followers(self, follower):
        """
        Takes the contents of a span where 'follower' is true.
        Splits any 'follower' characters from alpha numeric characters.
        Sets the 'following' attr on the previous data point with true followers
        and sends new alpha numeric string to be lemmatized.
        Returns None
        """
        followers = []
        text = []
        for idx, ch in enumerate(follower):
            if ch.isalnum():
                text = follower[idx:]
                break
            followers.append(ch)

        if len(self.lemmatized_text_data) > 0:
            self.lemmatized_text_data[-1]["following"] += "".join(followers)
        else:
            # this will only occur if the text begins with a "follower"
            self.lemmatized_text_data.append(
                {
                    "word": "",
                    "lemma_id": None,
                    "resolved": True,
                    "word_normalized": "",
                    "following": "".join(followers)
                }
            )
        if(len(text) > 0):
            self.lemmatize_chunk("".join(text))

    def lemmatize_chunk(self, chunk):
        """
        Takes an unrecognized chunk of text.
        Sends 'chunk' to be lemmatized, then extends the data with the returned content.
        Checks if chunk does not contain return and newline "\r\n" - only add tokens if it the chunk is not a return/newline
        **Fixes problem with empty tokens**
        Returns None
        """
        self.current_data = None
        # lemmatized_text_data_length = len(self.lemmatized_text_data)
        new_data = self.lemmatizer.lemmatize(chunk)
        if "\r\n" not in chunk:
            self.lemmatized_text_data.extend(new_data)
        elif "\r\n" in chunk and len(self.lemmatized_text_data):
            following = self.lemmatized_text_data[-1]["following"]
            token_lemma_dict_keys = list(self.token_lemma_dict.keys())
            prev_lemma_id = self.lemmatized_text_data[-1]["lemma_id"]
            #Note: Added check if we have reached the end of the data array because theres a bug where new lines are added after each edit
            if prev_lemma_id not in self.token_lemma_dict[token_lemma_dict_keys[-1]]:
                self.lemmatized_text_data[-1]["following"] = f"{following}{chunk}"
        # EDGE CASE: Newlines/breaks that may happen at the very beginning of the text
        # Pull out beginning new lines and add to self.initial
        else:
            self.initial = chunk


class TagStripper(HTMLParser):

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()
