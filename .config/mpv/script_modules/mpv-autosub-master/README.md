# [Automatic subtitle downloading for MPV](https://github.com/davidde/mpv-autosub)
* Cross-platform: **Windows, Mac and Linux**
* Multi-language support
* Subtitle provider login support
* **No hotkeys required**: opening a video will automatically trigger subtitles to download  
  (Only when the right subtitles are not yet present)

## Dependencies
This Lua script uses the [Python](https://www.python.org/downloads/) program
[subliminal](https://github.com/Diaoul/subliminal) to download subtitles.
Make sure you have both installed:  
```bash
pip install subliminal
```

## Setup
1. Copy autosub.lua into:

   |       OS      |                      Path                           |
   |---------------|-----------------------------------------------------|
   | **Windows**   | [Drive]:\Users\\[User]\AppData\Roaming\mpv\scripts\ |
   | **Mac/Linux** | ~/.config/mpv/scripts/                              |

   ```bash
   mkdir ~/.config/mpv/scripts
   cat > ~/.config/mpv/scripts/autosub.lua
   [Paste script contents and CTRL+D]
   ```
2. Specify the correct subliminal location for your system:  
   - To determine the correct path, use:  

     |       OS      |      App       |        Command          |
     |---------------|----------------|-------------------------|
     | **Windows**   | Command Prompt |    where subliminal     |
     | **Mac/Linux** | Terminal       |    which subliminal     |

   - Copy this path to the subliminal variable at the start of the script:
     ```lua
     local subliminal = '/path/to/your/subliminal'
     ```
     On Windows, the backslashes in the path need to be escaped, e.g.:  
     **C:\\\\Users\\\\Administrator\\\\AppData\\\\Local\\\\Programs\\\\Python\\\\Python37\\\\Scripts\\\\subliminal.exe**

## Customization
* Optionally change the subtitle languages / [ISO codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).
  Be sure to put your preferred language at the top of the list.  
  If necessary, you can manually trigger downloading your first choice language by pressing `b`,  
  or your second choice language by pressing `n`.
* Optionally specify the login credentials for your preferred subtitle provider(s), if you have one.
* If you do not care for the automatic downloading functionality, and only wish to use the hotkeys,  
  simply change the `auto` bool to `false`.
* For added convenience, you can specify the locations to exclude from auto-downloading subtitles, or alternatively,  
the *only* locations that *should* auto-download subtitles.

This script is under the [MIT License](./LICENSE-MIT),
so you are free to modify and adapt this script to your needs:  
check out the [MPV Lua API](https://mpv.io/manual/stable/#lua-scripting) for more information.

If you find yourself unable to find the correct subtitles for some niche movies/series,
you might be interested in the [submod](https://github.com/davidde/submod_rs)
command line tool I've written to manually correct subtitle timing.

## Credits
Inspired by [selsta's](https://gist.github.com/selsta/ce3fb37e775dbd15c698) and
[fullmetalsheep's](https://gist.github.com/fullmetalsheep/28c397b200a7348027d983f31a7eddfa) autosub scripts.
