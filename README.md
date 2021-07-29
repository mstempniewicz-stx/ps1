# Django React/Redux Base Project

This repository includes a boilerplate project. It uses Django as backend and React as frontend.

## Run

1. Make sure that you have working [Docker](https://www.docker.com/products/overview) and [Docker Compose](https://docs.docker.com/compose/install/).

2. Retrieve code
   `git clone git@github.com:stxnext/project-starter.git`

3. Create `.env` file just by using default template values
   `cp .env.template .env`

4. Build and run instance
   `make docker up`
   `make manage createsuperuser`

5. Enjoy at `http://localhost:3000`

6. To stop just push `Ctrl+C` or run
   `make docker stop`

7. Add git hooks
   You need to install pre-commit on your system instead of docker. In order to do that run the following command:
   `python -m pip install pre-commit`
   `make add-git-hooks`

## Other topics

-   [New Project Repository](docs/new_repository.md)
-   [Deployment](docs/deployment.md)
-   [Testing](docs/testing.md)
-   [Technologies](docs/technologies.md)
-   [Contributing](docs/contributing.md)
# ps1
