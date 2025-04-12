-- Set mapleader
vim.g.mapleader = ","

-- Check and install vim-plug if not present
local plug_path = vim.fn.stdpath('config') .. '/autoload/plug.vim'
if vim.fn.filereadable(plug_path) == 0 then
	print("Downloading junegunn/vim-plug to manage plugins...")
	vim.fn.mkdir(vim.fn.stdpath('config') .. '/autoload', 'p')
	vim.fn.system('curl -fLo ' .. plug_path .. ' --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim')
	vim.api.nvim_create_autocmd("VimEnter", {
		callback = function() vim.cmd("PlugInstall") end,
	})
end

-- Mappings for ,,
vim.keymap.set("n", ",,", ":keepp /<++><CR>ca<", { noremap = true })
vim.keymap.set("i", ",,", "<Esc>:keepp /<++><CR>ca<", { noremap = true })

-- Plugin setup with vim-plug
vim.fn['plug#begin'](vim.fn.stdpath('config') .. '/plugged')
vim.fn['plug#']('tpope/vim-surround')
vim.fn['plug#']('preservim/nerdtree')
vim.fn['plug#']('junegunn/goyo.vim')
vim.fn['plug#']('jreybert/vimagit')
vim.fn['plug#']('vimwiki/vimwiki')
vim.fn['plug#']('vim-airline/vim-airline')
vim.fn['plug#']('nvim-tree/nvim-web-devicons')
vim.fn['plug#']('tpope/vim-commentary')
vim.fn['plug#']('ap/vim-css-color')
-- New Plugins for LSP Server
vim.fn['plug#']('neovim/nvim-lspconfig')
vim.fn['plug#']('hrsh7th/nvim-cmp')
vim.fn['plug#']('hrsh7th/cmp-nvim-lsp')
vim.fn['plug#']('hrsh7th/cmp-buffer')
vim.fn['plug#']('hrsh7th/cmp-path')
vim.fn['plug#end']()

-- General settings
vim.opt.title = true
-- vim.opt.background = "light"
vim.opt.background = "dark"
vim.opt.mouse = "a"
vim.opt.hlsearch = false
vim.opt.clipboard:append("unnamedplus")
vim.opt.showmode = false
vim.opt.ruler = false
vim.opt.laststatus = 0
vim.opt.showcmd = false
vim.cmd("colorscheme vim")

-- Basic settings
vim.keymap.set("n", "c", '"_c', { noremap = true })
vim.cmd("filetype plugin on")
vim.cmd("syntax on")
vim.opt.encoding = "utf-8"
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.wildmode = "longest,list,full"
vim.api.nvim_create_autocmd("FileType", {
	callback = function()
		vim.opt_local.formatoptions:remove({"c", "r", "o"})
	end,
})
vim.keymap.set("v", ".", ":normal .<CR>", { noremap = true })

-- Goyo and spell-check mappings
--vim.keymap.set("n", "<leader>f", ":Goyo | set background=light | set linebreak<CR>", { noremap = true })
vim.keymap.set("n", "<leader>f", ":Goyo | set background=dark | set linebreak<CR>", { noremap = true })
vim.keymap.set("n", "<leader>o", ":setlocal spell! spelllang=en_us<CR>", { noremap = true })

-- Split settings
vim.opt.splitbelow = true
vim.opt.splitright = true

-- NERDTree
vim.keymap.set("n", "<leader>n", ":NERDTreeToggle<CR>", { noremap = true })
vim.api.nvim_create_autocmd("BufEnter", {
	callback = function()
		if vim.fn.winnr("$") == 1 and vim.b.NERDTree ~= nil and vim.b.NERDTree.isTabTree() then
			vim.cmd("q")
		end
	end,
})
vim.g.NERDTreeBookmarksFile = vim.fn.stdpath('data') .. '/NERDTreeBookmarks'

-- vim-airline configuration
vim.cmd([[
if !exists('g:airline_symbols')
	let g:airline_symbols = {}
	endif
	let g:airline_symbols.colnr = ' C:'
	let g:airline_symbols.linenr = ' L:'
	let g:airline_symbols.maxlinenr = ' '
	let g:airline#extensions#whitespace#symbol = '!'
]])

