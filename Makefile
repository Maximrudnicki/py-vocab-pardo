run:
	python -m grpc_tools.protoc -I proto --python_out=. --pyi_out=. --grpc_python_out=. proto/*.proto
	python main.py
