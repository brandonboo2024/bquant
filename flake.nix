{
  description = "dev shell for python";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
  };

  outputs = inputs@{
    self, nixpkgs, ...
  }:
  let 
    pkgs = import nixpkgs{
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
    '';
  };
}
