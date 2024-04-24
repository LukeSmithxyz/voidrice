#!/bin/bash

# A helper script for LaTeX/groff files used by `compiler` and `opout`.
# The user can add the root file of a larger project as a comment as below:
# % root = mainfile.tex
# And the compiler script will run on that instead of the opened file.

texroot="$(grep -i "^.\+\s*root\s*=\s*\S\+" "$1")"
texroot="${texroot##*=}"
texroot="${texroot//[\"\' ]}"

[ -f "$texroot" ] && readlink -f "$texroot" || exit 1
