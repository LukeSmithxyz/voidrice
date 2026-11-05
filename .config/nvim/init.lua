-- Set mapleader
vim.g.mapleader = ","

-- Check and install vim-plug if not present
local plug_path = vim.fn.stdpath('config') .. '/autoload/plug.vim'
if vim.fn.filereadable(plug_path) == 0 then
	print("Downloading junegunn/vim-plug to manage plugins...")
	vim.fn.mkdir(vim.fn.stdpath('config') .. '/autoload', 'p')
	vim.fn.system('curl -fLo ' .. plug_path .. ' --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim')
	vim.api.nvim_create_autocmd("VimEnter", { command = "PlugInstall" })
end

-- Mappings for ,,
vim.keymap.set("n", ",,", ":keepp /<++><CR>ca<", { noremap = true })
vim.keymap.set("i", ",,", "<Esc>:keepp /<++><CR>ca<", { noremap = true })

-- Plugin setup with vim-plug
local Plug = vim.fn["plug#"]
vim.fn['plug#begin'](vim.fn.stdpath('config') .. '/plugged')
Plug('tpope/vim-surround')
Plug('preservim/nerdtree')
Plug('junegunn/goyo.vim')
Plug('jreybert/vimagit')
Plug('vimwiki/vimwiki')
Plug('vim-airline/vim-airline')
Plug('nvim-tree/nvim-web-devicons')
Plug('tpope/vim-commentary')
Plug('ap/vim-css-color')
-- New Plugins for LSP Server
Plug('neovim/nvim-lspconfig')
Plug('hrsh7th/nvim-cmp')
Plug('hrsh7th/cmp-nvim-lsp')
Plug('hrsh7th/cmp-buffer')
Plug('hrsh7th/cmp-path')
-- Plugins for Debugging with DAP
Plug('mfussenegger/nvim-dap')
Plug('nvim-neotest/nvim-nio')
Plug('rcarriga/nvim-dap-ui')
Plug('mfussenegger/nvim-dap-python')
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
vim.opt.termguicolors = false	-- Use the terminal's colors (Xresources)
vim.cmd.colorscheme("vim")

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

-- Set light or dark theme --

vim.keymap.set("n", "<leader>l", ":set background=light<CR>", { noremap = true })
vim.keymap.set("n", "<leader>tb", ":set background=dark<CR>", { noremap = true })

-- Goyo and spell-check mappings
vim.keymap.set("n", "<leader>f", ":Goyo | set linebreak<CR>", { noremap = true })
vim.keymap.set("n", "<leader>o", ":setlocal spell! spelllang=en_us<CR>", { noremap = true })

-- Split settings
vim.opt.splitbelow = true
vim.opt.splitright = true

-- NERDTree
vim.keymap.set("n", "<leader>n", ":NERDTreeToggle<CR>", { noremap = true })
vim.api.nvim_create_autocmd("BufEnter", {
	callback = function()
		if vim.fn.winnr("$") == 1 and vim.b.NERDTree and vim.b.NERDTree.isTabTree() then
			vim.cmd("q")
		end
	end,
})
vim.g.NERDTreeBookmarksFile = vim.fn.stdpath('data') .. '/NERDTreeBookmarks'

-- vim-airline configuration

local airline_conf = vim.g.airline_symbols or {}
airline_conf.colnr = " C:"
airline_conf.linenr = " L:"
airline_conf.maxlinenr = "☰ "
vim.g.airline_symbols = airline_conf
vim.g['airline#extensions#whitespace#symbol'] = '!'

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
	pattern = { "*.tex", "*.md" },
	callback = function()
		local tex = vim.fn.expand("%:p:r") .. ".tex"
		if vim.fn.filereadable(tex) == 1 then
			vim.fn.system({ "latexmk", "-c", tex })
		end
	end,
})

-- Filetype settings
vim.g.vimwiki_ext2syntax = {
	['.md'] = 'markdown',
	['.markdown'] = 'markdown',
	['.mdown'] = 'markdown',
}

vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = {"*.Rmd", "*.rmd"},
	command = "setfiletype rmd",
})
vim.g.vimwiki_global_ext = 0
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
vim.keymap.set("ca", "w!!", "execute 'silent! write !sudo tee % >/dev/null' | edit!")

-- Goyo for mutt
vim.api.nvim_create_autocmd({"BufRead", "BufNewFile"}, {
	pattern = "/tmp/neomutt*",
	callback = function()
		vim.cmd("Goyo 80")
		vim.api.nvim_feedkeys("jk", "n", false)
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
	command = "!cd ~/.local/src/dwmblocks/; sudo make install && { killall -q dwmblocks; setsid -f dwmblocks; }",
})

-- Diff highlighting
if vim.opt.diff:get() then
	vim.cmd("highlight! link DiffText MatchParen")
end

-- Toggle statusbar

local hidden_all = false
local function toggle_hidden_all()
	vim.opt.showmode = hidden_all
	vim.opt.ruler = hidden_all
	vim.opt.showcmd = hidden_all
	vim.opt.laststatus = hidden_all and 2 or 0
	hidden_all = not hidden_all
end

vim.keymap.set("n", "<leader>h", toggle_hidden_all, { noremap = true })

-- Load shortcuts
pcall(vim.cmd, "source ~/.config/nvim/shortcuts.vim")

-- Syntax Highlighting - LSP setup

-- local lspconfig = require'lspconfig' -- For Neovim versions before 0.11

-- These language servers are in pacman or the AUR with the same name as given below, unless otherwise noted.

