from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class webServerHandler(BaseHTTPRequestHandler):
    """Requests handler."""

    def do_GET(self):
        try:
            if self.path == "/":
                # redirecting to restaurants list
                self.send_response(301)
                self.send_header("Location", "/restaurants")
                self.end_headers()

            if self.path.endswith("/restaurants"):

                # getting the data from the db
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurants = session.query(Restaurant).all()
                session.close()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<a href='/new'>Make a new Restaurant</a>"
                output += "<h1>Restaurants List:</h1><ul>"
                del_link = " <a href='/%s/delete'>Delete</a>"
                edit_link = " <a href='/%s/edit'>Edit</a>"
                for r in restaurants:
                    output += "<li>" + r.name
                    output += (edit_link % str(r.id))
                    output += (del_link % str(r.id)) + "</li>"
                output += "</ul></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a new Restaurant:</h1><ul>"
                form = '''<form method='POST' enctype='multipart/form-data' action='/new'><input name="restaurant" type="text" ><input type="submit" value="Submit"> </form>'''
                output += form
                output += "</ul></body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                # getting id from path:
                restaurant_id = self.path.split('/')[1]

                # getting restaurant from the database

                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
                session.close()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                if restaurant:
                    output += "<h1>Edit %s Restaurant:</h1><ul>" % restaurant.name
                    form = '''<form method='POST' enctype='multipart/form-data' action='/edit'><input name="restaurant" type="text" value="%s"><input type="submit" value="Rename"><input type="hidden" name="id" value="%s"> </form>''' % (restaurant.name, restaurant.id)
                    output += form
                else:
                    output += "<h1>Restaurant Not found!</h1>"
                output += "</ul></body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/delete"):
                # getting id from path:
                restaurant_id = self.path.split('/')[1]

                # getting restaurant from the database

                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
                session.close()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                if restaurant:
                    output += "<h1>Delete %s Restaurant?</h1><ul>" % restaurant.name
                    form = '''<form method='POST' enctype='multipart/form-data' action='/delete'><input type="submit" value="Delete"><input type="hidden" name="id" value="%s"> </form>''' % restaurant.id
                    output += form
                else:
                    output += "<h1>Restaurant Not found!</h1>"
                output += "</ul></body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path == '/new':
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')

                # saving the data from the db
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant1 = Restaurant(name=messagecontent[0])
                session.add(restaurant1)
                session.commit()
                session.close()

                output = ""
                output += "<html><body>"
                output += " <h2> Restaurant added: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += "</body></html>"
                self.wfile.write(output)
            if self.path == '/edit':

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('restaurant')[0]
                    restaurant_id = int(fields.get('id')[0])

                # getting the data from the db
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant1 = session.query(Restaurant).filter_by(id=restaurant_id).first()
                if restaurant1:
                    restaurant1.name = new_restaurant_name
                    session.add(restaurant1)
                    session.commit()
                session.close()
                # redirecting to restaurants list
                self.send_response(301)
                self.send_header("Location", "/restaurants")
                self.end_headers()
            if self.path == '/delete':

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_id = int(fields.get('id')[0])

                # deleteting the restaurant from the db
                engine = create_engine('sqlite:///restaurantmenu.db')
                Base.metadata.bind = engine
                DBSession = sessionmaker(bind=engine)
                session = DBSession()
                restaurant1 = session.query(Restaurant).filter_by(id=restaurant_id).first()
                if restaurant1:
                    session.delete(restaurant1)
                    session.commit()
                session.close()
                # redirecting to restaurants list
                self.send_response(301)
                self.send_header("Location", "/restaurants")
                self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