-- Split navigation
vim.keymap.set("n", "<C-h>", "<C-w>h", { noremap = true })
vim.keymap.set("n", "<C-j>", "<C-w>j", { noremap = true })
vim.keymap.set("n", "<C-k>", "<C-w>k", { noremap = true })
vim.keymap.set("n", "<C-l>", "<C-w>l", { noremap = true })

-- Replace ex mode with gq
vim.keymap.set("n", "Q", "gq", { noremap = true })

-- Shellcheck
vim.keymap.set("n", "<leader>s", ":!clear && shellcheck -x %<CR>", { noremap = true })

-- Bibliography and reference files
vim.keymap.set("n", "<leader>b", ":vsp $BIB<CR>", { noremap = true })
vim.keymap.set("n", "<leader>r", ":vsp $REFER<CR>", { noremap = true })

-- Replace all
vim.keymap.set("n", "S", ":%s//g<Left><Left>", { noremap = true })

-- Compile and preview
vim.keymap.set("n", "<leader>c", ":w! | !compiler %:p<CR>", { noremap = true })
vim.keymap.set("n", "<leader>p", ":!opout %:p<CR>", { noremap = true })

-- Clean tex build files on exit
vim.api.nvim_create_autocmd("VimLeave", {
	pattern = "*.tex",
	command = "!latexmk -c %",
})

-- Filetype settings
vim.g.vimwiki_ext2syntax = {
	['.Rmd'] = 'markdown',
	['.rmd'] = 'markdown',
	['.md'] = 'markdown',
	['.markdown'] = 'markdown',
	['.mdown'] = 'markdown',
}
vim.keymap.set("n", "<leader>v", ":VimwikiIndex<CR>", { noremap = true })
vim.g.vimwiki_list = {{path = '~/.local/share/nvim/vimwiki', syntax = 'markdown', ext = '.md'}}
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = {"/tmp/calcurse*", "~/.calcurse/notes/*"},
	command = "set filetype=markdown",
})
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = {"*.ms", "*.me", "*.mom", "*.man"},
	command = "set filetype=groff",
})
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = "*.tex",
	command = "set filetype=tex",
})

-- Sudo write
vim.api.nvim_create_user_command("W", "silent! write !sudo tee % >/dev/null | edit!", {})

-- Goyo for mutt
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = "/tmp/neomutt*",
	callback = function()
		vim.cmd("Goyo 80")
		vim.api.nvim_feedkeys("jk", "n", false)
	end,
})
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = "/tmp/neomutt*",
	callback = function()
		vim.keymap.set("n", "ZZ", ":Goyo!|x!<CR>", { buffer = true, noremap = true })
		vim.keymap.set("n", "ZQ", ":Goyo!|q!<CR>", { buffer = true, noremap = true })
	end,
})

-- Clean trailing whitespace and newlines on save
vim.api.nvim_create_autocmd("BufWritePre", {
	callback = function()
		local currPos = vim.fn.getpos(".")
		vim.cmd("%s/\\s\\+$//e")
		vim.cmd("%s/\\n\\+\\%$//e")
		if vim.bo.filetype == "c" or vim.bo.filetype == "h" then
			vim.cmd("%s/\\%$/\r/e")
		end
		if vim.fn.expand("%"):match("neomutt") then
			vim.cmd("%s/^--$/-- /e")
		end
		vim.fn.setpos(".", currPos)
	end,
})

-- Update shortcuts and configs
vim.api.nvim_create_autocmd("BufWritePost", {
	pattern = {"bm-files", "bm-dirs"},
	command = "!shortcuts",
})
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = {"Xresources", "Xdefaults", "xresources", "xdefaults"},
	command = "set filetype=xdefaults",
})
vim.api.nvim_create_autocmd("BufWritePost", {
	pattern = {"Xresources", "Xdefaults", "xresources", "xdefaults"},
	command = "!xrdb %",
})
vim.api.nvim_create_autocmd("BufWritePost", {
	pattern = "~/.local/src/dwmblocks/config.h",
	command = "!cd ~/.local/src/dwmblocks/; sudo make install && { killall -q dwmblocks;setsid -f dwmblocks }",
})

