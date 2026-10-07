-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Binds/
-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Dispatchers/
-- dnf in wev
-- For checking keys

local appMod = "SUPER + "
local appModSh = "SUPER + SHIFT + "
local commandMod = "SUPER + CONTROL + "
local commandModSh = "SUPER + CONTROL + SHIFT + "
local altMod = "SUPER + ALT + "

local leftMouseKey = "mouse:272"
local rightMouseKey = "mouse:273"
local middleMouseKey = "mouse:274"

local noct_ipc = "noctalia msg "


-- Desktop --
hl.bind(appMod .. "Q", hl.dsp.window.close())
hl.bind(appModSh .. "Q", hl.dsp.window.kill())
hl.bind(appMod .. leftMouseKey, hl.dsp.window.drag(), { mouse = true })
hl.bind(appMod .. rightMouseKey, hl.dsp.window.resize(), { mouse = true })

hl.bind(commandMod .. "F", hl.dsp.window.float())
hl.bind(commandMod .. "C", hl.dsp.exec_cmd("hyprctl reload"))

hl.bind(altMod .. "F", hl.dsp.window.fullscreen())

hl.bind("ALT + TAB", hl.dsp.window.cycle_next())
hl.bind("ALT + SHIFT + TAB", hl.dsp.window.cycle_next({next = false}))


-- Rice Apps --
-- hl.bind(appMod .. "SPACE", hl.dsp.exec_cmd(Menu))
-- hl.bind(appMod .. "N", hl.dsp.exec_cmd("swaync-client -t"))

-- Applications --
hl.bind(appMod .. "Return", hl.dsp.exec_cmd(Terminal))
hl.bind(appMod .. "E", hl.dsp.exec_cmd(FileManager))
hl.bind(appMod .. "B", hl.dsp.exec_cmd(Browser))
hl.bind(appModSh .. "B", hl.dsp.exec_cmd(Browser_alt))
hl.bind(appMod .. "C", hl.dsp.exec_cmd(Vscode))
hl.bind(appModSh .. "C", hl.dsp.exec_cmd(Zed))
hl.bind(appMod .. "O", hl.dsp.exec_cmd(Obsidian))
hl.bind(appMod .. "D", hl.dsp.exec_cmd(Discord))
hl.bind(appMod .. "P", hl.dsp.exec_cmd(Blender))
hl.bind(appMod .. "G", hl.dsp.exec_cmd(Godot))
hl.bind(appMod .. "R", hl.dsp.exec_cmd(Intellij_rider))
hl.bind(appModSh .. "R", hl.dsp.exec_cmd(Intellij_rust))
hl.bind(appMod .. "S", hl.dsp.exec_cmd(Steam))
hl.bind(appMod .. "V", hl.dsp.exec_cmd(Winboat))
hl.bind(appModSh .. "V", hl.dsp.exec_cmd(Virtmachine))


-- Tiling / Layout --
hl.bind(appMod .. "Left", hl.dsp.focus({ direction = "l" }), { submap_universal = true })
hl.bind(appMod .. "Right", hl.dsp.focus({ direction = "r" }), { submap_universal = true })
hl.bind(appMod .. "Up", hl.dsp.focus({ direction = "u" }), { submap_universal = true })
hl.bind(appMod .. "Down", hl.dsp.focus({ direction = "d" }), { submap_universal = true })

hl.bind(appModSh .. "Left", hl.dsp.window.move({ direction = "l" }))
hl.bind(appModSh .. "Right", hl.dsp.window.move({ direction = "r" }))
hl.bind(appModSh .. "Up", hl.dsp.window.move({ direction = "u" }))
hl.bind(appModSh .. "Down", hl.dsp.window.move({ direction = "d" }))

-- Off because hy3 not up to date -- TODO
-- bindo = $appModSh, left, exec, $phosCli tiling l
-- bindo = $appModSh, right, exec, $phosCli tiling r

