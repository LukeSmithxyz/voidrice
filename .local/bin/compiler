#!/bin/sh

# This script will compile or run another finishing operation on a document. I
# have this script run via vim.

# Compiles .tex. groff (.mom, .ms), .rmd, .md, .org.  Opens .sent files as sent
# presentations. Runs scripts based on extension or shebang.

# Note that .tex files which you wish to compile with XeLaTeX should have the
# string "xelatex" somewhere in a comment/command in the first 5 lines.

file="${1}"
ext="${file##*.}"
dir=${file%/*}
base="${file%.*}"

cd "${dir}" || exit "1"

case "${ext}" in
    [0-9]) preconv "${file}" | refer -PS -e | groff -mandoc -T pdf > "${base}.pdf" ;;
    mom|ms) preconv "${file}" | refer -PS -e | groff -T pdf -m"${ext}" > "${base}.pdf" ;;
    c) cc "${file}" -o "${base}" && "./${base}" ;;
    cpp) g++ "${file}" -o "${base}" && "./${base}" ;;
    cs) mcs "${file}" && mono "${base}.exe" ;;
    go) go run "${file}" ;;
    h) sudo make install ;;
    java) javac -d classes "${file}" && java -cp classes "${base}" ;;
    m) octave "${file}" ;;
    md) [ -x "$(command -v lowdown)" ] && \
	    lowdown --parse-no-intraemph "${file}" -Tms | groff -mpdfmark -ms -kept -T pdf > "${base}.pdf" || \
	    [ -x "$(command -v groffdown)" ] && \
	    groffdown -i "${file}" | groff -T pdf > "${base}.pdf" || \
	    pandoc -t ms --highlight-style="kate" -s -o "${base}.pdf" "${file}" ;;
    org) emacs "${file}" --batch -u "${USER}" -f org-latex-export-to-pdf ;;
    py) python "${file}" ;;
    [rR]md) Rscript -e "rmarkdown::render('${file}', quiet=TRUE)" ;;
    rs) cargo build ;;
    sass) sassc -a "${file}" "${base}.css" ;;
    scad) openscad -o "${base}.stl" "${file}" ;;
    sent) setsid -f sent "${file}" 2> "/dev/null" ;;
    tex)
	    textarget="$(getcomproot "${file}" || echo "${file}")"
	    command="pdflatex"
	    head -n5 "${textarget}" | grep -qi "xelatex" && command="xelatex"
	    ${command} --output-directory="${textarget%/*}" "${textarget%.*}" &&
	    grep -qi addbibresource "${textarget}" &&
	    biber --input-directory "${textarget%/*}" "${textarget%.*}" &&
	    ${command} --output-directory="${textarget%/*}" "${textarget%.*}" &&
	    ${command} --output-directory="${textarget%/*}" "${textarget%.*}"
	    ;;
    *) sed -n '/^#!/s/^#!//p; q' "${file}" | xargs -r -I % "${file}" ;;
esac
