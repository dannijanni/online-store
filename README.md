## Online Ecommerce Shop example using Django SQLite

some feature:

- Filter product form
- Add to Cart, Remove from Cart
- Product summary
- Checkout form
- Login with Guest Account

<br>

### Installation

clone this repository:

```
git clone https://github.com/dannijanni/online-store.git
```

- option 1: <a href="#virtualenv">Virtual Environment</a>
- option 2: <a href="#dockerengine">Docker</a>

### virtualenv

Recommends **Python3.9+**

```
cd app && pip install -r requirements.txt
```

> **Migrate** and **Load** dump data

```
python3 manage.py migrate
```

```
python3 manage.py loaddata dumped_data.json
```

> Run Server

```
python3 manage.py runserver
```

```
127.0.0.1:8000/
```

### dockerengine

```
docker-compose up -d --build
```

```
127.0.0.1:8000/
```
