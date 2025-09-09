.PHONY: test test-verbose clean install

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Run tests using the custom test runner
test:
	python run_tests.py

# Run tests with verbose output
test-verbose:
	python -u run_tests.py

# Run tests using pytest (if you want to keep the option)
test-pytest:
	pytest tests/ -v

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run CDK synth
synth:
	cdk synth

# Run CDK deploy
deploy:
	cdk deploy

# Run CDK destroy
destroy:
	cdk destroy

