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
hi Normal ctermbg=NONE ctermfg=7 cterm=NONE
hi NonText ctermbg=NONE ctermfg=0 cterm=NONE
hi Comment ctermbg=NONE ctermfg=8 cterm=NONE
hi Constant ctermbg=NONE ctermfg=3 cterm=NONE
hi Error ctermbg=1 ctermfg=7 cterm=NONE
hi Identifier ctermbg=NONE ctermfg=1 cterm=NONE
hi Ignore ctermbg=8 ctermfg=0 cterm=NONE
hi PreProc ctermbg=NONE ctermfg=3 cterm=NONE
hi Special ctermbg=NONE ctermfg=6 cterm=NONE
hi Statement ctermbg=NONE ctermfg=1 cterm=NONE
hi String ctermbg=NONE ctermfg=2 cterm=NONE
hi Number ctermbg=NONE ctermfg=3 cterm=NONE
hi Todo ctermbg=2 ctermfg=0 cterm=NONE
hi Type ctermbg=NONE ctermfg=3 cterm=NONE
hi Underlined ctermbg=NONE ctermfg=1 cterm=underline
hi StatusLine ctermbg=7 ctermfg=0 cterm=NONE
hi StatusLineNC ctermbg=NONE ctermfg=NONE cterm=NONE
hi TabLine ctermbg=NONE ctermfg=8 cterm=NONE
hi TabLineFill ctermbg=NONE ctermfg=8 cterm=NONE
hi TabLineSel ctermbg=4 ctermfg=0 cterm=NONE
hi TermCursorNC ctermbg=3 ctermfg=0 cterm=NONE
hi VertSplit ctermbg=NONE ctermfg=NONE cterm=NONE
hi Title ctermbg=NONE ctermfg=4 cterm=NONE
hi CursorLine ctermbg=8 ctermfg=0 cterm=NONE
hi LineNr ctermbg=NONE ctermfg=8 cterm=NONE
hi CursorLineNr ctermbg=NONE ctermfg=8 cterm=NONE
hi helpLeadBlank ctermbg=NONE ctermfg=7 cterm=NONE
hi helpNormal ctermbg=NONE ctermfg=7 cterm=NONE
hi Visual ctermbg=8 ctermfg=0 cterm=NONE
hi VisualNOS ctermbg=NONE ctermfg=1 cterm=NONE
hi Pmenu ctermbg=8 ctermfg=7 cterm=NONE
hi PmenuSbar ctermbg=6 ctermfg=7 cterm=NONE
hi PmenuSel ctermbg=4 ctermfg=0 cterm=NONE
hi PmenuThumb ctermbg=8 ctermfg=8 cterm=NONE
hi FoldColumn ctermbg=NONE ctermfg=7 cterm=NONE
hi Folded ctermbg=NONE ctermfg=8 cterm=NONE
hi WildMenu ctermbg=2 ctermfg=0 cterm=NONE
hi SpecialKey ctermbg=NONE ctermfg=8 cterm=NONE
hi DiffAdd ctermbg=NONE ctermfg=2 cterm=NONE
hi DiffChange ctermbg=NONE ctermfg=8 cterm=NONE
hi DiffDelete ctermbg=NONE ctermfg=1 cterm=NONE
hi DiffText ctermbg=NONE ctermfg=4 cterm=NONE
hi IncSearch ctermbg=3 ctermfg=0 cterm=NONE
hi Search ctermbg=3 ctermfg=0 cterm=NONE
hi Directory ctermbg=NONE ctermfg=4 cterm=NONE
hi MatchParen ctermbg=8 ctermfg=0 cterm=NONE
hi ColorColumn ctermbg=4 ctermfg=0 cterm=NONE
hi signColumn ctermbg=NONE ctermfg=4 cterm=NONE
hi ErrorMsg ctermbg=NONE ctermfg=8 cterm=NONE
hi ModeMsg ctermbg=NONE ctermfg=2 cterm=NONE
hi MoreMsg ctermbg=NONE ctermfg=2 cterm=NONE
hi Question ctermbg=NONE ctermfg=4 cterm=NONE
hi WarningMsg ctermbg=1 ctermfg=0 cterm=NONE
hi Cursor ctermbg=NONE ctermfg=8 cterm=NONE
hi Structure ctermbg=NONE ctermfg=5 cterm=NONE
hi CursorColumn ctermbg=8 ctermfg=7 cterm=NONE
hi ModeMsg ctermbg=NONE ctermfg=7 cterm=NONE
hi SpellBad ctermbg=1 ctermfg=0 cterm=NONE
hi SpellCap ctermbg=NONE ctermfg=4 cterm=underline
hi SpellLocal ctermbg=NONE ctermfg=5 cterm=underline
hi SpellRare ctermbg=NONE ctermfg=6 cterm=underline
hi Boolean ctermbg=NONE ctermfg=5 cterm=NONE
hi Character ctermbg=NONE ctermfg=1 cterm=NONE
hi Conditional ctermbg=NONE ctermfg=5 cterm=NONE
hi Define ctermbg=NONE ctermfg=5 cterm=NONE
hi Delimiter ctermbg=NONE ctermfg=5 cterm=NONE
hi Float ctermbg=NONE ctermfg=5 cterm=NONE
hi Include ctermbg=NONE ctermfg=4 cterm=NONE
hi Keyword ctermbg=NONE ctermfg=5 cterm=NONE
hi Label ctermbg=NONE ctermfg=3 cterm=NONE
hi Operator ctermbg=NONE ctermfg=7 cterm=NONE
hi Repeat ctermbg=NONE ctermfg=3 cterm=NONE
hi SpecialChar ctermbg=NONE ctermfg=5 cterm=NONE
hi Tag ctermbg=NONE ctermfg=3 cterm=NONE
hi Typedef ctermbg=NONE ctermfg=3 cterm=NONE
hi vimUserCommand ctermbg=NONE ctermfg=1 cterm=BOLD
    hi link vimMap vimUserCommand
    hi link vimLet vimUserCommand
    hi link vimCommand vimUserCommand
    hi link vimFTCmd vimUserCommand
    hi link vimAutoCmd vimUserCommand
    hi link vimNotFunc vimUserCommand
