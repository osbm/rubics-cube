{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
    ...
  }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
    };
  in {
    packages."${system}" = {
      rubics-cube = pkgs.python3Packages.buildPythonPackage rec {
        pname = "rubic-cube";
        version = "0.1.0";

        src = ./.;

        # do not run tests
        doCheck = false;
        # specific to buildPythonPackage, see its reference
        pyproject = true;
        build-system = with pkgs.python3Packages; [
          setuptools
          setuptools-scm # wtf is this
        ];
        propagatedBuildInputs = with pkgs.python3Packages; [
          numpy
          matplotlib
        ];
        pythonImportsCheck = ["rubics_cube"];
      };
      default = self.packages."${system}".rubics-cube;
    };
  };
}
