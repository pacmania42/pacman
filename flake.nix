{
  description = "Nix flake for pacman";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = nixpkgs.lib.systems.flakeExposed;

      perSystem =
        { pkgs, ... }:
        let
          x11Libs = with pkgs; [
            libX11
            libXrandr
            libXrender
            libXext
            libXcursor
            libXinerama
            libXi
            libXxf86vm
            libxcb
          ];

          glLibs = with pkgs; [
            libGL
          ];

          fontLibs = with pkgs; [
            freetype
            fontconfig
          ];
        in
        {
          devShells.default = pkgs.mkShellNoCC {
            packages = [
              pkgs.python313
              pkgs.uv
              pkgs.ruff
            ]
            ++ glLibs
            ++ x11Libs
            ++ fontLibs;
            env = {
              LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath (
                [ pkgs.stdenv.cc.cc.lib ] ++ glLibs ++ x11Libs ++ fontLibs
              );
              UV_PYTHON_DOWNLOADS = "never";
              UV_PYTHON = "${pkgs.python313}/bin/python3.13";
            };
          };
        };
    };
}
