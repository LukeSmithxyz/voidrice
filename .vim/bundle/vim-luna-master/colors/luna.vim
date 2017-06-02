" Name: Luna vim colorscheme
" Author: Pratheek
" URL: http://github.com/Pychimp/vim-luna
" (see this url for latest release & screenshots)
" License: MIT (see LICENSE.rst in the root of project)
" Created: In the middle of Earth's Rotation
" Version: 0.0.7
"
"
" TODO: {{{
" ---------------------------------------------------------------------
" -- Clean up !
" -- create a terminal version
" -- add more lang specifics
" -- (Will think of some more sutff !)
" }}}
"
" Usage and Requirements "{{{
" ---------------------------------------------------------------------
" REQUIREMENTS:
" ---------------------------------------------------------------------
" Currently,
"
" This colourscheme is intended for use on:
" - gVim >= 7.3 for Linux, Mac and Windows. (Since, all colours are in hex
"   values, hence works with gvim. Terminal vim will be supported in future)
"
" ---------------------------------------------------------------------
" INSTALLATION:
" ---------------------------------------------------------------------
" Two options for installation: manual or pathogen
"
" ---------------------------------------------------------------------
" MANUAL INSTALLATION OPTION:
" ---------------------------------------------------------------------
"
" 1. Download the luna distribution (as a zip archive, available on the github page)
" and unarchive the file.
" 2. Move `colors/luna.vim` to your `.vim/colors` directory.
" 3. Enjoy !
"
" ---------------------------------------------------------------------
" HIGHLY RECOMMENDED PATHOGEN INSTALLATION OPTION:
" ---------------------------------------------------------------------
"
" 1. Download and install Tim Pope's Pathogen from:
" https://github.com/tpope/vim-pathogen
"
" 2. Next, move or clone the `vim-luna` directory so that it is
" a subdirectory of the `.vim/bundle` directory.
"
" a. **clone with git:**
"
" $ cd ~/.vim/bundle
" $ git clone git://github.com/Pychimp/vim-luna.git
"
" ---------------------------------------------------------------------
" MODIFY VIMRC:
" ---------------------------------------------------------------------
"
" After either manual or pathogen installation, put the following two lines in your
" .vimrc:
"
" syntax enable
" colorscheme luna
" }}}
"
" Colorscheme initialization "{{{
" ---------------------------------------------------------------------
set background=dark
highlight clear
if exists("syntax_on")
    syntax reset
endif
let g:colors_name = "luna"
" }}}
"
" Gvim Highlighting: (see :help highlight-groups)"{{{
" ---------------------------------------------------------------------
" First, the Normal
hi Normal        guifg=#e5e5e5 guibg=#212121 gui=NONE
" ---------------------------------------------------------------------
" The Languages stuff
hi Title         guifg=#c9f0fa guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
hi Comment       guifg=#616161 guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
" hi Constant      guifg=#e3588d guibg=NONE    gui=NONE
hi Constant      guifg=#fff159 guibg=NONE    gui=NONE
hi String        guifg=#60bdf4 guibg=NONE    gui=NONE
hi Character     guifg=#ff8da1 guibg=NONE    gui=NONE
hi Number        guifg=#fff159 guibg=NONE    gui=NONE
hi Boolean       guifg=#fff159 guibg=NONE    gui=NONE
hi Float         guifg=#fff159 guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
"hi Identifier    guifg=#40ffff guibg=NONE    gui=NONE
hi Identifier    guifg=#00bcbc guibg=NONE    gui=NONE
hi Function      guifg=#00bcbc guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
"hi Statement     guifg=#ff8036 guibg=NONE    gui=NONE
"hi Statement     guifg=#ee82ee guibg=NONE    gui=NONE
"hi Statement     guifg=#f26d99 guibg=NONE    gui=NONE
"hi Statement     guifg=#b06bfc guibg=NONE    gui=NONE
"hi Statement     guifg=#f88379 guibg=NONE    gui=NONE
hi Statement     guifg=#f64a8a guibg=NONE    gui=NONE
"hi Conditional   guifg=#c72723 guibg=NONE    gui=NONE
hi Conditional   guifg=#e4d00a guibg=NONE    gui=NONE
" hi Repeat       guifg= guibg=NONE    gui=NONE
" hi Label       guifg= guibg=NONE    gui=NONE
hi Operator      guifg=#ff8036 guibg=NONE    gui=NONE
" hi Keyword       guifg= guibg=NONE    gui=NONE
hi Exception     guifg=#e4d00a guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
hi PreProc       guifg=#bada55 guibg=NONE    gui=NONE
" hi Include       guifg= guibg=NONE    gui=NONE
"hi Define        guifg=#bada55 guibg=NONE    gui=NONE
" hi Macro        guifg=#bada55 guibg=NONE    gui=NONE
" hi PreCondit        guifg=#bada55 guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
"hi Type          guifg=#26ffa1 guibg=NONE    gui=NONE
"hi Type          guifg=#ff3800 guibg=NONE    gui=NONE
hi Type          guifg=#ff4040 guibg=NONE    gui=NONE
"hi StorageClass  guifg=#f4bbff guibg=NONE    gui=NONE
hi StorageClass  guifg=#da8a67 guibg=NONE    gui=NONE
" hi Structure  guifg= guibg=NONE    gui=NONE
" hi Typedef  guifg= guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
hi Special       guifg=#ff8da1 guibg=NONE    gui=NONE
" hi SpecialChar       guifg=#ff8da1 guibg=NONE    gui=NONE
" hi Tag           guifg= guibg=NONE    gui=NONE
" hi Delimiter           guifg= guibg=NONE    gui=NONE
" hi SpecialComment           guifg= guibg=NONE    gui=NONE
" hi Debug           guifg= guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
hi Underlined    guifg=#80a0ff guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
" hi Ignore        guifg= guibg=NONE    gui=NONE
" ---------------------------------------------------------------------
hi Error         guifg=#870000 guibg=#ffa40b gui=NONE
" ---------------------------------------------------------------------
hi TODO          guifg=#ff0087 guibg=#ffff87 gui=NONE

" ---------------------------------------------------------------------
" Extended Highlighting

hi NonText       guifg=#838383 guibg=NONE    gui=NONE
hi Visual        guifg=#262626 guibg=#ffff4d gui=NONE
hi ErrorMsg      guifg=#870000 guibg=#ffa40b gui=NONE
hi IncSearch     guifg=#262626 guibg=#ff9933 gui=NONE
hi Search        guifg=#262626 guibg=#ff9933 gui=NONE
hi MoreMsg       guifg=#616161 guibg=NONE    gui=NONE
hi ModeMsg       guifg=#616161 guibg=NONE    gui=NONE
hi LineNr        guifg=#838383 guibg=NONE    gui=NONE
hi VertSplit     guifg=#212121 guibg=#474747 gui=NONE
hi VisualNOS     guifg=#262626 guibg=#ffff4d gui=NONE
"hi Folded        guifg=#2e4545 guibg=#1e2d2d gui=NONE
hi Folded        guifg=#426464 guibg=#1e2d2d gui=NONE
hi DiffAdd       guifg=#ffffff guibg=#006600 gui=NONE
hi DiffChange    guifg=#ffffff guibg=#007878 gui=NONE
hi DiffDelete    guifg=#ff0101 guibg=#9a0000 gui=NONE
hi DiffText      guifg=#000000 guibg=#ffb733 gui=NONE
hi SpellBad      guifg=#d80000 guibg=#ffff9a gui=NONE
hi SpellCap      guifg=#8b4600 guibg=#ffff9a gui=NONE
hi SpellRare     guifg=#ff0000 guibg=#ffff9a gui=NONE
hi SpellLocal    guifg=#008b00 guibg=#ffff9a gui=NONE
" hi StatusLine    guifg=#000000 guibg=#8d8d8d gui=NONE
" hi StatusLine    guifg=#ffffff guibg=#2e4545 gui=NONE
" hi StatusLine    guifg=#ffffff guibg=#1e2d2d gui=NONE
" hi StatusLine    guifg=#ffffff guibg=#353535 gui=NONE
" hi StatusLine    guifg=#ffffff guibg=#1f2e2e gui=NONE
hi StatusLine    guifg=#ffffff guibg=#002b2b gui=NONE
hi StatusLineNC  guifg=#ffffff guibg=#474747 gui=NONE
" hi Pmenu         guifg=#586e75 guibg=#fdf6e3 gui=NONE
" hi PmenuSel      guifg=#fdf6e3 guibg=#2aa198 gui=NONE
" hi PmenuSbar     guifg=#fdf6e3 guibg=#fdf6e3 gui=NONE
" hi PmenuThumb    guifg=#fdf6e3 guibg=#fdf6e3 gui=NONE
" hi Pmenu         guifg=#426464 guibg=#002b2b gui=NONE
" hi Pmenu         guifg=#609292 guibg=#002b2b gui=NONE
hi Pmenu         guifg=#7ca9a9 guibg=#002b2b gui=NONE
hi PmenuSel      guifg=#002b2b guibg=#fdf6e3 gui=NONE
hi PmenuSbar     guifg=#002b2b guibg=#002b2b gui=NONE
hi PmenuThumb    guifg=#002b2b guibg=#002b2b gui=NONE
hi MatchParen    guifg=#000000 guibg=#ff4040 gui=NONE
hi CursorLine    guifg=NONE    guibg=#2e2e2e gui=NONE
"hi CursorLineNr  guifg=#50c878 guibg=#2e2e2e gui=NONE
"hi CursorLineNr  guifg=#3eb489 guibg=NONE    gui=NONE
"hi CursorLineNr  guifg=#f5fffa guibg=NONE    gui=NONE
hi CursorLineNr  guifg=#87ceeb guibg=NONE    gui=NONE
hi CursorColumn  guifg=NONE    guibg=#2e2e2e gui=NONE
hi ColorColumn   guifg=NONE    guibg=#3e3739 gui=NONE
hi WildMenu      guifg=#002b2b guibg=#ffffff gui=NONE
hi SignColumn    guifg=NONE    guibg=#212121 gui=NONE
" }}}
"
" Language Specifics: {{{
" ---------------------------------------------------------------------
" These are language specifics. These are set explicitly to override the group
" highlighting provided by vim (Simply to make the language that you're working
" on more awesome, and fun to work with !)
" ---------------------------------------------------------------------
" Python Specifics
"hi pythonDot        guifg=#00ffa5 guibg=NONE gui=NONE
"hi pythonDot        guifg=#ffff31 guibg=NONE gui=NONE
"hi pythonDot        guifg=#ff0800 guibg=NONE gui=NONE
hi pythonDot                 guifg=#d70a53 guibg=NONE gui=NONE
hi pythonParameters          guifg=#bada55 guibg=NONE gui=NONE
hi pythonClassParameters     guifg=#bada55 guibg=NONE gui=NONE
hi pythonClass               guifg=#00bcbc guibg=NONE gui=NONE
"
" ---------------------------------------------------------------------
"  Ruby Specifics
hi rubyInterpolation      guifg=#ff4040 guibg=NONE gui=NONE
"hi rubyMethodBlock        guifg=#ff8da1 guibg=NONE gui=NONE
"hi rubyMethodBlock        guifg=#8ddaff guibg=NONE gui=NONE
hi rubyMethodBlock        guifg=#ffb28d guibg=NONE gui=NONE
hi rubyCurlyBlock         guifg=#f64a8a guibg=NONE gui=NONE
hi rubyDoBlock            guifg=#f64a8a guibg=NONE gui=NONE
hi rubyBlockExpression    guifg=#f64a8a guibg=NONE gui=NONE
hi rubyArrayDelimiter     guifg=#00bcbc guibg=NONE gui=NONE
"
" ---------------------------------------------------------------------
" }}}
"
" Extras: {{{
" ---------------------------------------------------------------------
" These are extra parts for highlighting certain external plugins
" ---------------------------------------------------------------------
"
" Startify (https://github.com/mhinz/vim-startify)
"
hi StartifyBracket  guifg=#b06bfc guibg=NONE gui=NONE
hi StartifyNumber   guifg=#bada55 guibg=NONE gui=NONE
hi StartifySpecial  guifg=#2e8857 guibg=NONE gui=NONE
hi StartifyPath     guifg=#545454 guibg=NONE gui=NONE
hi StartifySlash    guifg=#474747 guibg=NONE gui=NONE
" hi StartifyFile     guifg=#00ffa5 guibg=NONE gui=NONE
" hi StartifyFile     guifg=#2aa198 guibg=NONE gui=NONE
" hi StartifyFile     guifg=#f0e68c guibg=NONE gui=NONE
hi StartifyFile     guifg=#fa8072 guibg=NONE gui=NONE
hi StartifyHeader   guifg=#f0e68c guibg=NONE gui=NONE
hi StartifyFooter   guifg=#a0522d guibg=NONE gui=NONE
"
" ---------------------------------------------------------------------
"
" Signify (https://github.com/mhinz/vim-signify)
"
hi SignifySignAdd    guifg=#00ff00 guibg=#212121 gui=NONE
hi SignifySignChange guifg=#ff5f00 guibg=#212121 gui=NONE
hi SignifySignDelete guifg=#ff0000 guibg=#212121 gui=NONE
"
" ---------------------------------------------------------------------
" }}}
"
" vim:foldmethod=marker:foldlevel=0:textwidth=79
"
