from snowman_teste.models import Access, User, Category, TourPoint, Session, Base, engine

engine.echo = True
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

restaurante = Category(name='Restaurante')
mouseu = Category(name='Mouseu')

Session.add(restaurante)
Session.add(mouseu)
Session.commit()

public = Access('public')
private = Access('private')

Session.add(public)
Session.add(private)
Session.commit()

user1 = User(name='Teste01', email='teste01@teste.com', password='123')
user2 = User(name='Teste02', email='teste02@teste.com', password='4321')

Session.add(user1)
Session.add(user2)
Session.commit()

tour_point1 = TourPoint(name='Aqui',
                        latitude=-25.4330467,
                        longitude=-49.2798088,
                        user_id=user1.id,
                        access_id=public.id,
                        category_id=restaurante.id)

tour_point2 = TourPoint(name='Ali',
                        latitude=-25.410174,
                        longitude=-49.26695470000001,
                        user_id=user2.id,
                        access_id=private.id,
                        category_id=mouseu.id)

Session.add(tour_point1)
Session.add(tour_point2)
Session.commit()

print(engine.url)


