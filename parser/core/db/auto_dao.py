from core.db.models.auto import Auto
from core.db.database import session_factory


class AutoDAO:
    def __init__(self):
        self.session_factory = session_factory

    def create(self, auto_data: dict) -> Auto:
        with session_factory() as session:
            auto = Auto(**auto_data)
            session.add(auto)
            session.commit()
            session.refresh(auto)
            return auto

    def exists_by_auto_id(self, auto_id: int) -> bool:
        with self.session_factory() as session:
            exists = session.query(
                session.query(Auto).filter(Auto.auto_id == auto_id).exists()
            ).scalar()
            return exists

    def get_price_by_auto_id(self, auto_id: int) -> int:
        with self.session_factory() as session:
            price = session.query(Auto.price).filter(Auto.auto_id == auto_id).scalar()
            return price

    def update(self, update_data: dict) -> int:
        with self.session_factory() as session:
            result = (
                session.query(Auto)
                .filter(Auto.auto_id == update_data["auto_id"])
                .update(update_data)
            )
            session.commit()
            return result
