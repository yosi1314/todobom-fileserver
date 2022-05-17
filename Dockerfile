FROM python:3.10 as poetryexporter

# add poetry's installation path to PATH
ENV PATH="${PATH}:/root/.local/bin"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

COPY ./pyproject.toml ./poetry.lock* /

RUN poetry export --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.10

COPY --from=poetryexporter requirements.txt /

RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
