#!/usr/bin/env bash
# Complete and verify the project-local TeX installation, including German PDFs.
set -euo pipefail
repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$repo_dir/scripts/activate.sh"

extra_files=(luatexbase.sty ctablestack.sty ngerman.ldf selnolig.sty loadhyph-de-1996.tex)
install_extra=false
for tex_file in "${extra_files[@]}"; do
  if ! kpsewhich "$tex_file" >/dev/null; then
    install_extra=true
    break
  fi
done
if [[ "$install_extra" == true ]]; then
  # The fixed TinyTeX bundle can contain an older manager than the repository
  # requires. Update only the manager before installing the missing packages.
  echo "Updating the TeX Live package manager from $TEXLIVE_REPOSITORY"
  tlmgr --verify-repo=all --repository "$TEXLIVE_REPOSITORY" update --self
  echo "Installing German LuaLaTeX dependencies from $TEXLIVE_REPOSITORY"
  tlmgr --verify-repo=all --repository "$TEXLIVE_REPOSITORY" install "${TEXLIVE_EXTRA_PACKAGES[@]}"
fi

for tex_file in "${extra_files[@]}" tcolorbox.sty sectsty.sty needspace.sty adjustbox.sty texgyreheros-regular.otf; do
  kpsewhich "$tex_file" >/dev/null || {
    echo "Required TeX file is missing after setup: $tex_file" >&2
    exit 1
  }
done

# File presence alone misses transitive dependencies and language configuration.
check_dir="$(mktemp -d "$DHBW_TOOLCHAIN_DIR/.tex-check.XXXXXX")"
trap 'rm -rf -- "$check_dir"' EXIT
mkdir -p "$DHBW_TOOLCHAIN_DIR/checks"
check_log="$DHBW_TOOLCHAIN_DIR/checks/tex-smoke.log"
if ! lualatex -no-shell-escape -interaction=nonstopmode -halt-on-error \
    -output-directory="$check_dir" "$repo_dir/scripts/tex-smoke.tex" > "$check_log" 2>&1; then
  cat "$check_log" >&2
  echo "German LuaLaTeX check failed; log: $check_log" >&2
  exit 1
fi
if [[ ! -s "$check_dir/tex-smoke.pdf" ]]; then
  echo "German LuaLaTeX check produced no PDF; log: $check_log" >&2
  exit 1
fi
echo "German LuaLaTeX handout check passed. Log: $check_log"
