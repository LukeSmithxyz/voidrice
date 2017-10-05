" wal.vim -- Vim color scheme.
" Author:       Dylan Araps
" Webpage:      https://github.com/dylanaraps/wal
" Description:  A colorscheme that uses your terminal colors, made to work with 'wal'.

hi clear
set background=dark

if exists('syntax_on')
    syntax reset
endif

" Colorscheme name
let g:colors_name = 'wal'

" highlight groups {{{

" set t_Co=16
hi Normal ctermbg=NONE ctermfg=7
hi NonText ctermbg=NONE ctermfg=0
hi Comment ctermbg=NONE ctermfg=8
hi Constant ctermbg=NONE ctermfg=3
hi Error ctermbg=1 ctermfg=7
hi Identifier ctermbg=NONE ctermfg=1 cterm=BOLD
hi Ignore ctermbg=8 ctermfg=0
hi PreProc ctermbg=NONE ctermfg=3
hi Special ctermbg=NONE ctermfg=6
hi Statement ctermbg=NONE ctermfg=1
hi String ctermbg=NONE ctermfg=2
hi Number ctermbg=NONE ctermfg=3
hi Todo ctermbg=2 ctermfg=0
hi Type ctermbg=NONE ctermfg=3
hi Underlined ctermbg=NONE ctermfg=1 cterm=underline
hi StatusLine ctermbg=7 ctermfg=0
hi StatusLineNC ctermbg=NONE ctermfg=NONE
hi TabLine ctermbg=NONE ctermfg=8
hi TabLineFill ctermbg=NONE ctermfg=8
hi TabLineSel ctermbg=4 ctermfg=0
hi TermCursorNC ctermbg=3 ctermfg=0
hi VertSplit ctermbg=NONE ctermfg=NONE
hi Title ctermbg=NONE ctermfg=4
hi CursorLine ctermbg=8 ctermfg=0
hi LineNr ctermbg=NONE ctermfg=8
hi CursorLineNr ctermbg=NONE ctermfg=8
hi helpLeadBlank ctermbg=NONE ctermfg=7
hi helpNormal ctermbg=NONE ctermfg=7
hi Visual ctermbg=8 ctermfg=0
hi VisualNOS ctermbg=NONE ctermfg=1
hi Pmenu ctermbg=8 ctermfg=7
hi PmenuSbar ctermbg=6 ctermfg=7
hi PmenuSel ctermbg=4 ctermfg=0
hi PmenuThumb ctermbg=8 ctermfg=8
hi FoldColumn ctermbg=NONE ctermfg=7
hi Folded ctermbg=NONE ctermfg=8
hi WildMenu ctermbg=2 ctermfg=0
hi SpecialKey ctermbg=NONE ctermfg=8
hi DiffAdd ctermbg=NONE ctermfg=2
hi DiffChange ctermbg=NONE ctermfg=8
hi DiffDelete ctermbg=NONE ctermfg=1
hi DiffText ctermbg=NONE ctermfg=4
hi IncSearch ctermbg=3 ctermfg=0
hi Search ctermbg=3 ctermfg=0
hi Directory ctermbg=NONE ctermfg=4
hi MatchParen ctermbg=8 ctermfg=0
hi ColorColumn ctermbg=4 ctermfg=0
hi signColumn ctermbg=NONE ctermfg=4
hi ErrorMsg ctermbg=NONE ctermfg=8
hi ModeMsg ctermbg=NONE ctermfg=2
hi MoreMsg ctermbg=NONE ctermfg=2
hi Question ctermbg=NONE ctermfg=4
hi WarningMsg ctermbg=1 ctermfg=0
hi Cursor ctermbg=NONE ctermfg=8
hi Structure ctermbg=NONE ctermfg=5
hi CursorColumn ctermbg=8 ctermfg=7
hi ModeMsg ctermbg=NONE ctermfg=7
hi SpellBad ctermbg=1 ctermfg=0
hi SpellCap ctermbg=NONE ctermfg=4 cterm=underline
hi SpellLocal ctermbg=NONE ctermfg=5 cterm=underline
hi SpellRare ctermbg=NONE ctermfg=6 cterm=underline
hi Boolean ctermbg=NONE ctermfg=5
hi Character ctermbg=NONE ctermfg=1
hi Conditional ctermbg=NONE ctermfg=5
hi Define ctermbg=NONE ctermfg=5
hi Delimiter ctermbg=NONE ctermfg=5
hi Float ctermbg=NONE ctermfg=5
hi Include ctermbg=NONE ctermfg=4
hi Keyword ctermbg=NONE ctermfg=5
hi Label ctermbg=NONE ctermfg=3
hi Operator ctermbg=NONE ctermfg=7
hi Repeat ctermbg=NONE ctermfg=3
hi SpecialChar ctermbg=NONE ctermfg=5
hi Tag ctermbg=NONE ctermfg=3
hi Typedef ctermbg=NONE ctermfg=3
hi vimUserCommand ctermbg=NONE ctermfg=1 cterm=BOLD
    hi link vimMap vimUserCommand
    hi link vimLet vimUserCommand
    hi link vimCommand vimUserCommand
    hi link vimFTCmd vimUserCommand
    hi link vimAutoCmd vimUserCommand
    hi link vimNotFunc vimUserCommand
