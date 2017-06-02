" # Configuration
if !exists('g:instant_markdown_slow')
    let g:instant_markdown_slow = 0
endif

if !exists('g:instant_markdown_autostart')
    let g:instant_markdown_autostart = 1
endif

if !exists('g:instant_markdown_open_to_the_world')
    let g:instant_markdown_open_to_the_world = 0
endif

if !exists('g:instant_markdown_allow_unsafe_content')
    let g:instant_markdown_allow_unsafe_content = 0
endif

if !exists('g:instant_markdown_allow_external_content')
    let g:instant_markdown_allow_external_content = 1
endif

" # Utility Functions
" Simple system wrapper that ignores empty second args
function! s:system(cmd, stdin)
    if strlen(a:stdin) == 0
        call system(a:cmd)
    else
        call system(a:cmd, a:stdin)
    endif
endfu

" Wrapper function to automatically execute the command asynchronously and
" redirect output in a cross-platform way. Note that stdin must be passed as a
" List of lines.
function! s:systemasync(cmd, stdinLines)
    if has('win32') || has('win64')
        call s:winasync(a:cmd, a:stdinLines)
    else
        let cmd = a:cmd . '&>/dev/null &'
        call s:system(cmd, join(a:stdinLines, "\n"))
    endif
endfu

" Executes a system command asynchronously on Windows. The List stdinLines will
" be concatenated and passed as stdin to the command. If the List is empty,
" stdin will also be empty.
function! s:winasync(cmd, stdinLines)
    " To execute a command asynchronously on windows, the script must use the
    " "!start" command. However, stdin can't be passed to this command like
    " system(). Instead, the lines are saved to a file and then piped into the
    " command.
    if len(a:stdinLines)
        let tmpfile = tempname()
        call writefile(a:stdinLines, tmpfile)
        let command = 'type ' . tmpfile . ' | ' . a:cmd
    else
        let command = a:cmd
    endif
    exec 'silent !start /b cmd /c ' . command . ' > NUL'
endfu

function! s:refreshView()
    let bufnr = expand('<bufnr>')
    call s:systemasync("curl -X PUT -T - http://localhost:8090",
                \ s:bufGetLines(bufnr))
endfu

function! s:startDaemon(initialMDLines)
    let env = ''
    if g:instant_markdown_open_to_the_world
        let env .= 'INSTANT_MARKDOWN_OPEN_TO_THE_WORLD=1 '
    endif
    if g:instant_markdown_allow_unsafe_content
        let env .= 'INSTANT_MARKDOWN_ALLOW_UNSAFE_CONTENT=1 '
    endif
    if !g:instant_markdown_allow_external_content
        let env .= 'INSTANT_MARKDOWN_BLOCK_EXTERNAL=1 '
    endif

    call s:systemasync('instant-markdown-d', a:initialMDLines)
endfu

function! s:initDict()
    if !exists('s:buffers')
        let s:buffers = {}
    endif
endfu

function! s:pushBuffer(bufnr)
    call s:initDict()
    let s:buffers[a:bufnr] = 1
endfu

function! s:popBuffer(bufnr)
    call s:initDict()
    call remove(s:buffers, a:bufnr)
endfu

function! s:killDaemon()
    call s:systemasync("curl -s -X DELETE http://localhost:8090", [])
endfu

function! s:bufGetLines(bufnr)
  return getbufline(a:bufnr, 1, "$")
endfu

" I really, really hope there's a better way to do this.
fu! s:myBufNr()
    return str2nr(expand('<abuf>'))
endfu

" # Functions called by autocmds
"
" ## push a new Markdown buffer into the system.
"
" 1. Track it so we know when to garbage collect the daemon
" 2. Start daemon if we're on the first MD buffer.
" 3. Initialize changedtickLast, possibly needlessly(?)
fu! s:pushMarkdown()
    let bufnr = s:myBufNr()
    call s:initDict()
    if len(s:buffers) == 0
        call s:startDaemon(s:bufGetLines(bufnr))
    endif
    call s:pushBuffer(bufnr)
    let b:changedtickLast = b:changedtick
endfu

" ## pop a Markdown buffer
"
" 1. Pop the buffer reference
" 2. Garbage collection
"     * daemon
"     * autocmds
fu! s:popMarkdown()
    let bufnr = s:myBufNr()
    silent au! instant-markdown * <buffer=abuf>
    call s:popBuffer(bufnr)
    if len(s:buffers) == 0
        call s:killDaemon()
    endif
endfu

" ## Refresh if there's something new worth showing
"
" 'All things in moderation'
fu! s:temperedRefresh()
    if !exists('b:changedtickLast')
        let b:changedtickLast = b:changedtick
    elseif b:changedtickLast != b:changedtick
        let b:changedtickLast = b:changedtick
        call s:refreshView()
    endif
endfu

fu! s:previewMarkdown()
  call s:startDaemon(getline(1, '$'))
  aug instant-markdown
    if g:instant_markdown_slow
      au CursorHold,BufWrite,InsertLeave <buffer> call s:temperedRefresh()
    else
      au CursorHold,CursorHoldI,CursorMoved,CursorMovedI <buffer> call s:temperedRefresh()
    endif
    au BufWinLeave <buffer> call s:cleanUp()
  aug END
endfu

fu! s:cleanUp()
  call s:killDaemon()
  au! instant-markdown * <buffer>
endfu

if g:instant_markdown_autostart
    " # Define the autocmds "
    aug instant-markdown
        au! * <buffer>
        au BufEnter <buffer> call s:refreshView()
        if g:instant_markdown_slow
          au CursorHold,BufWrite,InsertLeave <buffer> call s:temperedRefresh()
        else
          au CursorHold,CursorHoldI,CursorMoved,CursorMovedI <buffer> call s:temperedRefresh()
        endif
        au BufWinLeave <buffer> call s:popMarkdown()
        au BufwinEnter <buffer> call s:pushMarkdown()
    aug END
else
    command! -buffer InstantMarkdownPreview call s:previewMarkdown()
endif
