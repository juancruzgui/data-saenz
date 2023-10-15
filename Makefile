run_analysis:
	python sentiment_analysis/interface/main.py

run_test_api:
	uvicorn api.fast:app --reload
