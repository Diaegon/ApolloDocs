# def test_create_user(session, mock_db_time):
#     with mock_db_time(model=User) as time:
#         new_user = User(username="diego", password="secret", email="test@test")

#     session.add(new_user)
#     session.commit()

#     user = session.scalar(select(User).where(User.username == "diego"))
#     assert asdict(user) == {
#         "id": 1,
#         "username": "diego",
#         "password": "secret",
#         "email": "test@test",
#         "created_at": time,
#     }
