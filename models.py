from typing import List

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

from sqlalchemy.orm import Mapped, mapped_column


class Shed(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    children: Mapped[List["ShedData"]] = relationship(back_populates="shed")


class ShedData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    shed_id: Mapped[int] = mapped_column(ForeignKey("shed.id"))
    shed: Mapped["Shed"] = relationship(back_populates="children")
    date: Mapped[str]
    value: Mapped[float]
