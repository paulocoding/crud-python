from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


print '####'
restaurants = session.query(Restaurant).all()
for r in restaurants:
    print r.name

print '####'
r = session.query(Restaurant).first()
print r.name

print '####'
r = session.query(Restaurant).filter_by(name='Panda Garden').first()
if r:
    print r.name
else:
    print "No restaurant found with that name"

print '#### count ###'
print session.query(Restaurant).count()

print '#### ordered ###'
restaurants = session.query(Restaurant).order_by(Restaurant.name)
for r in restaurants:
    print r.name

print '#### menu items ###'
items = session.query(MenuItem).order_by(MenuItem.name)
for i in items:
    print i.name + ' - ' + i.restaurant.name
