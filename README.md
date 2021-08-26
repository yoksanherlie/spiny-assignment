# Spiny.ai Take Home Assignment

## Brief Instructions

1. `docker-compose up` to start the whole app (will build image first)
2. Open new terminal session and `docker exec -it spiny_puller_1 bash` to access the puller container
    - Run `python search_interest_puller.py` to pull google trends data (optional: specify date (default to yesterday), e.g: `python search_interest_pullery.py 2021-08-23`)
3. Open browser session and access the API on `localhost:9000/apis/search_interest/<keyword>` to get the normalized search interest of the keyword specified.

## Framework/Libraries/Techs Used

1. Pytrends
    - To access google trends api
2. Pandas
    - To manipulate data returned from the google trends api, the data returned is of type pandas `DataFrame`
3. Flask
    - Small web framework use to create the simple API
4. MongoDB
    - NoSQL database used to store google trends data returned from the API.
    - Document format:
        ```json
        {
            "keyword": "ncis",
            "trends_data": {
                "2021-08-24 00:00:00": 12,
                "2021-08-24 04:00:00": 52,
                "2021-08-24 08:00:00": 6,
                "2021-08-24 12:00:00": 45,
                ...
            }
        }
        ```
    - **Reason**: Simple lightweight solution to store the data (JSON format) so that I can use the value directly and don't have to manipulate it anymore (other than normalizing) when I try to retrieve the normalized search interest. Also to accomodate the expected return format of the API.
5. Pymongo
    - Python MongoDB library

## CI/CD Pipeline using Github Actions explanation

For this project, I'm gonna use a simple deployment method where I deploy the puller and the API to a DigitalOcean Server via Docker (docker image).

1. Create unit testing for the functions at the very least
2. Add DockerHub credentials to Github to enable access and for variables used in the workflow
2. Build a Github Action workflow with these steps on `push` event to `master` branch for the repository:
    - build:
        1. Runs on `ubuntu-latest`
        2. Checkout code from repository
        3. Setup Python with Python version 3.7
        5. Install dependencies required from `requirements.txt`
        4. Run tests
    - deploy: **(only runs if the build job succedd)**
        1. Login to DockerHub
            - uses `docker/login-action`
        2. Build and push Docker image to DockerHub
            - uses `docker/build-push-action`
        3. Deploy puller and API to DigitalOcean Server with Docker
            - Run a script in the server to pull the Docker image from the DockerHub
