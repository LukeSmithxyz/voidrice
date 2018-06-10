let g:ProseOn=0

function! ToggleProse()
    if !g:ProseOn
        call Prose()
    else
        call ProseOff()
    endif
endfunction

function! Prose()
    echo "Prose: On"
    let g:ProseOn=1

    noremap j gj
    noremap k gk
    noremap 0 g0
    noremap $ g$
    noremap A g$a
    noremap I g0i
    setlocal linebreak nonumber norelativenumber t_Co=0 foldcolumn=2
    hi! link FoldColumn Normal

endfunction

function! ProseOff()
    echo "Prose: Off"
    let g:ProseOn=0

    noremap j j
    noremap k k
    noremap 0 0
    noremap $ $
    noremap A A
    noremap I I
    setlocal nolinebreak number relativenumber t_Co=256 foldcolumn=0

endfunction