hi vimNotation ctermbg=NONE ctermfg=4 cterm=NONE
hi vimMapModKey ctermbg=NONE ctermfg=4 cterm=NONE
hi vimBracket ctermbg=NONE ctermfg=7 cterm=NONE
hi vimCommentString ctermbg=NONE ctermfg=8 cterm=NONE
hi htmlLink ctermbg=NONE ctermfg=1 cterm=underline
hi htmlBold ctermbg=NONE ctermfg=3 cterm=NONE
hi htmlItalic ctermbg=NONE ctermfg=5 cterm=NONE
hi htmlEndTag ctermbg=NONE ctermfg=7 cterm=NONE
hi htmlTag ctermbg=NONE ctermfg=7 cterm=NONE
hi htmlTagName ctermbg=NONE ctermfg=1 cterm=BOLD
hi htmlH1 ctermbg=NONE ctermfg=7 cterm=NONE
    hi link htmlH2 htmlH1
    hi link htmlH3 htmlH1
    hi link htmlH4 htmlH1
    hi link htmlH5 htmlH1
    hi link htmlH6 htmlH1
hi cssMultiColumnAttr ctermbg=NONE ctermfg=2 cterm=NONE
    hi link cssFontAttr cssMultiColumnAttr
    hi link cssFlexibleBoxAttr cssMultiColumnAttr
hi cssBraces ctermbg=NONE ctermfg=7 cterm=NONE
    hi link cssAttrComma cssBraces
hi cssValueLength ctermbg=NONE ctermfg=7 cterm=NONE
hi cssUnitDecorators ctermbg=NONE ctermfg=7 cterm=NONE
hi cssValueNumber ctermbg=NONE ctermfg=7 cterm=NONE
    hi link cssValueLength cssValueNumber
hi cssNoise ctermbg=NONE ctermfg=8 cterm=NONE
hi cssTagName ctermbg=NONE ctermfg=1 cterm=NONE
hi cssFunctionName ctermbg=NONE ctermfg=4 cterm=NONE
hi scssSelectorChar ctermbg=NONE ctermfg=7 cterm=NONE
hi scssAttribute ctermbg=NONE ctermfg=7 cterm=NONE
    hi link scssDefinition cssNoise
