components = momentum/data.py momentum/executor.py momentum/screener.py momentum/signaller.py


main : $(components)
	uv run main.py

clean : 
	rm -r momentum/__pycache__
