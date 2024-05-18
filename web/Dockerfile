ARG PYTHON_BASE=3.10-slim
# BUILD stage
FROM python:$PYTHON_BASE AS builder

# install PDM
RUN pip install -U pdm
# disable update check
ENV PDM_CHECK_UPDATE=false
# copy files
COPY pyproject.toml pdm.lock README.md /app/
COPY airdelay/ /app/airdelay

# install dependencies and app into the local packages directory
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache pdm install --check --prod --no-editable

### RUN stage
FROM python:$PYTHON_BASE

# retrieve packages from build stage
COPY --from=builder /app/.venv/ /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
# set command/entrypoint, adapt to fit your needs
COPY airdelay /app/airdelay
ADD tmp-datasets/catboost_regression.csv /app/datasets/catboost_regression.csv
ADD tmp-datasets/airport_geolocalization.csv /app/datasets/airport_geolocalization.csv
COPY .streamlit /app/.streamlit
# COPY templates /app/templates
# COPY static /app/static
EXPOSE 8501
CMD ["streamlit", "run", "/app/airdelay/main.py"]
