import os
from flask import Flask, render_template_string, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from queries import query_a, query_b, query_c, query_d

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@db:5432/sakila"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Sakila | Consultas ORM</title>
  <style>
    body { font-family: 'Segoe UI', sans-serif; background: #f6f7fb; margin: 0; padding: 0; }
    .container { max-width: 1100px; margin: 30px auto; padding: 20px; }
    h1 { color: #222; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); gap: 15px; }
    .card { background: white; border-radius: 12px; padding: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
    button { background: #4f46e5; color: white; border: none; padding: 10px 14px; border-radius: 8px; cursor: pointer; }
    button:hover { background: #4338ca; }
    table { width: 100%; border-collapse: collapse; margin-top: 16px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f0f0f0; }
    .muted { color: #666; font-size: 0.95em; }
  </style>
</head>
<body>
<div class="container">
  <h1>Sakila - Consultas ORM</h1>
  <p class="muted">Consultas implementadas con SQLAlchemy ORM.</p>

  <div class="grid">
    <div class="card">
      <h3>A. Más alquileres por categoría</h3>
      <form method="get">
        <input type="hidden" name="view" value="a"/>
        <button>Ejecutar</button>
      </form>
    </div>
    <div class="card">
      <h3>B. Clientes con gasto > promedio</h3>
      <form method="get">
        <input type="hidden" name="view" value="b"/>
        <button>Ejecutar</button>
      </form>
    </div>
    <div class="card">
      <h3>C. Películas sobre promedio de categoría</h3>
      <form method="get">
        <input type="hidden" name="view" value="c"/>
        <button>Ejecutar</button>
      </form>
    </div>
    <div class="card">
      <h3>D. Clientes Q1 pero no Q2</h3>
      <form method="get">
        <input type="hidden" name="view" value="d"/>
        <button>Ejecutar</button>
      </form>
    </div>
  </div>

  {% if view and results %}
  <div class="card" style="margin-top: 20px;">
    <h2>Resultados</h2>
    <table>
      <tr>
        {% for k in results[0].keys() %}
          <th>{{ k }}</th>
        {% endfor %}
      </tr>
      {% for row in results %}
        <tr>
          {% for v in row.values() %}
            <td>{{ v }}</td>
          {% endfor %}
        </tr>
      {% endfor %}
    </table>
  </div>
  {% endif %}

  {% if view and (results|length == 0) %}
    <p class="muted">Sin resultados.</p>
  {% endif %}
</div>
</body>
</html>
"""

@app.get("/")
def index():
    view = request.args.get("view", "")
    results = []

    with SessionLocal() as session:
        if view == "a":
            results = query_a(session)
        elif view == "b":
            results = query_b(session)
        elif view == "c":
            results = query_c(session)
        elif view == "d":
            results = query_d(session)

    return render_template_string(HTML, view=view, results=results)

@app.get("/health")
def health():
    return {"status": "ok"}