from snowman_teste.models import User, TourPoint, Session, Base, engine

engine.echo = True
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

user1 = User(email='teste01@teste.com', password='123')
user1.name = 'Teste01'
user2 = User(email='teste02@teste.com', password='4321')
user2.name = 'Teste02'

Session.add(user1)
Session.add(user2)
Session.commit()

tour_point1 = TourPoint(name='Aqui',
                        latitude=-25.4330467,
                        longitude=-49.2798088,
                        public=False,
                        category='restaurant')
tour_point1.user = user1

tour_point2 = TourPoint(name='Ali',
                        latitude=-25.410174,
                        longitude=-49.26695470000001,
                        public=True,
                        category='park')
tour_point2.user = user2

Session.add(tour_point1)
Session.add(tour_point2)
Session.commit()

print(engine.url)