hi vimNotation ctermbg=NONE ctermfg=4
hi vimMapModKey ctermbg=NONE ctermfg=4
hi vimBracket ctermbg=NONE ctermfg=7
hi vimCommentString ctermbg=NONE ctermfg=8
hi htmlLink ctermbg=NONE ctermfg=1 cterm=underline
hi htmlBold ctermbg=NONE ctermfg=3 cterm=BOLD
hi htmlItalic ctermbg=NONE ctermfg=5
hi htmlEndTag ctermbg=NONE ctermfg=7
hi htmlTag ctermbg=NONE ctermfg=7
hi htmlTagName ctermbg=NONE ctermfg=1 cterm=BOLD
hi htmlH1 ctermbg=NONE ctermfg=7
    hi link htmlH2 htmlH1
    hi link htmlH3 htmlH1
    hi link htmlH4 htmlH1
    hi link htmlH5 htmlH1
    hi link htmlH6 htmlH1
hi cssMultiColumnAttr ctermbg=NONE ctermfg=2
    hi link cssFontAttr cssMultiColumnAttr
    hi link cssFlexibleBoxAttr cssMultiColumnAttr
hi cssBraces ctermbg=NONE ctermfg=7
    hi link cssAttrComma cssBraces
hi cssValueLength ctermbg=NONE ctermfg=7
hi cssUnitDecorators ctermbg=NONE ctermfg=7
hi cssValueNumber ctermbg=NONE ctermfg=7
    hi link cssValueLength cssValueNumber
hi cssNoise ctermbg=NONE ctermfg=8
hi cssTagName ctermbg=NONE ctermfg=1
hi cssFunctionName ctermbg=NONE ctermfg=4
hi scssSelectorChar ctermbg=NONE ctermfg=7
hi scssAttribute ctermbg=NONE ctermfg=7
    hi link scssDefinition cssNoise
hi sassidChar ctermbg=NONE ctermfg=1
hi sassClassChar ctermbg=NONE ctermfg=5
hi sassInclude ctermbg=NONE ctermfg=5
hi sassMixing ctermbg=NONE ctermfg=5
hi sassMixinName ctermbg=NONE ctermfg=4
hi javaScript ctermbg=NONE ctermfg=7
hi javaScriptBraces ctermbg=NONE ctermfg=7
hi javaScriptNumber ctermbg=NONE ctermfg=5
hi markdownH1 ctermbg=NONE ctermfg=7
    hi link markdownH2 markdownH1
    hi link markdownH3 markdownH1
    hi link markdownH4 markdownH1
    hi link markdownH5 markdownH1
    hi link markdownH6 markdownH1
hi markdownAutomaticLink ctermbg=NONE ctermfg=1 cterm=underline
    hi link markdownUrl markdownAutomaticLink
hi markdownError ctermbg=NONE ctermfg=7
hi markdownCode ctermbg=NONE ctermfg=3
hi markdownCodeBlock ctermbg=NONE ctermfg=3
hi markdownCodeDelimiter ctermbg=NONE ctermfg=5
hi xdefaultsValue ctermbg=NONE ctermfg=7
hi rubyInclude ctermbg=NONE ctermfg=4
hi rubyDefine ctermbg=NONE ctermfg=5
hi rubyFunction ctermbg=NONE ctermfg=4
hi rubyStringDelimiter ctermbg=NONE ctermfg=2
hi rubyInteger ctermbg=NONE ctermfg=3
hi rubyAttribute ctermbg=NONE ctermfg=4
hi rubyConstant ctermbg=NONE ctermfg=3
hi rubyInterpolation ctermbg=NONE ctermfg=2
hi rubyInterpolationDelimiter ctermbg=NONE ctermfg=3
hi rubyRegexp ctermbg=NONE ctermfg=6
hi rubySymbol ctermbg=NONE ctermfg=2
hi rubyTodo ctermbg=NONE ctermfg=8
hi rubyRegexpAnchor ctermbg=NONE ctermfg=7
    hi link rubyRegexpQuantifier rubyRegexpAnchor
hi pythonOperator ctermbg=NONE ctermfg=5
hi pythonFunction ctermbg=NONE ctermfg=4
hi pythonRepeat ctermbg=NONE ctermfg=5
hi pythonStatement ctermbg=NONE ctermfg=1 cterm=Bold
hi pythonBuiltIn ctermbg=NONE ctermfg=4
hi phpMemberSelector ctermbg=NONE ctermfg=7
hi phpComparison ctermbg=NONE ctermfg=7
hi phpParent ctermbg=NONE ctermfg=7
hi cOperator ctermbg=NONE ctermfg=6
hi cPreCondit ctermbg=NONE ctermfg=5
hi SignifySignAdd ctermbg=NONE ctermfg=2
hi SignifySignChange ctermbg=NONE ctermfg=4
hi SignifySignDelete ctermbg=NONE ctermfg=1
hi NERDTreeDirSlash ctermbg=NONE ctermfg=4
hi NERDTreeExecFile ctermbg=NONE ctermfg=7
hi ALEErrorSign ctermbg=NONE ctermfg=1
hi ALEWarningSign ctermbg=NONE ctermfg=3
hi ALEError ctermbg=NONE ctermfg=1
hi ALEWarning ctermbg=NONE ctermfg=3

" }}}

" Plugin options {{{

let g:limelight_conceal_ctermfg = 8

" }}}
