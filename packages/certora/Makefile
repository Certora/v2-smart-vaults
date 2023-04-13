default: help

PATCH         = applyHarness.patch
CONTRACTS_DIR = ../contracts
MUNGED_DIR    = ./munged
SmartVault_Origin = ../../node_modules/@mimic-fi/v2-smart-vault/contracts/SmartVault.sol
SmartVault_munged = ./munged/SmartVault.sol


help:
	@echo "usage:"
	@echo "  make clean:  remove all generated files (those ignored by git)"
	@echo "  make $(MUNGED_DIR): create $(MUNGED_DIR) directory by applying the patch file to $(CONTRACTS_DIR)"
	@echo "  make record: record a new patch file capturing the differences between $(CONTRACTS_DIR) and $(MUNGED_DIR)"

munge:
	cp $(SmartVault_Origin) $(MUNGED_DIR)
	patch -d $(MUNGED_DIR) < $(PATCH)

record:
	diff -burN $(SmartVault_Origin) $(SmartVault_munged) | sed 's+\$(SmartVault_Origin)/++g' | sed 's+$(SmartVault_munged)++g' > $(PATCH)

clean:
	git clean -fdX
	touch $(PATCH)