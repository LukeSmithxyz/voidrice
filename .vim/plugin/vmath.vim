" Vim global plugin for math on visual regions
" Maintainer:	Damian Conway
" License:	This file is placed in the public domain.

"######################################################################
"##                                                                  ##
"##  To use:                                                         ##
"##                                                                  ##
"##     vmap <expr>  ++  VMATH_YankAndAnalyse()                      ##
"##     nmap         ++  vip++                                       ##
"##                                                                  ##
"##  (or whatever keys you prefer to remap these actions to)         ##
"##                                                                  ##
"######################################################################


" If already loaded, we're done...
if exists("loaded_vmath")
    finish
endif
let loaded_vmath = 1

" Preserve external compatibility options, then enable full vim compatibility...
let s:save_cpo = &cpo
set cpo&vim

" Grab visual selection and do simple math on it...
function! VMATH_YankAndAnalyse ()
    if &showmode
        " Don't reselect the visual region if showmode is enabled
        " because it will clobber the sum/avg/etc report with the
        " "-- VISUAL --" message.
        return "y:call VMATH_Analyse()\<CR>"
    else
        return "y:call VMATH_Analyse()\<CR>gv"
    endif
endfunction

" What to consider a number...
let s:NUM_PAT = '^[+-]\?\d\+\%([.]\d\+\)\?\([eE][+-]\?\d\+\)\?$'

" How widely to space the report components...
let s:REPORT_GAP = 3  "spaces between components

" Do simple math on current yank buffer...
function! VMATH_Analyse ()
    " Extract data from selection...
    let selection = getreg('')
    let raw_numbers = filter(split(selection), 'v:val =~ s:NUM_PAT')
    let numbers = map(copy(raw_numbers), 'str2float(v:val)')

    " Results include a newline if original selection did...
    let newline = selection =~ "\n" ? "\n" : ""

    " Calculate and en-register various interesting metrics...
    let summation = len(numbers) ? join( numbers, ' + ') : '0'
    call setreg('s', s:tidy( eval( summation )      )) " Sum     --> register s
    call setreg('a',         s:average(raw_numbers)  ) " Average --> register a
    call setreg('x', s:tidy( s:max(numbers)         )) " Max     --> register x
    call setreg('n', s:tidy( s:min(numbers)         )) " Min     --> register n
    call setreg('r',         @n . ' to ' . @x        ) " Range   --> register r
    call setreg('c', len(numbers)                    ) " Count   --> register c

    " Default paste buffer should depend on original contents (TODO)
    call setreg('', @s )

    " Report...
    let gap = repeat(" ", s:REPORT_GAP)
    highlight NormalUnderlined term=underline cterm=underline gui=underline
    echohl NormalUnderlined
    echo  's'
    echohl NONE
    echon  'um: ' . @s . gap
    echohl NormalUnderlined
    echon 'a'
    echohl NONE
    echon  'vg: ' . @a . gap
    echon 'mi'
    echohl NormalUnderlined
    echon   'n'
    echohl NONE
    echon    ': ' . @n . gap
    echon 'ma'
    echohl NormalUnderlined
    echon   'x'
    echohl NONE
    echon    ': ' . @x . gap
    echohl NormalUnderlined
    echon  'c'
    echohl NONE
    echon  'ount: ' . @c

endfunction

" Prettify numbers...
function! s:tidy (number)
    let tidied = printf('%g', a:number)
    return substitute(tidied, '[.]0\+$', '', '')
endfunction

" Compute average with meaningful number of decimal places...
function! s:average (numbers)
    " Compute average...
    let summation = eval( len(a:numbers) ? join( a:numbers, ' + ') : '0' )
    let avg = 1.0 * summation / s:max([len(a:numbers), 1])

    " Determine significant figures...
    let min_decimals = 15
    for num in a:numbers
        let decimals = strlen(matchstr(num, '[.]\d\+$')) - 1
        if decimals < min_decimals
            let min_decimals = decimals
        endif
    endfor

    " Adjust answer...
    return min_decimals > 0 ? printf('%0.'.min_decimals.'f', avg)
    \                       : string(avg)
endfunction

" Reimplement these because the builtins don't handle floats (!!!)
function! s:max (numbers)
    if !len(a:numbers)
        return 0
    endif
    let numbers = copy(a:numbers)
    let maxnum = numbers[0]
    for nextnum in numbers[1:]
        if nextnum > maxnum
            let maxnum = nextnum
        endif
    endfor
    return maxnum
endfunction

function! s:min (numbers)
    if !len(a:numbers)
        return 0
    endif
    let numbers = copy(a:numbers)
    let minnum = numbers[0]
    for nextnum in numbers[1:]
        if nextnum < minnum
            let minnum = nextnum
        endif
    endfor
    return minnum
endfunction


" Restore previous external compatibility options
let &cpo = s:save_cpo
