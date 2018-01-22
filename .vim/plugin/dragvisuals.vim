" Vim global plugin for dragging virtual blocks
" Last change: Tue Jul 24 07:19:35 EST 2012
" Maintainer:	Damian Conway
" License:	This file is placed in the public domain.

"#########################################################################
"##                                                                     ##
"##  Add the following (uncommented) to your .vimrc...                  ##
"##                                                                     ##
"##     runtime plugin/dragvisuals.vim                                  ##
"##                                                                     ##
"##     vmap  <expr>  <LEFT>   DVB_Drag('left')                         ##
"##     vmap  <expr>  <RIGHT>  DVB_Drag('right')                        ##
"##     vmap  <expr>  <DOWN>   DVB_Drag('down')                         ##
"##     vmap  <expr>  <UP>     DVB_Drag('up')                           ##
"##     vmap  <expr>  D        DVB_Duplicate()                          ##
"##                                                                     ##
"##     " Remove any introduced trailing whitespace after moving...     ##
"##     let g:DVB_TrimWS = 1                                            ##
"##                                                                     ##
"##  Or, if you use the arrow keys for normal motions, choose           ##
"##  four other keys for block dragging. For example:                   ##
"##                                                                     ##
"##     vmap  <expr>  h        DVB_Drag('left')                         ##
"##     vmap  <expr>  l        DVB_Drag('right')                        ##
"##     vmap  <expr>  j        DVB_Drag('down')                         ##
"##     vmap  <expr>  k        DVB_Drag('up')                           ##
"##                                                                     ##
"##  Or:                                                                ##
"##                                                                     ##
"##     vmap  <expr>  <S-LEFT>   DVB_Drag('left')                       ##
"##     vmap  <expr>  <S-RIGHT>  DVB_Drag('right')                      ##
"##     vmap  <expr>  <S-DOWN>   DVB_Drag('down')                       ##
"##     vmap  <expr>  <S-UP>     DVB_Drag('up')                         ##
"##                                                                     ##
"##  Or even:                                                           ##
"##                                                                     ##
"##     vmap  <expr>   <LEFT><LEFT>   DVB_Drag('left')                  ##
"##     vmap  <expr>  <RIGHT><RIGHT>  DVB_Drag('right')                 ##
"##     vmap  <expr>   <DOWN><DOWN>   DVB_Drag('down')                  ##
"##     vmap  <expr>     <UP><UP>     DVB_Drag('up')                    ##
"##                                                                     ##
"#########################################################################


" If already loaded, we're done...
if exists("loaded_dragvirtualblocks")
    finish
endif
let loaded_dragvirtualblocks = 1

" Preserve external compatibility options, then enable full vim compatibility...
let s:save_cpo = &cpo
set cpo&vim

"====[ Implementation ]====================================

" Toggle this to stop trimming on drags...
if !exists('g:DVB_TrimWS')
    let g:DVB_TrimWS = 1
endif

function! DVB_Drag (dir)
    " No-op in Visual mode...
    if mode() ==# 'v'
        return "\<ESC>gv"

    " Do Visual Line drag indirectly via temporary nmap
    " (to ensure we have access to block position data)...
    elseif mode() ==# 'V'
        " Set up a temporary convenience...
        exec "nnoremap <silent><expr><buffer>  M  \<SID>Drag_Lines('".a:dir."')"

        " Return instructions to implement the move and reset selection...
        return '"vyM'

    " Otherwise do Visual Block drag indirectly via temporary nmap
    " (to ensure we have access to block position data)...
    else
        " Set up a temporary convenience...
        exec "nnoremap <silent><expr><buffer>  M  \<SID>Drag_Block('".a:dir."')"

        " Return instructions to implement the move and reset selection...
        return '"vyM'
    endif
endfunction

" Duplicate selected block and place to the right...
function! DVB_Duplicate ()
    exec "nnoremap <silent><expr><buffer>  M  \<SID>DuplicateBlock()"
    return '"vyM'
endfunction

