# **T2A2 Web API assessment** - *Tané Kaio*

***
## **1. Identify problem to be solved**
***

As a passionate music lover who doesn't use social media platforms like Facebook or Instagram, it has become increasingly difficult to keep up to date and know what's happening in my local music scene. But even when I used those platforms, the smaller "word-of-mouth" shows (that usually produce the most magical moments) would often be obscured or not posted at all. Facebook in particular typically relies on the musical act, the venue and/or an events/ticketing company to publish a show - I would like to propose a platform for the *punters* to share upcoming shows with each other with a focus on community spirit - the heart of music. 

***
## **2. Why is it a problem that needs solving?**
***

For a long time social media platforms such as Facebook and Instagram have dominated the “events” category for local music scenes. But people are increasingly withdrawing from social media for various reasons, which can make staying in the loop difficult in a digital world. Bands still need exposure and people still need to know where they can get their music fix, so a public and free local gig database can solve these problems in an environment that doesn’t have some of the less desirable side effects of social media. 

***
## **3. Why have I chosen PSQL? Pros/cons, compare to others**
***

I have chosen PostgreSQL (PSQL) as my *database management system* (DBMS) because it as well as being the focal database system used in class, it is free, open-source and offers all the features I need for this API project. Another option would have been MySQL, which is also open source and potentially offers faster performances and is easier to use, however PSQL supports more advanced features, such as the `CASCADE` deletion event constraints, the `EXCEPT` query clause to exclude results from a search and the ability to store complex data objects such as arrays. MySQL, however does outperform PSQL for read-only processes however given the scope of my project it shouldn't be too significant of a factor. 

https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-vs-mysql/ 

***
## **4. Identify and discuss the key functionalities and benefits of an ORM**
***

I will be utilising a database toolkit called *SQLAlchemy* as my Object Relational Mapper (ORM) for the API. An ORM essentially allows a translation between SQL commands and statements (such as `SELECT * FROM table`) from an object oriented environment - such as an application written in Python. This allows us to interact with and control our PostgreSQL database (which is natively controlled by pure SQL syntax) from our Flask application, opening the door to endless possibilities of database manipulation with programmatic conditions and instructions. ORM's like SQLAlchemy simply map SQL code to our preferred programming language, so that our example above `SELECT * FROM table` can be expressed in our application as `table.query.all()`. 

https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a 




***
## **7. Detail any third party services that your app will use**
***

* **Flask** (`flask`) is at the spine of the API and is the Python web framework I will be using which is fairly lightweight however it offers great features like a built-in developmental server and easy web app configuration. As it's so barebones there are many great services that are made for it which offers a great deal of flexibility. It does, however provide features such as `Blueprint`, `request`, `abort` and `Markup` that will help with handling web-based features of the API.

* As mentioned above, I will be using **SQLAlchemy** as well as the Flask-specific **Flask-SQLalchemy** (`sqlalchemy` and `flask_sqlalchemy`) as my object-relational-mapper to interact with my database. Flask doesn't have its own database abstraction layer so we need packages like this to streamline database management

* For serialisation/deserialisation I will be implementing **Marshmallow** (`flask_marshmallow`) to convert complex data objects to simple Python datatypes. I will be constructing my schemas using Marshmallow's `Schema` class, which allows me to control validation and handle exceptions using modules from the `marshmallow` package such as `ValidationError`.

* I will be controlling user authentication using **Flask-JWT-Extended** (`flask_jwt_extended`), which is a service that generates and handles JSON Web Token features. I can verify the current user's identity using functions such as `get_jwt_identity()` and use the `@jwt_required()` decorator to control route access. 

* For sensitive data storage I will use **Flask-Bcrypt** (`flask_bcrypt`) for its hashing tools to ensure that sensitive information such as passwords are not stored in plain-text in the database.