-- Diff highlighting
if vim.opt.diff:get() then
	vim.cmd("highlight! link DiffText MatchParen")
end

-- Toggle statusbar
local hidden_all = 0
local function toggle_hidden_all()
	if hidden_all == 0 then
		hidden_all = 1
		vim.opt.showmode = false
		vim.opt.ruler = false
		vim.opt.laststatus = 0
		vim.opt.showcmd = false
	else
		hidden_all = 0
		vim.opt.showmode = true
		vim.opt.ruler = true
		vim.opt.laststatus = 2
		vim.opt.showcmd = true
	end
end
vim.keymap.set("n", "<leader>h", toggle_hidden_all, { noremap = true })

-- Load shortcuts
pcall(vim.cmd, "source ~/.config/nvim/shortcuts.vim")

-- Syntax Highlighting - LSP setup
local lspconfig = require'lspconfig'
-- These language servers are in pacman or the AUR with the same name as given below, unless otherwise noted.
local servers = {
--	'server_name',		-- Language name	-- Pacman/AUR name
	'pyright',		-- Python		-- pyright
	'ts_ls',		-- TypeScript		-- typescript-language-server
	'gopls',		-- Go			-- gopls
	'clangd',		-- C			-- clang
	'rust_analyzer',	-- Rust			-- rust_analyzer
	'texlab',		-- LaTeX		-- texlab
	'marksman',		-- Markdown		-- marksman
	'r_language_server',	-- R			-- Run `install.packages("languageserver")` inside R
	'csharp_ls',		-- C#			-- csharp-ls
--	'omnisharp',		-- C# (legacy)		-- omnisharp-roslyn-bin
	'lua_ls',		-- Lua			-- lua-language-server
	'yamlls',		-- YAML			-- yaml-language-server
	'bashls',		-- bash			-- bash-language-server
}
-- Automatically set up each LSP server in the list
for _, server in ipairs(servers) do
	lspconfig[server].setup {}
end

local cmp = require'cmp'
cmp.setup({
	mapping = {
		['<C-n>'] = cmp.mapping.select_next_item(), -- Next suggestion
		['<C-j>'] = cmp.mapping.select_next_item(), -- Next suggestion (vim-style bind)
		['<C-p>'] = cmp.mapping.select_prev_item(), -- Previous suggestion
		['<C-k>'] = cmp.mapping.select_prev_item(), -- Previous suggestion (vim-style bind)
		['<C-y>'] = cmp.mapping.confirm({ select = true }), -- Confirm completion
		['<CR>'] = cmp.mapping.confirm({ select = true }), -- Confirm completion
		['<C-Space>'] = cmp.mapping.complete(), -- Trigger completion manually
	},
	sources = {
		{ name = 'nvim_lsp' },  -- Use LSP as a completion source
		{ name = 'buffer' },    -- Suggest words from open buffers
		{ name = 'path' },      -- Suggest file paths
	}
})

-- Diagnostic navigation mappings
vim.keymap.set('n', ']d', vim.diagnostic.goto_next, { desc = "Go to next diagnostic" })
vim.keymap.set('n', '[d', vim.diagnostic.goto_prev, { desc = "Go to previous diagnostic" })

vim.diagnostic.config({
	virtual_text = false, -- Disable virtual text to avoid clutter
	signs = true, -- Show signs in the gutter
	underline = true, -- Underline errors
	update_in_insert = false, -- Don’t update diagnostics in insert mode
})

-- Automatically show diagnostics on hover
vim.o.updatetime = 250 -- Adjust delay for hover (in milliseconds)
vim.api.nvim_create_autocmd("CursorHold", {
	callback = function()
		vim.diagnostic.open_float(nil, { focusable = false })
	end,
})
