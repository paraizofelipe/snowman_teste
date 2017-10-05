import googlemaps
from faker import Faker
from random import randint
from snowman_teste.settings import CONFIG
from snowman_teste.models import User, TourPoint, Session, Base, engine

engine.echo = True
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

fake = Faker('pt_BR')

location = [
    {"category": "restaurant", "name": "Restaurante Spagheto", "lat": -25.433106, "lng": -49.27981},
    {"category": "restaurant", "name": "Restaurante Amareno", "lat": -25.4334533, "lng": -49.2807944},
    {"category": "restaurant", "name": "Restaurante Ditarugo", "lat": -25.435214, "lng": -49.282142},
    {"category": "restaurant", "name": "Mac Donalds", "lat": -25.4301388, "lng": -49.2695793},
    {"category": "museum", "name": "Museu do Olho", "lat": -25.410174, "lng": -49.26695470000001},
    {"category": "museum", "name": "Museu do Expedicionário", "lat": -25.428618, "lng": -49.258505},
    {"category": "museum", "name": "Museu da Fotografia", "lat": -25.4263244, "lng": -49.2700843},
    {"category": "park", "name": "Prque Barigüi", "lat": -25.434937, "lng": -49.316264},
    {"category": "park", "name": "Parque Tingui", "lat": -25.3923778, "lng": -49.3050592},
    {"category": "park", "name": "Parque Tanguá", "lat": -25.3779871, "lng": -49.28395980000001}

]
gmaps = googlemaps.Client(key=CONFIG['api']['google_key'])

list_user = []
for index in range(3):
    user = User(email=fake.email(), password=fake.password())
    user.name = fake.name()
    list_user.append(user)


for index in range(10):
    tour_point = TourPoint(name=location[index]['name'],
                           latitude=location[index]['lat'],
                           longitude=location[index]['lng'],
                           public=fake.boolean(),
                           category=location[index]['category'])

    user = list_user[randint(0, 2)]
    user.list_tour_points.append(tour_point)
    Session.add(user)
    Session.commit()

# user1 = User(email='', password='')
# user1.name = ''
# user2 = User(email='', password='')
# user2.name = ''
#
# Session.add(user1)
# Session.add(user2)
# Session.commit()
#
# tour_point1 = TourPoint(name='Aqui',
#                         latitude=-25.4330467,
#                         longitude=-49.2798088,
#                         public=False,
#                         category='restaurant')
# tour_point1.user = user1
#
# tour_point2 = TourPoint(name='Ali',
#                         latitude=-25.410174,
#                         longitude=-49.26695470000001,
#                         public=True,
#                         category='park')
# tour_point2.user = user2
#
# Session.add(tour_point1)
# Session.add(tour_point2)
# Session.commit()
#
# print(engine.url)
#
#
