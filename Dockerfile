FROM ryukinix/pdm:3.11.2

COPY pyproject.toml setup.cfg pdm.lock /app/
RUN --mount=type=cache,target=/root/.cache pdm install --no-self

ADD README.md /app/
COPY dsc2024 /app/dsc2024
RUN pdm install

RUN chmod -R 777 /app /tmp
CMD ["pdm", "run", "dsc2024"]
