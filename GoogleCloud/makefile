
.DEFAULT_GOAL := help


.PHONY: help noop \
		deploy-infraestructure delete-infraestructure \
		deploy-services delete-services \
		update-gcr-container

GOOGLE_CLOUD_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
GOOGLE_CLOUD_SCRIPTS_DIR := $(GOOGLE_CLOUD_DIR)/scripts
GOOGLE_CLOUD_STATICS_DIR := $(GOOGLE_CLOUD_DIR)/statics
HELP_FILE := $(GOOGLE_CLOUD_STATICS_DIR)/help.txt

define bootstrap_run
	bash -lc 'set -euo pipefail; \
		source "$(GOOGLE_CLOUD_SCRIPTS_DIR)/bootstrap.sh"; \
		bootstrap_load_scripts; \
		$(1)'
endef


###############################################################################
# Targets
###############################################################################

help:
	@cat "$(HELP_FILE)"

noop:
	@:

deploy-infraestructure:
	$(call bootstrap_run,deploy_infraestructure_main)

delete-infraestructure:
	$(call bootstrap_run,delete_infraestructure_main)

deploy-services:
	$(call bootstrap_run,deploy_services_main)

delete-services:
	$(call bootstrap_run,delete_services_main)

update-gcr-container:
	$(call bootstrap_run,update_gcr_container)
