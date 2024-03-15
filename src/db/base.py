from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_255 = Annotated[str, 255]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_255: String(255),
    }

    # def __repr__(self):
    #     cols = []
    #     for col in self.__table__.columns.keys():
    #         if col != "hashed_password":
    #             cols.append(f"{col}={getattr(self, col)}")
    #     return f"<{self.__class__.__name__}: {', '.join(cols)}>"
