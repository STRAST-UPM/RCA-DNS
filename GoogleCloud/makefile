.PHONY: deploy-infraestructure delete-infraestructure \
		deploy-service delete-service

GOOGLE_CLOUD_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GOOGLE_CLOUD_SCRIPTS_DIR := $(GOOGLE_CLOUD_DIR)/scripts
GOOGLE_CLOUD_AUXILIAR_FUNCTIONS_DIR := $(GOOGLE_CLOUD_DIR)/auxiliar
ENV_FILE := $(GOOGLE_CLOUD_DIR)/.env
LOG_DIR := $(GOOGLE_CLOUD_DIR)/logs
LOG_FILE := $(LOG_DIR)/log_$(shell date +%Y-%m-%d_%H-%M-%S).log

# Load environment variables from root .env and optional service .env.
# $(1): service directory under services (e.g. ingress)
define load_env
	set -a; \
	[ -f "$(ENV_FILE)" ] && . "$(ENV_FILE)"; \
	[ -n "$(1)" ] && [ -f "$(SERVICES_DIR)/$(1)/.env" ] && . "$(SERVICES_DIR)/$(1)/.env"; \
	set +a
endef

# Load auxiliar functions
define load_auxiliar_function
	bash $(GOOGLE_CLOUD_AUXILIAR_FUNCTIONS_DIR)/logs.sh
	bash $(GOOGLE_CLOUD_AUXILIAR_FUNCTIONS_DIR)/utils.sh
	bash $(GOOGLE_CLOUD_AUXILIAR_FUNCTIONS_DIR)/gc_resources.sh
endef

###############################################################################
# Targets
###############################################################################

deploy-infraestructure:
	bash $(GOOGLE_CLOUD_SCRIPTS_DIR)/deploy_infraestructure.sh

delete-infraestructure:
	bash $(GOOGLE_CLOUD_SCRIPTS_DIR)/delete_infraestructure.sh

deploy-services:
	bash $(GOOGLE_CLOUD_SCRIPTS_DIR)/deploy_services.sh

delete-services:
	bash $(GOOGLE_CLOUD_SCRIPTS_DIR)/delete_services.sh
