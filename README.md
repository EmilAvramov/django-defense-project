# DigiWorld

## Description

The project is a small library application, which connects to an external API to retrieve Digimon data, and allows users to browse the thousands of digimon currently created/added to all global databases.
This also allows referencing and seeing prior and future evolutions easily and allows for in-depth exploration of possible evolution paths.

## Guest/Registered/Admin/Superuser
- Guest users may browse the site and search, but may not add digimon to their library or edit a profile. 
- Registered users may browse, add to, remove from or edit digimon in their library and manage their profile (edit account info/password/delete account), in addition to guest functions.
- Admins/staff have some limited CRUD permissions in the admin site and may not modify everything (e.g. permissions).
- Superusers may manage the whole admin site as needed.

## Features
- **Rich Database** - The searchable database features all currently created/added digimon known. Note this may sometimes feature incomplete digimons as those get updated over time.
- **Seamless Experience** - Users can easily access all features, can navigate the application with ease and enjoy a pleasant experience.
- **Library Function** - Registered users may add digimon to their collection and add comments to them for reference. This allows brainstorming evolution paths and seeing skill patterns easily.
- **Profile Section** - Users can edit their profile as needed, including adding additional details and a picture. Users may also change their passwords and delete their accounts if needed.
- **Helpful Info** - The application features a few pages that may be helpful to enthusiasts new to the digimon universe get acquainted with what it is about.

## Setup and Usage

1. Clone the repository and navigate to the project directory.

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Create an .env file in src/django_defense_project and add the necessary PostgreSQL details according to the 6 parameter names in settings.py.
   This allows the app to connect to a local databse. Format for .env is below:
   ```
   SECRET_KEY=(can be anything)
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

5. Apply the database migrations:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create an admin superuser and follow the prompt steps:

   ```
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```
   python manage.py runserver
   ```

8. Access the admin panel at http://localhost:8000/admin/ and use the superuser credentials to log in.

9. Begin managing the pizza menu and ingredients via the admin panel or web.
