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
        stdenv.cc.cc.lib
        python313
        uv
        openssl
        zlib
      ];
      # assign correct paths for binaries and libraries for dev shell
      # auto enter venv in uv and check
      shellHook = ''
        export UV_LINK_MODE=copy
        export UV_PYTHON=${pkgs.python3}/bin/python3

        export PKG_CONFIG_PATH=${pkgs.openssl.dev}/lib/pkgconfig:$PKG_CONFIG_PATH
        export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt

        export LD_LIBRARY_PATH=${
          pkgs.lib.makeLibraryPath [
            pkgs.stdenv.cc.cc.lib
            pkgs.zlib
            pkgs.openssl
            pkgs.glibc
          ]
        }:$LD_LIBRARY_PATH

        uv sync --quiet
        if [ -d ".venv" ]; then
          . .venv/bin/activate
        fi

        echo "dev environment loaded"
        echo "$(which python3)";
        ''; # should show python 3.13
    };
  };
}
