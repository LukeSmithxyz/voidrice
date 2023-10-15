#!/bin/dash

BIB_FILE="$HOME/latex/uni.bib"

correction_method() {
    sed -n -E 's/.*((DOI|doi)((\.(org))?\/?|:? *))([^: ]+[^ .]).*/doi:\6/p; T; q'
}

get_doi_from_pdf() {
    pdf="$1"
    doi=$(pdfinfo "$pdf" 2>/dev/null | correction_method)
    [ -z "$doi" ] && doi=$(pdftotext -q -l 2 "$pdf" - 2>/dev/null | correction_method)
    [ -z "$doi" ] && echo "No DOI found for PDF: $pdf" >&2 && return 1
    echo "$doi"
}

correct_names() {
    sed '/^@[a-z]\+{[^[:space:]]\+[0-9]\{4\},/{
    s/\([A-Z]\)/\L\1/g
    s/_//g
    s/[0-9]*\([0-9]\{2\}\)/\1/g
  }'
}

normalize_doi() {
    doi="$1"
    doi=$(echo "$doi" | sed 's@%@\\x@g' | xargs -I {} printf "%b" "{}")
    printf "%s" "$doi" | tr 'A-Z' 'a-z'
}

process_doi() {
    doi="$1"
    bibtex_entry=$(curl -s "https://api.crossref.org/works/$doi/transform/application/x-bibtex" -w "\\n" | correct_names)
    red_color='\033[0;31m'
    reset_color='\033[0m'

    printf "${red_color}%s${reset_color}\n" "$bibtex_entry"
    [ -z "$bibtex_entry" ] && [ "$(echo "$bibtex_entry" | cut -c2)" != "@" ] && echo "Failed to fetch bibtex entry for DOI: $doi" && return 1

    normalized_doi="${doi#doi:}"
    grep -q -E "doi\s*=\s*\{$(echo "$normalized_doi" | sed 's/(/\\(/g')\}" "$BIB_FILE" || {
        [ -s "$BIB_FILE" ] && echo "" >> "$BIB_FILE"
        echo "$bibtex_entry" >> "$BIB_FILE"
        echo "Added bibtex entry for DOI: $doi"
        return 1
    }
    echo "Bibtex entry for DOI: $doi already exists in the file."
}

[ -z "$1" ] && echo "Give either a pdf file or a DOI or a directory path that has PDFs as an argument." && exit 1

[ -d "$1" ] && {
    for pdf in "$1"/*.pdf; do
        doi=$(get_doi_from_pdf "$pdf")
        [ -n "$doi" ] && {
            doi=$(normalize_doi "$doi")
            process_doi "$doi"
        }
    done
    exit 1
}

[ -f "$1" ] && [ "$(echo "$1" | grep -c "\.pdf$")" -ne 0 ] && {
    doi=$(get_doi_from_pdf "$1")
    [ -n "$doi" ] && {
        doi=$(normalize_doi "$doi")
        process_doi "$doi"
    }
    exit 1
}

doi=$(echo "$1" | correction_method)
[ -n "$doi" ] && {
    doi=$(normalize_doi "$doi")
    process_doi "$doi"
}
