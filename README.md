# ITA data science challenge 2024

Competition description: https://comp.ita.br/dsc/edicoes/2024/

Live demo at https://airdelay.manoel.dev and final google
[presentation]. The live talk at ITA Engineering Education For The
Future event can be watch at [youtube] (PT-BR).

[presentation]: https://docs.google.com/presentation/d/e/2PACX-1vSwBhQqeJUUEVwybUGQqj4d-X4YCD1GQj3zUwGKxKU7kXSSIUQjWb2sYP85RhLngQ/pub?start=true&loop=false&delayms=30000#slide=id.p1
[youtube]: https://youtu.be/8dTiRw5rD_M?t=4678

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