function! s:DuplicateBlock ()
    nunmap <buffer>  M
    " Locate block boundaries...
    let [buf_left,  line_left,  col_left,  offset_left ] = getpos("'<")
    let [buf_right, line_right, col_right, offset_right] = getpos("'>")

    " Identify special '$' blocks...
    let dollar_block = 0
    let start_col    = min([col_left+offset_left, col_right+offset_right])
    let end_col      = max([col_left+offset_left, col_right+offset_right])
    let visual_width = end_col - start_col + 1
    for visual_line in split(getreg("v"),"\n")
        if strlen(visual_line) > visual_width
            let dollar_block = 1
            let visual_width = strlen(visual_line)
        endif
    endfor
    let square_up = (dollar_block ? (start_col+visual_width-2).'|' : '')

    set virtualedit=all
    return 'gv'.square_up.'yPgv'
        \. (visual_width-dollar_block) . 'lo' . (visual_width-dollar_block) . 'l'
        \. "y:set virtualedit=block\<CR>gv"
        \. (dollar_block ? 'o$' : '')
endfunction


" Kludge to hide change reporting inside implementation...
let s:NO_REPORT   = ":let b:DVB_report=&report\<CR>:let &report=1000000000\<CR>"
let s:PREV_REPORT = ":let &report = b:DVB_report\<CR>"


" Drag in specified direction in Visual Line mode...
function! s:Drag_Lines (dir)
    " Clean up the temporary convenience...
    nunmap <buffer>  M

    " Locate block being shifted...
    let [buf_left,  line_left,  col_left,  offset_left ] = getpos("'<")
    let [buf_right, line_right, col_right, offset_right] = getpos("'>")

    " Drag entire lines left if possible...
    if a:dir == 'left'
        " Are all lines indented at least one space???
        let lines        = getline(line_left, line_right)
        let all_indented = match(lines, '^[^ ]') == -1
        nohlsearch

        " If can't trim one space from start of each line, be a no-op...
        if !all_indented
            return 'gv'

        " Otherwise drag left by removing one space from start of each line...
        else
            return    s:NO_REPORT
                  \ . "gv:s/^ //\<CR>"
                  \ . s:PREV_REPORT
                  \ . "gv"
        endif

    " To drag entire lines right, add a space in column 1...
    elseif a:dir == 'right'
        return   s:NO_REPORT
             \ . "gv:s/^/ /\<CR>:nohlsearch\<CR>"
             \ . s:PREV_REPORT
             \ . "gv"

    " To drag entire lines upwards...
    elseif a:dir == 'up'
        let EOF = line('$')

        " Can't drag up if at first line...
        if line_left == 1 || line_right == 1
            return 'gv'

        " Needs special handling at EOF (because cursor moves up on delete)...
        elseif line_left == EOF || line_right == EOF
            let height = line_right - line_left
            let select_extra = height ? height . 'j' : ""
            return   s:NO_REPORT
                 \ . 'gvxP'
                 \ . s:PREV_REPORT
                 \ . 'V' . select_extra

        " Otherwise just cut-move-paste-reselect...
        else
            let height = line_right - line_left
            let select_extra = height ? height . 'j' : ""
            return   s:NO_REPORT
                 \ . 'gvxkP'
                 \ . s:PREV_REPORT
                 \ . 'V' . select_extra
        endif

    " To drag entire lines downwards...
    elseif a:dir == 'down'
        let EOF = line('$')

        " This is how much extra we're going to have to reselect...
        let height = line_right - line_left
        let select_extra = height ? height . 'j' : ""

        " Needs special handling at EOF (to push selection down into new space)...
        if line_left == EOF || line_right == EOF
            return   "O\<ESC>gv"

        " Otherwise, just cut-move-paste-reselect...
        else 
            return   s:NO_REPORT
                 \ . 'gvxp'
                 \ . s:PREV_REPORT
                 \ . 'V' . select_extra
        endif

    endif
endfunction

