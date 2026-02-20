# 📚 BookApp

Aplicación web desarrollada con **Django 6.0** para gestionar una lista de lectura personal.
Permite registrar libros con información como páginas, valoración, estado y fecha de publicación,
con autenticación y control de acceso por permisos.

---

## ✨ Nuevas implementaciones

### Listado en tabla
El listado de libros ha pasado de ser una lista simple a una **tabla** con las columnas:
título, páginas, rating, estado y fecha de publicación.

### Filtrado, ordenación y paginación
- **Filtrado** por título mediante un formulario de búsqueda.
- **Ordenación** por cualquier columna haciendo clic en su cabecera (ascendente/descendente).
- **Paginación** de 10 libros por página, compatible con filtro y ordenación simultáneos.

### Página de estadísticas (`/stats`)
Nueva página con:
- Libro con **más** y **menos** páginas.
- **Media de páginas** y **rating medio** de todos los libros.
- **Gráfico de tarta**: libros agrupados por estado (Pending, Reading, Finished).
- **Gráfico de barras**: libros agrupados por rating (1-5).

---

## 🚀 Instalación rápida

```bash
git clone https://github.com/georgealexandrunechita/bookapp
cd bookapp
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
🧪 Tests
bash
python manage.py test
