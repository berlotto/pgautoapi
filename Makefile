
.DEFAULT_GOAL = help

# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo " "
	@echo "PGAUTOAPI"
	@echo " "
	@echo "  make debug     : Para executar local para desenvolvimento"
	@echo " "

debug:
	uvicorn main:app --reload
