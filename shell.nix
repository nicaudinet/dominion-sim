{ pkgs ? import <nixpkgs> {} }:

let

    python-with-my-packages = pkgs.python3.withPackages (p: with p; [
        ipython
        ipykernel
        jupyterlab
    ]);

in

    python-with-my-packages.env
