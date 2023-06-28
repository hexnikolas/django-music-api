


# Django JSON Backend API

Name: Nikos Zacharatos
Email: zacharatos.ni@gmail.com

This project is a Django JSON backend API that provides functionality for managing user subscriptions, retrieving tracks, and performing search queries on artists, albums, and tracks. The API uses MySQL database to store the artists, albums, tracks and user info.

## Database

The database schema is shown below.

![Database Schema](https://i.ibb.co/4P3tDj5/Blank-diagram-1.png)Since tracks cannot exist without an album, album column in track table is set to cascade on delete. This does not apply to album-artist or track-artist relations, which is set to Null on instead.

Database is created and populated using the music.sql file in mysql-dump directory.  The script adds 5 artists, 5 albums, 9 tracks and 3 users to the database.

User with id 1 has an expired subscription.
User with id 2 has an active subscription.
User with id 3 just registered, has null values in subscription_start and subscription_end columns.

There are also fixtures to repopulate the database. For example we can run ```python manage.py loaddata fixtures/users.json``` to reset subscription values of the users.


## Pages
The API has three endpoints. All of them return json responses that include a message field, which provides feedback.

The pages are described below:



### 1. Subscription

**Endpoint**: `/subscription` **Method:** POST

This endpoint allows users to purchase subscriptions. The body of the request has to  include the following fields:
 - **user_id**: The id of the user purchasing the subscription.
 - **duration**: The duration of the subscription in months. Duration values can be 1, 6, 12.
 - **card_number**: The card number that will execute the transaction with. Need to be of XXXX-XXXX-XXXX-XXXX format, where X is a number between 1 and 9.
  - **holder_name** : Card's holder name.
 - **expiration_date** : The expiration date of the card. Need to be in MM/YY format.
 - **cvv** : The CVV code of the card. Need to be in XXX format, where X is a number between 1 and 9.

The API performs the following test in the provided data:
- the user id is valid
- the user does not have an active subscription
- card number is of correct format
- expiration date is of correct format and later than current date
- cvv is of correct format

If everything is error free, the user table is updated. The subscription_start column is set to current date, and subscription_end column is set to current date plus the duration.
It was assumed that the duration variable is always  1, 6, or 12 and the API does not perform a value test.

### Track listening

Endpoint: `/track/track_id/listen`  **Method:** GET/POST

This endpoint allows users to listen to music. The body of the request has to include the following fields:
 - **user_id**: It's the id of the user that requests the track.

The API checks that the user exists and has an active subscription, then retrieves the track (if the track id is valid).

### Search

Endpoint: `/search`  **Method:** GET/POST

Retrieves artists, albums, and tracks that match the search term. The body of the request has to include a **search** field.
The search function checks the following columns:
- Name, short_description and genre in artist table.
- Name, type, artist in the album table.
- Title, lyrics, album and artist in the track table.

The search function also checks the foreign keys of the tables, for example, searching for a specific artist, will return all of the albums and songs that the artist has published.



## Containerization

The benefits of packing a backend app to a container are the following:

 - It makes the app portable. Anyone with a docker installation can pull the image and run it.
 - It makes the app scalable. Multiple containers of the same instance can be run on high workloads.
 - It makes the app isolated. Each container has its own file system, networking stack and process space, and they do not interfere with each-other.
 - It allows CI/CD, automating the build, test, and deployment processes for the app.

Dockerfile:

    FROM python:3.8
    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED 1
    WORKDIR /app
    COPY requirements.txt /app/requirements.txt
    RUN pip install -r requirements.txt
    COPY . /app
    ENTRYPOINT ["python"]
    CMD ["manage.py", "runserver","0.0.0.0:8000"]

docker-compose.yml



    version: '3'
	services:
	  db:
	    image: mysql
	    restart: always
	    env_file: docker.env
	    ports:
	      - '3306:3306'
	    expose:
	      - '3306'
	    volumes:
	      - ./mysql-dump:/docker-entrypoint-initdb.d
	    healthcheck:
	      test: ["CMD", "mysqladmin" ,"ping", "-h", "localhost"]
	      interval: 3s
	      retries: 10
	  web:
	    build: .
	    ports:
	      - "8000:8000"
	    restart: on-failure
	    depends_on:
	       db:
	         condition: service_healthy
	    volumes:
	      - .:/app

docker.env

    MYSQL_DATABASE=django_music
	MYSQL_USER=test
	MYSQL_PASSWORD=testtest
	MYSQL_ROOT_PASSWORD=testtesttest




## Build Instructions

Ports 3306 and 8000 must be free. Mysql container runs on port 3306, and django server runs on port 8000. The server is for development purposes only and uses `manage.py runserver` command.

1. Clone the repository:

   ```bash
   git clone https://gitlab.com/django1751326/django-music-api
   ```

2. Change directory
   ```bash
   cd django-music-api
   ```

3. Start the containers:

   ```bash
   docker compose up
   ```

	  In the event that the database container successfully runs while the server container fails to start, it is necessary to find the IP address of the database container. This can be achieved by executing the command `docker inspect <db-container> | grep IPAddress`. Subsequently, the IP setting in the "django-music-api/djangomusic/settings" file should be modified with the new database IP address, at line 87.

4. The API is accesible through localhost:8000 .




## CI/CD

The gitlab-ci.yml is shown below:

    stages: #define the two different stages
	  - build
	  - deploy

	build_image: #build job
	  stage: build
	  tags:
	    - Build
	  script: #scripts to run each time the image is built
	    - docker build -t repo.awesomecorp.com/docker-repo/streaming-service:latest .
	    - docker login -u <username_on_the_repo> -p <password> repo.awesomecorp.com
	    - docker push repo.awesomecorp.com/docker-repo/streaming-service:latest
	  only: # activate only at master branch
	    - master

	deploy_image: #deploy job
	  stage: deploy
	  tags:
	    - Deployment
	  script:  #scripts to run each time the image is deployed
	    - docker login -u <username_on_the_repo> -p <password> repo.awesomecorp.com
	    - docker pull repo.awesomecorp.com/docker-repo/streaming-service:latest
	    - docker compose up -d
	  only: # activate only at master branch
	    - master
	  when: manual # manual task, it won't be automatically triggered

Two stages are defined inside the file: build and deploy. Both are activated only on master branch.

The script inside build stage, first builds the image, then logs in and pushes it to repo.awesomecorp.com.

The script inside deploy stage logs in to repo.awesome.com, pulls the image, and composes it.

Deploy stage activates manually.
