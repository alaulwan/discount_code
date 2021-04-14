-   **What is the URL to your application?**

*swagger api documentation*

<http://127.0.0.1:8000/swagger>

<http://127.0.0.1:8000/redoc>
________________________________________________________________________________
-   **How to run:**
1.   **Using docker-compose:**

```    -   git clone https://github.com/alaulwan/discount_code.git ```

```    -   cd discount_code ```

```    -   docker-compose up ```
________________________________________________________________________________
2.  **Without docker:**

- It is recommended to create and activate a new virtual environment

- Execute the sql file **./initiate_sql/init.sql** to create requered db and user

```    -   git clone https://github.com/alaulwan/discount_code.git ```

```    -   cd discount_code ```

```    -   pip install -r requirements.txt ```

```    -   python manage.py makemigrations base ```

```    -   python manage.py makemigrations discount_code ```

```    -   python manage.py migrate ```

```    -   python manage.py shell < initial_script.py ```

 ```   -   python manage.py runserver ```

________________________________________________________________________________
In both cases, the script **initial_script.py** will create default users and discount codes.
- the user: **admin:admin**
- the user: **brand:brand**
- the user: **alaa:alaa** (with one assigned discount code)
- the user: **omar:omar** (no assigned discount code)
- Two additinal discount codes that are not assigned to any user (all discount code are for the brand **HM**)
