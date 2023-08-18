# Set up a new development environment
init:
	python -m pip install --upgrade pip
	pip install pip-tools
	$(MAKE) install
	pip install -e .
	pip check
	python -c "import nltk; nltk.download('punkt')"

# Install all dependencies
install:
	pip install -r requirements.txt

# Pin all dependencies
pin:
	pip-compile pyproject.toml -q --resolver=backtracking --no-emit-index-url -o requirements.txt

# Upgrade all dependencies
upgrade:
	pip-compile pyproject.toml -q --resolver=backtracking --no-emit-index-url --upgrade -o requirements.txt
	$(MAKE) install

# Run all code checks
checks: format lint type

# Check code formatting
format:
	black --check .

# Run linting
lint:
	ruff check .

# Run type checking
type:
	mypy .

reformat:
	black .
	ruff --fix .
