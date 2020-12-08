# UPA projekt 2020
FIT VUT Brno, in collaboration with [Mmat95](https://github.com/Mmat95).

Main content is in [UPA_project.ipynb]().

Uses [jupyterWith](https://github.com/tweag/jupyterWith) and [Nix](https://nixos.org/) flakes for infrastructure - a portable Jupyter server via `nix-shell`, and a PostgreSQL and a MongoDB server via a `systemd-nspawn` container (`nixos-container`) - see [flake.nix]().
