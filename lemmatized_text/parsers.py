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
        return super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            self.current_tag = "span"
            self.current_attrs = dict(attrs)

    def handle_endtag(self, tag):
        if "follower" in self.current_attrs:
            self.separate_true_followers(self.current_data)
        # check for breaks and add new line to following for last element in the lemmatized_text_data
        elif tag == "br":
            following = self.lemmatized_text_data[-1]["following"]
            new_following = f"{following}\n"
            self.lemmatized_text_data[-1]["following"] = new_following
        elif self.current_data is not None and self.current_tag is not None:
            self.current_attrs["lemma_id"] = self.parse_lemma_id_value()
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
                    (self.parse_lemma_id_value() not in self.token_lemma_dict[data])
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

    def parse_lemma_id_value(self):
        """
        Parses the string lemma_id value in the current attrs to an integer.
        Returns int, or None if there is an error
        """
        try:
            return int(self.current_attrs["lemma_id"])
        except (KeyError, ValueError):
            return None

    def lemmatize_chunk(self, chunk):
        """
        Takes an unrecognized chunk of text.
        Sends 'chunk' to be lemmatized, then extends the data with the returned content.
        Returns None
        """
        self.current_data = None
        new_data = self.lemmatizer.lemmatize(chunk)
        # check if last element in the new_data is empty and remove - fixes double newline when editing
        if new_data[-1]["word"] == "" and new_data[-1]["following"] == " ":
            new_data.pop()
        # Checks if chunk is not return and newline "\r\n" - only add tokens if it the chunk is not a return/newline
        # Fixes problem with empty tokens
        if chunk != "\r\n":
            self.lemmatized_text_data.extend(new_data)


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
