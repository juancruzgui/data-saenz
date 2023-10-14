run_analysis:
	python interface/main.py

run_test_api:
	uvicorn api.fast:app --reload