" Drag in specified direction in Visual Block mode...
function! s:Drag_Block (dir)
    " Clean up the temporary convenience...
    nunmap <buffer>  M

    " Locate block being shifted...
    let [buf_left,  line_left,  col_left,  offset_left ] = getpos("'<")
    let [buf_right, line_right, col_right, offset_right] = getpos("'>")

    " Identify special '$' blocks...
    let dollar_block = 0
    let start_col    = min([col_left+offset_left, col_right+offset_right])
    let end_col      = max([col_left+offset_left, col_right+offset_right])
    let visual_width = end_col - start_col + 1
    for visual_line in split(getreg("v"),"\n")
        if strlen(visual_line) > visual_width
            let dollar_block = 1
            let visual_width = strlen(visual_line)
        endif
    endfor
    let square_up = (dollar_block ? (start_col+visual_width-2).'|' : '')

    " Drag left...
    if a:dir == 'left'
        "Can't drag left at left margin...
        if col_left == 1 || col_right == 1
            return 'gv'

        " Otherwise reposition one column left (and optionally trim any whitespace)...
        elseif g:DVB_TrimWS
            " May need to be able to temporarily step past EOL...
            let prev_ve = &virtualedit
            set virtualedit=all

            " Are we moving past other text???
            let square_up_final = ""
            if dollar_block
                let lines = getline(line_left, line_right)
                if match(lines, '^.\{'.(start_col-2).'}\S') >= 0
                    let dollar_block = 0
                    let square_up_final = (start_col+visual_width-3).'|'
                endif
            endif

            let vcol = start_col - 2
            return   'gv'.square_up.'xhP'
                 \ . s:NO_REPORT
                 \ . "gvhoho:s/\\s*$//\<CR>gv\<ESC>"
                 \ . ':set virtualedit=' . prev_ve . "\<CR>"
                 \ . s:PREV_REPORT
                 \ . ":nohlsearch\<CR>gv"
                 \ . (dollar_block ? '$' : square_up_final )
        else
            return 'gv'.square_up.'xhPgvhoho'
        endif

    " Drag right...
    elseif a:dir == 'right'
        " May need to be able to temporarily step past EOL...
        let prev_ve = &virtualedit
        set virtualedit=all

        " Reposition block one column to the right...
        if g:DVB_TrimWS
            let vcol = start_col
            return   'gv'.square_up.'xp'
                 \ . s:NO_REPORT
                 \ . "gvlolo"
                 \ . ":s/\\s*$//\<CR>gv\<ESC>"
                 \ . ':set virtualedit=' . prev_ve . "\<CR>"
                 \ . s:PREV_REPORT
                 \ . (dollar_block ? 'gv$' : 'gv')
        else
            return 'gv'.square_up.'xp:set virtualedit=' . prev_ve . "\<CR>gvlolo"
        endif

    " Drag upwards...
    elseif a:dir == 'up'
        " Can't drag upwards at top margin...
        if line_left == 1 || line_right == 1
            return 'gv'
        endif

        " May need to be able to temporarily step past EOL...
        let prev_ve = &virtualedit
        set virtualedit=all

        " If trimming whitespace, jump to just below block to do it...
        if g:DVB_TrimWS
            let height = line_right - line_left + 1
            return  'gv'.square_up.'xkPgvkoko"vy'
                    \ . height
                    \ . 'j:s/\s*$//'
                    \ . "\<CR>:nohlsearch\<CR>:set virtualedit="
                    \ . prev_ve
                    \ . "\<CR>gv"
                    \ . (dollar_block ? '$' : '')

        " Otherwise just move and reselect...
        else
            return   'gv'.square_up.'xkPgvkoko"vy:set virtualedit='
                    \ . prev_ve
                    \ . "\<CR>gv"
                    \ . (dollar_block ? '$' : '')
        endif

    " Drag downwards...
    elseif a:dir == 'down'
        " May need to be able to temporarily step past EOL...
        let prev_ve = &virtualedit
        set virtualedit=all

        " If trimming whitespace, move to just above block to do it...
        if g:DVB_TrimWS
            return   'gv'.square_up.'xjPgvjojo"vyk:s/\s*$//'
                    \ . "\<CR>:nohlsearch\<CR>:set virtualedit="
                    \ . prev_ve
                    \ . "\<CR>gv"
                    \ . (dollar_block ? '$' : '')

        " Otherwise just move and reselect...
        else
            return   'gv'.square_up.'xjPgvjojo"vy'
                    \ . "\<CR>:set virtualedit="
                    \ . prev_ve
                    \ . "\<CR>gv"
                    \ . (dollar_block ? '$' : '')
        endif
    endif
endfunction


" Restore previous external compatibility options
let &cpo = s:save_cpo

