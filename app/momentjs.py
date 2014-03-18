from jinja2 import Markup

class momentjs(object):
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        output = self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z")
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n\
                      </script>" % (output, format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