hi sassidChar ctermbg=NONE ctermfg=1 cterm=NONE
hi sassClassChar ctermbg=NONE ctermfg=5 cterm=NONE
hi sassInclude ctermbg=NONE ctermfg=5 cterm=NONE
hi sassMixing ctermbg=NONE ctermfg=5 cterm=NONE
hi sassMixinName ctermbg=NONE ctermfg=4 cterm=NONE
hi javaScript ctermbg=NONE ctermfg=7 cterm=NONE
hi javaScriptBraces ctermbg=NONE ctermfg=7 cterm=NONE
hi javaScriptNumber ctermbg=NONE ctermfg=5 cterm=NONE
hi markdownH1 ctermbg=NONE ctermfg=7 cterm=NONE
    hi link markdownH2 markdownH1
    hi link markdownH3 markdownH1
    hi link markdownH4 markdownH1
    hi link markdownH5 markdownH1
    hi link markdownH6 markdownH1
hi markdownAutomaticLink ctermbg=NONE ctermfg=1 cterm=underline
    hi link markdownUrl markdownAutomaticLink
hi markdownError ctermbg=NONE ctermfg=7 cterm=NONE
hi markdownCode ctermbg=NONE ctermfg=3 cterm=NONE
hi markdownCodeBlock ctermbg=NONE ctermfg=3 cterm=NONE
hi markdownCodeDelimiter ctermbg=NONE ctermfg=5 cterm=NONE
hi xdefaultsValue ctermbg=NONE ctermfg=7 cterm=NONE
hi rubyInclude ctermbg=NONE ctermfg=4 cterm=NONE
hi rubyDefine ctermbg=NONE ctermfg=5 cterm=NONE
hi rubyFunction ctermbg=NONE ctermfg=4 cterm=NONE
hi rubyStringDelimiter ctermbg=NONE ctermfg=2 cterm=NONE
hi rubyInteger ctermbg=NONE ctermfg=3 cterm=NONE
hi rubyAttribute ctermbg=NONE ctermfg=4 cterm=NONE
hi rubyConstant ctermbg=NONE ctermfg=3 cterm=NONE
hi rubyInterpolation ctermbg=NONE ctermfg=2 cterm=NONE
hi rubyInterpolationDelimiter ctermbg=NONE ctermfg=3 cterm=NONE
hi rubyRegexp ctermbg=NONE ctermfg=6 cterm=NONE
hi rubySymbol ctermbg=NONE ctermfg=2 cterm=NONE
hi rubyTodo ctermbg=NONE ctermfg=8 cterm=NONE
hi rubyRegexpAnchor ctermbg=NONE ctermfg=7 cterm=NONE
    hi link rubyRegexpQuantifier rubyRegexpAnchor
hi pythonOperator ctermbg=NONE ctermfg=5 cterm=NONE
hi pythonFunction ctermbg=NONE ctermfg=4 cterm=NONE
hi pythonRepeat ctermbg=NONE ctermfg=5 cterm=NONE
hi pythonStatement ctermbg=NONE ctermfg=1 cterm=Bold
hi pythonBuiltIn ctermbg=NONE ctermfg=4 cterm=NONE
hi phpMemberSelector ctermbg=NONE ctermfg=7 cterm=NONE
hi phpComparison ctermbg=NONE ctermfg=7 cterm=NONE
hi phpParent ctermbg=NONE ctermfg=7 cterm=NONE
hi cOperator ctermbg=NONE ctermfg=6 cterm=NONE
hi cPreCondit ctermbg=NONE ctermfg=5 cterm=NONE
hi SignifySignAdd ctermbg=NONE ctermfg=2 cterm=NONE
hi SignifySignChange ctermbg=NONE ctermfg=4 cterm=NONE
hi SignifySignDelete ctermbg=NONE ctermfg=1 cterm=NONE
hi NERDTreeDirSlash ctermbg=NONE ctermfg=4 cterm=NONE
hi NERDTreeExecFile ctermbg=NONE ctermfg=7 cterm=NONE
hi ALEErrorSign ctermbg=NONE ctermfg=1 cterm=NONE
hi ALEWarningSign ctermbg=NONE ctermfg=3 cterm=NONE
hi ALEError ctermbg=NONE ctermfg=1 cterm=NONE
hi ALEWarning ctermbg=NONE ctermfg=3 cterm=NONE

" }}}

" Plugin options {{{

let g:limelight_conceal_ctermfg = 8

" }}}
