#!/usr/bin/python3

"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp


class Shortener (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    content = {"a": "b", "c": "d"}

    def parse(self, request):
        """Return the resource name (including /)"""
        method = request.split(' ', 2)[0]
        resource = request.split(' ', 2)[1]
        body = request.split('\r\n\r\n', 2)[1]

        return method, resource, body

    def process(self, parsedname):
        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        (method, resourceName, body) = parsedname
        print("METHOD = " + method)
        print("RESOURCE = " + resourceName)
        print("BODY = " + body)

        htmlbody = ""
        httpcode = ""
        url = ""
        short = ""

        questionaire = """<h1>Shorten URL's App</h1>
                          <form action="" method="POST">
                            <p>Insert URL: <input type="text" name="url"></p>
                            <p>Insert Short URL: <input type="text" name="short"></p>
                            <p>
                              <input type="submit" value="Send">
                            </p>
                          </form>
                        """

        if resourceName == "/":
            httpcode = "200 OK"
            if method == "GET":
                htmlbody = "<html><body>" + questionaire + "<h2>List:<br></h2>"+str(self.content)[1:-1]+"</body></html>"
            elif method == "POST":
                url = body.split("&", 2)[0].split("=", 2)[1]
                short = body.split("&", 2)[1].split("=", 2)[1]
                if url == "" or short == "":
                    htmlbody = "<html><body><p>QUERY STRING ERROR</p></body></html>"
                else:
                    if url[4] == "http" or url[4] == "https":
                        htmlbody = "<html><body><p><h2>Original URL: <a href=" + url + ">" + url + "</a></h2></p>" + \
                                   "<p><h2>Shorten URL: <a href=" + url + ">" + short + "</a> </h2></p>" + \
                                   "</body></html>"
                        self.content[short] = url
                    else:
                        print("FALTA PROTOCOLO HTTP")

                print("URL = " + url + ", SHORT = " + short)
        else:
            httpcode = "404 Not Found"
            error_message = "Not implemented yet"
            htmlbody = "<html><body>" + error_message + "</body></html>"

        """
        if method == "POST":
            self.content[resourceName] = body.split("=")[1]

        if resourceName in self.content.keys():
            httpcode = "200 OK"
            htmlbody = "<html><body>" + self.content[resourceName]
        else:
            httpcode = "404 Not Found"
            error_message = "Not Found. Add it by yourself"
            htmlbody = "<html><body>" + error_message

        """

        return httpcode, htmlbody


if __name__ == "__main__":
    testWebApp = Shortener("localhost", 1234)
