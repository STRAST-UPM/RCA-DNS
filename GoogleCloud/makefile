
.PHONY: deploy-infraestructure delete-infraestructure \
		deploy-services delete-services

GOOGLE_CLOUD_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GOOGLE_CLOUD_SCRIPTS_DIR := $(GOOGLE_CLOUD_DIR)/scripts
GOOGLE_CLOUD_ENV_FILE := $(GOOGLE_CLOUD_DIR)/.env

define run_with_loaded_environment
	bash -lc 'set -euo pipefail; \
		if [[ ! -f "$(GOOGLE_CLOUD_ENV_FILE)" ]]; then \
			echo "[ERROR] Missing env file: $(GOOGLE_CLOUD_ENV_FILE)" >&2; \
			echo "Copy .env.example to .env and adjust values before running scripts." >&2; \
			exit 1; \
		fi; \
		set -a; \
		source "$(GOOGLE_CLOUD_ENV_FILE)"; \
		set +a; \
		source "$(GOOGLE_CLOUD_SCRIPTS_DIR)/bootstrap.sh"; \
		bootstrap_load_scripts; \
		$(1)'
endef


###############################################################################
# Targets
###############################################################################

deploy-infraestructure:
	$(call run_with_loaded_environment,deploy_infraestructure_main)

delete-infraestructure:
	$(call run_with_loaded_environment,delete_infraestructure_main)

deploy-services:
	$(call run_with_loaded_environment,deploy_services_main)

delete-services:
	$(call run_with_loaded_environment,delete_services_main)
