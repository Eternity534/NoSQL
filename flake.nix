{
  description = "Flake pour projet Flask + MongoDB + Seaborn + Matplotlib + NumPy + Pandas sur Python 3.13";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
    in {
      devShell = pkgs.mkShell {
        buildInputs = [
          pkgs.python313Full
          pkgs.gcc # libstdc++ nécessaire pour NumPy
          pkgs.python313Packages.numpy
          pkgs.python313Packages.matplotlib
          pkgs.python313Packages.seaborn
          pkgs.python313Packages.pandas
          pkgs.python313Packages.flask
          pkgs.python313Packages.pymongo
          pkgs.python313Packages.pip
          pkgs.python313Packages.neo4j
        ];

        shellHook = ''
            # Installer Flask-PyMongo via pip si pas déjà présent
            python3 -m venv .venv
            source .venv/bin/activate
            pip install Flask-PyMongo==3.0.1
          exec zsh
        '';
      };
    });
}
