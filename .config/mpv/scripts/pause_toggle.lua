-- Adds an additional keybinding to pause an unpaused mpv

local mp = require 'mp'
local utils = require 'mp.utils'
local msg = require 'mp.msg'

local opts = {

	pause_toggle = "\\"

}

(require 'mp.options').read_options(opts, "pause_toggle")
-- main
-- keybind to toggle pause

mp.add_key_binding(opts.pause_toggle, "pause_toggle", function()
	if (mp.get_property('pause') == "no") then
		mp.commandv('cycle', 'pause')
	end
end)

