from snowman_teste.models import User, Category, TourPoint, Session, Base, engine

Base.metadata.create_all(engine)

restaurante = Category(name='Restaurante')
mouseu = Category(name='Mouseu')

Session.add(restaurante)
Session.add(mouseu)
Session.commit()

user1 = User(name='Teste01', email='teste01@teste.com', password='1234')
user2 = User(name='Teste02', email='teste02@teste.com', password='4321')

Session.add(user1)
Session.add(user2)
Session.commit()

tour_point1 = TourPoint(name='Aqui', latitude=-25.4330467, longitude=-49.2798088, user_id=user1.id, category=restaurante)

tour_point2 = TourPoint(name='Ali', latitude=-25.410174, longitude=-49.26695470000001, user_id=user2.id, category=mouseu)

Session.add(tour_point1)
Session.add(tour_point2)
Session.commit()