
.PHONY: deploy-infraestructure delete-infraestructure deploy-services delete-services

GOOGLE_CLOUD_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GOOGLE_CLOUD_SCRIPTS_DIR := $(GOOGLE_CLOUD_DIR)/scripts

define run_with_loaded_scripts
	bash -lc 'set -euo pipefail; \
		source "$(GOOGLE_CLOUD_SCRIPTS_DIR)/bootstrap.sh"; \
		bootstrap_load_scripts; \
		$(1)'
endef


###############################################################################
# Targets
###############################################################################

deploy-infraestructure:
	$(call run_with_loaded_scripts,deploy_infraestructure_main)

delete-infraestructure:
	$(call run_with_loaded_scripts,delete_infraestructure_main)

deploy-services:
	$(call run_with_loaded_scripts,deploy_services_main)

delete-services:
	$(call run_with_loaded_scripts,delete_services_main)
