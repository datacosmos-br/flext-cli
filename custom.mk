# Project-owned custom Make targets for flext-cli
# This file is read by the generated Makefile but never generated itself.

# Custom gen target: also project agents-governance capsule to this project
_custom-gen:
	@echo "Projecting agents-governance capsule to flext-cli..."
	@cd "$(PROJECT_ROOT)" && python -c "from agents_governance import GovernanceBundle; from agents_governance.projection import project_from_bundle; from pathlib import Path; bundle = GovernanceBundle.load(Path('/home/marlonsc/agents')); project_from_bundle(Path('.'), bundle)"
