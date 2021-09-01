from html.parser import HTMLParser
from io import StringIO

from lemmatization.lemmatizer import Lemmatizer


class EditedTextHtmlParser(HTMLParser):

    def __init__(self, token_node_dict=None, lang=None):
        self.current_tag = None
        self.current_attrs = {}
        self.current_data = ""
        self.lemmatized_text_data = []
        self.token_node_dict = token_node_dict
        self.lang = lang
        self.lemmatizer = Lemmatizer(self.lang)
        return super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            self.current_tag = "span"
            self.current_attrs = dict(attrs)

    def handle_endtag(self, tag):
        if "follower" in self.current_attrs:
            self.separate_true_followers(self.current_data)
        elif self.current_data is not None:
            self.current_attrs["node"] = self.parse_node_value()
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
                    (self.parse_node_value() not in self.token_node_dict[data])
                ):
                    self.lemmatize_chunk(data)
                else:
                    self.current_data = data
            except KeyError:
                self.lemmatize_chunk(data)

    def separate_true_followers(self, follower):
        followers = []
        text = []
        for idx, ch in enumerate(follower):
            if ch.isalnum():
                text = follower[idx:]
                break
            followers.append(ch)
        # this is problem if it starts with a follower
        self.lemmatized_text_data[-1]["following"] += "".join(followers)
        if(len(text) > 0):
            self.lemmatize_chunk("".join(text))

    def parse_node_value(self):
        try:
            return int(self.current_attrs["node"])
        except (KeyError, ValueError):
            return None

    def lemmatize_chunk(self, chunk):
        self.current_data = None
        new_data = self.lemmatizer.lemmatize(chunk)
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
