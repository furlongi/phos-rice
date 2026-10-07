-- Desktop --
Terminal = "kitty"
FileManager = "dolphin"
Browser = "brave-browser --enable-features=UseOzonePlatform --ozone-platform=wayland --password-store=kwallet6"
Browser_alt = "librewolf --enable-features=UseOzonePlatform --ozone-platform=wayland"
Menu = "pgrep wofi >/dev/null 2>&1 && killall wofi || wofi --show drun --conf=/etc/wofi/config --style=/etc/wofi/style.css"


-- Apps --
Obsidian = _Device_obsidian_path
Discord = "discord --enable-features=UseOzonePlatform --ozone-platform=wayland"
Vscode = "codium --enable-features=UseOzonePlatform --ozone-platform=wayland"
Zed = "zed"
Blender = "blender"
Godot = _Device_godot_path .. " --single-window"
Intellij_rider = "rider -Dawt.toolkit.name=WLToolkit"
Intellij_rust = "rustrover"
Steam = "steam"
Winboat = "winboat"
Virtmachine = "virt-manager"


-- Scripts --
WorkspaceSwitcher = "$hypr_scripts/workspaces_switcher.py"
WallpaperChange = "$hypr/swww/swww_randomizer.sh"
PhosCli = _PhosCli_path


-- Tools --
Screenshot = "slurp | grim -g- - | wl-copy"