-- Resizing --
local sizeMod = 15
hl.bind(commandMod .. "R", hl.dsp.submap("resize"))
hl.define_submap("resize", function()
    hl.bind("Right + Up", hl.dsp.window.resize({ x = sizeMod, y = -sizeMod, relative = true}), { repeating = true })
    hl.bind("Right + Down", hl.dsp.window.resize({ x = sizeMod, y = sizeMod, relative = true}), { repeating = true })
    hl.bind("Left + Up", hl.dsp.window.resize({ x = -sizeMod, y = -sizeMod, relative = true}), { repeating = true })
    hl.bind("Left + Down", hl.dsp.window.resize({ x = -sizeMod, y = sizeMod, relative = true}), { repeating = true })

    hl.bind("Right", hl.dsp.window.resize({ x = sizeMod, y = 0, relative = true}), { repeating = true })
    hl.bind("Left", hl.dsp.window.resize({ x = -sizeMod, y = 0, relative = true}), { repeating = true })
    hl.bind("Up", hl.dsp.window.resize({ x = 0, y = -sizeMod, relative = true}), { repeating = true })
    hl.bind("Down", hl.dsp.window.resize({ x = 0, y = sizeMod, relative = true}), { repeating = true })
    
    hl.bind("escape",  hl.dsp.submap("reset"))
end)

-- Workspaces --
hl.bind(commandMod .. "Right", hl.dsp.exec_cmd(PhosCli .. " workspace r " .. WorkspaceMode))
hl.bind(commandMod .. "Left", hl.dsp.exec_cmd(PhosCli .. " workspace l " .. WorkspaceMode))
hl.bind(commandModSh .. "Right", hl.dsp.exec_cmd(PhosCli .. " workspace r -w " .. WorkspaceMode))
hl.bind(commandModSh .. "Left", hl.dsp.exec_cmd(PhosCli .. " workspace l -w " .. WorkspaceMode))


-- Scratchpad --
hl.bind(appMod .. "1", hl.dsp.workspace.toggle_special("mainPad"))
hl.bind(appMod .. "2", hl.dsp.workspace.toggle_special("sidePad"))
hl.bind(appMod .. "3", hl.dsp.workspace.toggle_special("other"))

hl.bind(appModSh .. "1", hl.dsp.window.move({ workspace = "special:mainPad" }))
hl.bind(appModSh .. "2", hl.dsp.window.move({ workspace = "special:sidePad" }))
hl.bind(appModSh .. "3", hl.dsp.window.move({ workspace = "special:other" }))


-- Power --
hl.bind(altMod .. "P", hl.dsp.submap("power"))
hl.define_submap("power", "reset", function()
    hl.bind("L", hl.dsp.exec_cmd(noct_ipc .. "session lock"))
    hl.bind("S", hl.dsp.exec_cmd("noctalia msg session lock;sleep1;hyprctl dispatch dpms off;sleep 2;systemctl suspend"))
    hl.bind("H", hl.dsp.exec_cmd("sleep 2 & systemctl hibernate"))
    hl.bind("R", hl.dsp.exec_cmd("sleep 2 & systemctl reboot"))
    hl.bind("Q", hl.dsp.exec_cmd("sleep 2 & systemctl poweroff"))
    
    hl.bind("escape",  hl.dsp.submap("power"))
end)


-- Tools --
hl.bind(appModSh .. "S", hl.dsp.exec_cmd(Screenshot))


-- Audio / Multimedia --
-- Requires playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl position +5"), { locked = true })
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),        { locked = true, long_press = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl position -5"), { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),    { locked = true, long_press = true  })

hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"),  { locked = true })

-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),     { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 10%+"),                 { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 10%-"),                 { locked = true, repeating = true })


-- Noctalia Protocols --


-- Core binds
hl.bind(appMod .. "+ Space", hl.dsp.exec_cmd(noct_ipc .. "panel-toggle launcher"))
hl.bind(appMod .. "+ grave", hl.dsp.exec_cmd(noct_ipc .. "panel-toggle control-center"))
hl.bind(commandMod .. "+ W", hl.dsp.exec_cmd(noct_ipc .. "panel-toggle wallpaper"))
hl.bind(commandModSh .. "+ W", hl.dsp.exec_cmd(noct_ipc .. "panel-toggle noctalia/mpvpaper:picker"))
hl.bind(commandMod .. "+ comma", hl.dsp.exec_cmd(noct_ipc .. "settings-toggle"))
hl.bind("ALT + Tab", hl.dsp.exec_cmd(noct_ipc .. "window-switcher hold"))

-- Media keys
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd(noct_ipc .. "volume-up"))
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd(noct_ipc .. "volume-down"))
hl.bind("XF86AudioMute", hl.dsp.exec_cmd(noct_ipc .. "volume-mute"))
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd(noct_ipc .. "brightness-up"))
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd(noct_ipc .. "brightness-down"))

-- Noctalia Settings
hl.window_rule({
    match = { class = "dev.noctalia.Noctalia" },
    float = true,
    size = { 1080, 920 },
})