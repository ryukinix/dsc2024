# ITA data science challenge 2024

ref: https://comp.ita.br/dsc/edicoes/2024/

Live demo at https://airdelay.manoel.dev and final [presentation].

[presentation]: https://docs.google.com/presentation/d/e/2PACX-1vSwBhQqeJUUEVwybUGQqj4d-X4YCD1GQj3zUwGKxKU7kXSSIUQjWb2sYP85RhLngQ/pub?start=true&loop=false&delayms=30000#slide=id.p1

# Setup / Run notebook

Ensure you have [pdm] installed, then run in the roof of the
repository:

``` shell
pdm install
```

Then, [dvc]¹ is installed as dev dependency, you can setup dvc folders
running:

``` shell
pdm run dvc pull
```

To run later the jupyterlab with the lib `dsc2024` installed, run:

``` shell
pdm notebook
```

[dvc]: https://dvc.org/
[pdm]: https://pdm-project.org/en/latest/


¹ You need proper google drive permisssion to run `dvc pull` and
retrieve datasets. Request permission from some member of the team.

# Team

- Manoel Vilela
- Jorge Franco