local servers = {
	--'server_name',	-- Language name	-- Pacman/AUR name
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
	'cssls',		-- CSS			-- vscode-css-languageserver
	'openscad_lsp',		-- OpenSCAD		-- openscad-lsp
	'nginx_language_server'	-- nginx		-- nginx-language-server
}
-- Automatically set up each LSP server in the list
for _, server in ipairs(servers) do
	-- lspconfig[server].setup {} 	-- For Neovim versions before 0.11
	vim.lsp.enable(server)		-- for Neovim versions including or after 0.11
end

local ok_cmp, cmp = pcall(require, 'cmp')	-- Not available until PlugInstall has run
if ok_cmp then
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
end

-- Diagnostic navigation mappings
vim.keymap.set('n', ']d', function() vim.diagnostic.jump({ count = 1, float = true }) end, { desc = "Go to next diagnostic" })
vim.keymap.set('n', '[d', function() vim.diagnostic.jump({ count = -1, float = true }) end, { desc = "Go to previous diagnostic" })

local diagnostics_auto_enabled = false
local diagnostics_autocmd_id = nil

-- Function to toggle diagnostic auto-display
local function toggle_diagnostics_auto()
	if diagnostics_auto_enabled then
		-- Remove the autocommand if it exists
		if diagnostics_autocmd_id then
			vim.api.nvim_del_autocmd(diagnostics_autocmd_id)
			diagnostics_autocmd_id = nil
		end
		diagnostics_auto_enabled = false
		print("Diagnostic auto-display disabled")
	else
		-- Create the autocommand
		diagnostics_autocmd_id = vim.api.nvim_create_autocmd("CursorHold", {
			callback = function()
				vim.diagnostic.open_float(nil, { focusable = false, scope = "cursor" })
			end,
		})
		diagnostics_auto_enabled = true
		print("Diagnostic auto-display enabled")
	end
end


-- Keybinding to toggle diagnostic auto-display
vim.keymap.set('n', '<leader>e', toggle_diagnostics_auto, { desc = "Toggle diagnostic auto-display" })

-- Optional: Manual trigger to show diagnostics immediately
vim.keymap.set('n', '<leader>E', vim.diagnostic.open_float, { desc = "Show diagnostic under cursor" })

-- Copy Diagnostics

local function copy_diagnostics()
	local bufnr = vim.api.nvim_get_current_buf()
	local line = vim.api.nvim_win_get_cursor(0)[1] - 1  -- 0-indexed
	local diags = vim.diagnostic.get(bufnr, { lnum = line })
	if #diags == 0 then
		print("No diagnostics on this line")
		return
	end

	local messages = {}
	for _, diag in ipairs(diags) do
		table.insert(messages, diag.message)
	end

	local all_msg = table.concat(messages, "\n")
	vim.fn.setreg('+', all_msg)  -- copy to system clipboard
	print("Copied diagnostics to clipboard")
end

-- Keybinding to copy diagnostics

vim.keymap.set('n', '<leader>y', copy_diagnostics, { desc = "Copy diagnostics under cursor" })

--- DAP ---

-- Load nvim-dap and dap-ui
local ok_dap, dap = pcall(require, 'dap')
local ok_dapui, dapui = pcall(require, 'dapui')
if not (ok_dap and ok_dapui) then return end	-- Not available until PlugInstall has run

-- dap-ui setup

dapui.setup({
	icons = { expanded = "▾", collapsed = "▸"},
	mappings = {
		expand = { "<CR>", "<2-LeftMouse>" },
		open = 'o',
		remove = 'd',
		edit = "e",
		repl = "r",
	},
	layouts = {
		{
			elements = {
				"scopes",
				"breakpoints",
				"stacks",
				"watches",
			},
			size = 40, -- width of the side panel
			position = "left",
		},
		{
			elements = {
				"repl",
			},
			size = 10, -- height of the bottom panel
			position = "bottom",
		},
	},
	floating = {
		max_height = nil,
		max_width = nil,
		border = "rounded",
		mappings = {
			close = { "q", "<Esc>" },
		},
	},
})

-- Open dap-ui automatically when debugging starts
dap.listeners.after.event_initialized["dapui_config"] = function()
	dapui.open()
end

-- Close dap-ui automatically when debugging ends
dap.listeners.before.event_terminated["dapui_config"] = function()
	dapui.close()
end
dap.listeners.before.event_exited["dapui_config"] = function()
	dapui.close()
end

-- Configure Python adapter
dap.adapters.python = {
	type = 'executable';
	command = 'python';
	args = { '-m', 'debugpy.adapter' };
}

-- Configure Python debug configurations
dap.configurations.python = {
	{
		type = 'python';
		request = 'launch';
		name = "Launch file";
		program = "${file}";
		pythonPath = function()
			return '/usr/bin/python'  -- change to your Python path
		end;
	},
}

-- Keybindings for DAP
vim.api.nvim_set_keymap('n', '<F5>', "<cmd>lua require'dap'.continue()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<F10>', "<cmd>lua require'dap'.step_over()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<F11>', "<cmd>lua require'dap'.step_into()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<F12>', "<cmd>lua require'dap'.step_out()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>db', "<cmd>lua require'dap'.toggle_breakpoint()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>B', "<cmd>lua require'dap'.set_breakpoint(vim.fn.input('Breakpoint condition: '))<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>dr', "<cmd>lua require'dap'.repl.open()<CR>", { noremap = true, silent = true })
vim.api.nvim_set_keymap('n', '<leader>dl', "<cmd>lua require'dap'.run_last()<CR>", { noremap = true, silent = true })
