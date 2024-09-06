
# BackBoiler


Welcome to **BackBoiler** – a boilerplate for Django restful services projects.
this boiler has drf-spectacular usefule functionality to build a new project. 

## Prerequisites

Make sure you have the following installed:

- **python**
- **virtualenv**

## Getting Started

Follow these steps to get the project up and running:
1. **Clone the repository**

    ```bash
    git clone https://github.com/aimoonx//BackBoiler.git
    ```

2. **Navigate to the project directory**

    ```bash
    cd BrontBoiler
    ```

3. **Install the dependencies**

    ```bash
    python -m virtualenv backenv
    .\backenv\Scripts\activate
    pip install -r reqs.txt
    ```

4. **Run the development server**

    ```bash
    Demo
    ```
5. **make sure: if you are in windows set policy**

    ```bash
    Set-ExecutionPolicy Unrestricted -Scope Process
    ```
## Run Demo:
```bash
cd src
```
```bash
python manage.py makemigrations TestAppModel
```
```bash
python manage.py migrate TestAppModel
```
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
to check the correct install of drf-spectacular run:
```bash
python manage.py spectacular --color --file swagger.yml
```
```bash
py manage.py runserver
```

After running the development server, you can see the working demo by opening your browser and navigating to `http://127.0.0.1:8000`.

you can check the swagger in 
~~~bash
http://127.0.0.1:8000/swagger/
~~~

---

Happy coding!
