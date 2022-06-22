FROM python:3.10-buster
RUN pip3 install poetry
COPY . .
RUN poetry install
ENTRYPOINT ["poetry", "run", "python3", "validator.py"]