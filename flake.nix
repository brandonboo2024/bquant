{
  description = "dev shell for python";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = inputs@{
    self, nixpkgs, ...
  }:
  let 
    system = "x86_64-linux";
  in {
    devShells."${system}".default = let
      pkgs = import nixpkgs{
        inherit system;
        config.allowUnfree = true;
      };
    in pkgs.mkShell{
      packages = with pkgs; [
        python313
          python313Packages.numpy
          python313Packages.pandas
          python313Packages.matplotlib
          python313Packages.yfinance
          python313Packages.scipy
      ];

      shellHook = ''
        echo "dev environment loaded"
        echo "`python --version`";
        ''; # should show python 3.13
    };
  };
}
