#!/usr/bin/python3

"""
 Shortener class
 Simple web application for shortener URLs

 Author: Juan Antonio Ortega Aparicio

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp
from urllib.parse import unquote

class Shortener(webapp.webApp):
    """Simple web application for rename URLs.

    Content is stored in a dictionary, which is initialised
    with the web content."""

    # Declare and initialize content
    content = {}

    def parse(self, request):
        """Return the method in use, the resource in the call and the body"""
        method = request.split(' ', 2)[0]
        resource = request.split(' ', 2)[1]
        body = request.split('\r\n\r\n', 2)[1]

        return method, resource, body

    def process(self, parsedname):
        """Process the URL adding it to a dictionary where the short URL is the Key and the original URL is the value.
        When the user get in the app our server will show a form where the user can archive the URL and the Short URL,
        after that, user can call the URL writing the short URL as a resource
        """
        (method, resourceName, body) = parsedname
        print("METHOD = " + method)
        print("RESOURCE = " + resourceName)
        print("BODY = " + body)

        htmlbody = ""
        httpcode = ""
        url = ""
        short = ""

        questionaire = """
                        <html>
                            <body>
                            <h1>Shorten URL's App</h1>
                                <form action="/" method="POST">
                                <p>Insert URL: <input type="text" name="url"></p>
                                <p>Insert Short URL: <input type="text" name="short"></p>
                                <p><input type="submit" value="Send"></p>
                            </form>
                            "<h2>List:<br></h2>" 
                        """

        if resourceName == "/":
            httpcode = "200 OK"
            if method == "GET":
                htmlbody = questionaire + str(self.content)[1:-1] + "</body></html>"
            elif method == "POST":
                # Getting URL and short URL from body
                url = unquote(body.split("&", 2)[0].split("=", 2)[1])
                short = body.split("&", 2)[1].split("=", 2)[1]
                if url == "" or short == "":
                    htmlbody = "<html><body><p>QUERY STRING ERROR</p></body></html>"
                else:
                    if not url.startswith('http://') and not url.startswith('https://'):
                        url = 'https://' + url
                    htmlbody = '<html><head><meta charset="utf-8" /><title>Shorten URL\'s App</title></head>' + \
                               "<body><p><h2>Original URL: <a href=" + url + ">" + url + "</a></h2></p>" + \
                               "<p><h2>Shorten URL: <a href=" + url + ">" + short + "</a> </h2></p>" + \
                               "</body></html>"
                    self.content[short] = url
                    print("URL = " + url + ", SHORT = " + short)
            else:
                httpcode = "501 Not Implemented (en-US)"
                error_message = "Method not implemented on this server"
                htmlbody = "<html><body>" + error_message + "</body></html>"
        else:
            if method == "GET":
                if resourceName[1:] in self.content:
                    httpcode = "301 Moved Permanently"
                    htmlbody = '<html><head><title>Redirection</title><meta http-equiv="refresh"' \
                               'content="2;URL=' + self.content[resourceName[1:]] + '" /></head><body>' \
                               '<p>REDIRECTION.....</p></body></html>'
                else:
                    httpcode = "404 Not Found"
                    htmlbody = "<html>Error: Resource not available</html>"
            else:
                httpcode = "501 Not Implemented (en-US)"
                error_message = "Method not implemented on this server"
                htmlbody = "<html><body>" + error_message + "</body></html>"

        return httpcode, htmlbody


if __name__ == "__main__":
    testWebApp = Shortener("localhost", 1234)
