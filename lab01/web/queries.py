from sqlalchemy import select, func, literal_column, extract
from sqlalchemy.orm import Session
from model import (
    Rental, Inventory, Film, FilmCategory, Category,
    Payment, Customer
)

def query_a(session: Session):
    alquileres = (
        select(
            Category.name.label("categoria"),
            Film.title.label("titulo"),
            func.count(Rental.rental_id).label("total_alquileres")
        )
        .join(FilmCategory, FilmCategory.category_id == Category.category_id)
        .join(Film, Film.film_id == FilmCategory.film_id)
        .join(Inventory, Inventory.film_id == Film.film_id)
        .join(Rental, Rental.inventory_id == Inventory.inventory_id)
        .group_by(Category.name, Film.film_id, Film.title)
        .subquery()
    )

    max_por_categoria = (
        select(
            alquileres.c.categoria,
            func.max(alquileres.c.total_alquileres).label("max_alquileres")
        )
        .group_by(alquileres.c.categoria)
        .subquery()
    )

    stmt = (
        select(alquileres.c.categoria, alquileres.c.titulo, alquileres.c.total_alquileres)
        .join(
            max_por_categoria,
            (max_por_categoria.c.categoria == alquileres.c.categoria) &
            (max_por_categoria.c.max_alquileres == alquileres.c.total_alquileres)
        )
        .order_by(alquileres.c.categoria.asc(), alquileres.c.titulo.asc())
    )

    return session.execute(stmt).mappings().all()

def query_b(session: Session):
    gasto_por_cliente = (
        select(
            Customer.customer_id,
            Customer.first_name,
            Customer.last_name,
            Customer.email,
            func.sum(Payment.amount).label("gasto_total")
        )
        .join(Payment, Payment.customer_id == Customer.customer_id)
        .group_by(Customer.customer_id, Customer.first_name, Customer.last_name, Customer.email)
        .subquery()
    )

    promedio = select(func.avg(gasto_por_cliente.c.gasto_total)).scalar_subquery()

    stmt = (
        select(
            gasto_por_cliente.c.first_name.label("nombre"),
            gasto_por_cliente.c.last_name.label("apellido"),
            gasto_por_cliente.c.email.label("correo"),
            gasto_por_cliente.c.gasto_total,
            promedio.label("promedio")
        )
        .where(gasto_por_cliente.c.gasto_total > promedio)
        .order_by(gasto_por_cliente.c.gasto_total.desc())
    )

    return session.execute(stmt).mappings().all()

def query_c(session: Session):
    alquileres = (
        select(
            FilmCategory.category_id,
            Category.name.label("categoria"),
            Film.title.label("titulo"),
            func.count(Rental.rental_id).label("total_alquileres")
        )
        .join(Category, Category.category_id == FilmCategory.category_id)
        .join(Film, Film.film_id == FilmCategory.film_id)
        .join(Inventory, Inventory.film_id == Film.film_id)
        .join(Rental, Rental.inventory_id == Inventory.inventory_id)
        .group_by(FilmCategory.category_id, Category.name, Film.film_id, Film.title)
        .subquery()
    )

    promedio_por_categoria = (
        select(
            alquileres.c.category_id,
            func.avg(alquileres.c.total_alquileres).label("promedio_categoria")
        )
        .group_by(alquileres.c.category_id)
        .subquery()
    )

    stmt = (
        select(
            alquileres.c.categoria,
            alquileres.c.titulo,
            alquileres.c.total_alquileres,
            promedio_por_categoria.c.promedio_categoria
        )
        .join(promedio_por_categoria, promedio_por_categoria.c.category_id == alquileres.c.category_id)
        .where(alquileres.c.total_alquileres > promedio_por_categoria.c.promedio_categoria)
        .order_by(alquileres.c.categoria.asc(), alquileres.c.total_alquileres.desc())
    )

    return session.execute(stmt).mappings().all()

def query_d(session: Session):
    q1 = (
        select(Rental.customer_id)
        .where(extract("quarter", Rental.rental_date) == 1)
        .distinct()
        .subquery()
    )

    q2 = (
        select(Rental.customer_id)
        .where(extract("quarter", Rental.rental_date) == 2)
        .distinct()
        .subquery()
    )

    stmt = (
        select(
            Customer.first_name.label("nombre"),
            Customer.last_name.label("apellido"),
            Customer.email.label("correo")
        )
        .where(Customer.customer_id.in_(select(q1.c.customer_id)))
        .where(~Customer.customer_id.in_(select(q2.c.customer_id)))
        .order_by(Customer.first_name.asc(), Customer.last_name.asc())
    )

    return session.execute(stmt).mappings().all()