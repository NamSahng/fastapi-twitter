PYTHON=3.8
BASENAME=$(notdir $(abspath $(CURDIR)/..))
CONDA_CH=conda-forge defaults

env:
	conda create -n $(BASENAME)  python=$(PYTHON)

setup:
	conda install --file requirements.txt $(addprefix -c ,$(CONDA_CH))
