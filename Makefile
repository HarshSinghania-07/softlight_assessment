# ===============================
# Makefile for UI State Capture Agent
# ===============================
# Usage examples:
#   make linear-view
#   make linear-login
#   make linear-scroll
#   make notion-pricing
#   make test-all
#   make clean

PYTHON := python
MAIN := main.py
VENV := venv
ACTIVATE := source $(VENV)/bin/activate

# -------------------------------------
# Linear workflows
# -------------------------------------
linear-view:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Linear --workflow view_landing_page

linear-login:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Linear --workflow open_login_modal

linear-product:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Linear --workflow explore_product_page

linear-scroll:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Linear --workflow scroll_features_section

linear-hover:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Linear --workflow hover_resources_menu

# -------------------------------------
# Notion workflows
# -------------------------------------
notion-home:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Notion --workflow capture_homepage

notion-pricing:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Notion --workflow explore_pricing_modal

notion-signup:
	@$(ACTIVATE); $(PYTHON) $(MAIN) --app Notion --workflow simulate_signup_flow

# -------------------------------------
# Run everything sequentially
# -------------------------------------
test-all:
	@echo "🚀 Running all Linear + Notion workflows..."
	@$(ACTIVATE); \
	for app in Linear Notion; do \
		for wf in view_landing_page open_login_modal explore_product_page scroll_features_section hover_resources_menu capture_homepage explore_pricing_modal simulate_signup_flow; do \
			echo "▶️ Running $$app - $$wf"; \
			$(PYTHON) $(MAIN) --app $$app --workflow $$wf; \
			echo "✅ Completed $$app - $$wf"; \
		done; \
	done
