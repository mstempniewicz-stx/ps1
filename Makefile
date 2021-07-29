COMPOSE_DEV=docker-compose -f docker-compose.yml
COMPOSE_CYPRESS=$(COMPOSE_DEV) -f docker-compose.cypress.yml

docker:
	$(COMPOSE_DEV) $(filter-out $@,$(MAKECMDGOALS))

manage:
	$(COMPOSE_DEV) run --rm backend python /backend/manage.py $(filter-out $@,$(MAKECMDGOALS))

exec-manage:
	$(COMPOSE_DEV) exec backend python /backend/manage.py $(filter-out $@,$(MAKECMDGOALS))

install-dev-requirements:
	cd backend && pip install -r requirements.txt
	cd frontend && yarn

reset-db:
	$(COMPOSE_DEV) rm -fsv postgres
	$(COMPOSE_DEV) up -d --force-recreate postgres

add-git-hooks:
	@\cp ./config/scripts/git-hook-prepare-commit-msg.sh .git/hooks/prepare-commit-msg
	@chmod +rx .git/hooks/prepare-commit-msg
	pre-commit install

lint-backend:
	$(COMPOSE_DEV) up -d backend
	$(COMPOSE_DEV) exec -T backend isort -rc .
	$(COMPOSE_DEV) exec -T backend black .
	$(COMPOSE_DEV) exec -T backend flake8 .
	$(COMPOSE_DEV) exec -T backend pydocstyle .

test: test-frontend test-backend

test-backend:
	$(COMPOSE_DEV) run --rm backend pytest .

test-frontend:
	$(COMPOSE_DEV) run --rm frontend sh -c "CI=true yarn test"

e2e-electron:
	$(COMPOSE_CYPRESS) up --exit-code-from e2e-electron

%: #Ignores unknown commands (and extra params)
	@:

