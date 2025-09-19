ENV_FILE=.env.development

NAME_COMPOSE=c2s_challenge

CMD_COMPOSE=docker compose --env-file $(ENV_FILE)

up:
	$(CMD_COMPOSE) -p $(NAME_COMPOSE) up -d --build

down:
	$(CMD_COMPOSE) down -v

logs:
	$(CMD_COMPOSE) logs -f