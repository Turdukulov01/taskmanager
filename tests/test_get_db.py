def test_get_db_generator_covers_finally():
    from app.api import get_db

    gen = get_db()
    db = next(gen)     # попадаем в yield
    assert db is not None
    gen.close()        # закрываем генератор -> выполняется finally: db.close()
