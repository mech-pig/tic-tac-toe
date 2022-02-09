let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2022-02-08";
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "refs/heads/nixos-unstable";
    rev = "9f697d60e4d9f08eacf549502528bfaed859d33b";
  };

  pkgs = import nixpkgs {};
in
  pkgs.mkShell {
    buildInputs = [
      pkgs.poetry
      pkgs.python310
    ];
  }