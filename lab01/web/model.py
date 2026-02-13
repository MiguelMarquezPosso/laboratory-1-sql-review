from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
from sqlalchemy import Integer, SmallInteger, String, Text, Numeric, ForeignKey, TIMESTAMP, LargeBinary

Base = declarative_base()

class Country(Base):
    __tablename__ = "country"
    country_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class City(Base):
    __tablename__ = "city"
    city_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.country_id"), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Address(Base):
    __tablename__ = "address"
    address_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    address2: Mapped[str] = mapped_column(String(50))
    district: Mapped[str] = mapped_column(String(50), nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.city_id"), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20))
    phone: Mapped[str] = mapped_column(String(20))
    location: Mapped[bytes] = mapped_column(LargeBinary)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Store(Base):
    __tablename__ = "store"
    store_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    manager_staff_id: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Staff(Base):
    __tablename__ = "staff"
    staff_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_name: Mapped[str] = mapped_column(String(45), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    picture: Mapped[bytes] = mapped_column(LargeBinary)
    email: Mapped[str] = mapped_column(String(50))
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"), nullable=False)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    username: Mapped[str] = mapped_column(String(16), nullable=False)
    password: Mapped[str] = mapped_column(String(40))
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Customer(Base):
    __tablename__ = "customer"
    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_name: Mapped[str] = mapped_column(String(45), nullable=False)
    email: Mapped[str] = mapped_column(String(50))
    address_id: Mapped[int] = mapped_column(ForeignKey("address.address_id"), nullable=False)
    active: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    create_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Language(Base):
    __tablename__ = "language"
    language_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Film(Base):
    __tablename__ = "film"
    film_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    release_year: Mapped[int] = mapped_column(SmallInteger)
    language_id: Mapped[int] = mapped_column(ForeignKey("language.language_id"), nullable=False)
    original_language_id: Mapped[int] = mapped_column(ForeignKey("language.language_id"))
    rental_duration: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    rental_rate: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    length: Mapped[int] = mapped_column(SmallInteger)
    replacement_cost: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    rating: Mapped[str] = mapped_column(String(10))
    special_features: Mapped[str] = mapped_column(String(255))
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Actor(Base):
    __tablename__ = "actor"
    actor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_name: Mapped[str] = mapped_column(String(45), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Category(Base):
    __tablename__ = "category"
    category_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class FilmActor(Base):
    __tablename__ = "film_actor"
    actor_id: Mapped[int] = mapped_column(ForeignKey("actor.actor_id"), primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey("film.film_id"), primary_key=True)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class FilmCategory(Base):
    __tablename__ = "film_category"
    film_id: Mapped[int] = mapped_column(ForeignKey("film.film_id"), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.category_id"), primary_key=True)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Inventory(Base):
    __tablename__ = "inventory"
    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey("film.film_id"), nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.store_id"), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Rental(Base):
    __tablename__ = "rental"
    rental_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    rental_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.inventory_id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.customer_id"), nullable=False)
    return_date: Mapped[str] = mapped_column(TIMESTAMP)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.staff_id"), nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

class Payment(Base):
    __tablename__ = "payment"
    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.customer_id"), nullable=False)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff.staff_id"), nullable=False)
    rental_id: Mapped[int] = mapped_column(ForeignKey("rental.rental_id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    payment_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    last_update: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)