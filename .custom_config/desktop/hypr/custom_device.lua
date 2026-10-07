-- Paths
local device_home = "/home/main"

-- Plugins


-- Appearance --
-- Do these even work?
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "12")
hl.env("HYPRCURSOR_THEME", "Sweet-cursors")
hl.env("XCURSOR_THEME", "Sweet-cursors")


-- Power Hungry
hl.config({
    decoration = {
        shadow = {
            enabled = true
        },
        blur = {
            enabled = true
        }
    }
})

-- Input --
hl.config({
    input = {
        accel_profile = "adaptive"
    },
    cursor = {
        default_monitor = "DP-1"
    }
})


-- Applications --
_Device_obsidian_path = device_home .. "/AppImages/obsidian.appimage"
_Device_godot_path = device_home .. "/Applications/Godot/Godot_v4.6.1-stable_mono_linux.x86_64"
_PhosCli_path = device_home .. "/Dev/phos-rice/phoscli/bin/phoscli"


-- Workspace --
WorkspaceMode = ""

hl.workspace_rule({workspace = "1", monitor = "DP-1", default = true, persistent = true})
hl.workspace_rule({workspace = "2", monitor = "DP-1", persistent = true})
hl.workspace_rule({workspace = "3", monitor = "DP-1", persistent = true})
hl.workspace_rule({workspace = "4", monitor = "DP-1", persistent = true})
hl.workspace_rule({workspace = "5", monitor = "DP-1", persistent = true})
hl.workspace_rule({workspace = "6", monitor = "DP-2", default = true, persistent = true})
hl.workspace_rule({workspace = "7", monitor = "DP-2", persistent = true})
hl.workspace_rule({workspace = "8", monitor = "DP-3", persistent = true})
hl.workspace_rule({workspace = "9", monitor = "DP-3", persistent = true})
hl.workspace_rule({workspace = "10", monitor = "HDMI-A-1", default = true, persistent = true})


-- Monitor Layout -- 
-- https://wiki.hypr.land/configuring/core/monitors/
-- hyprctl monitors all
-- wdisplays

-- From Left to Right
-- Drawing Pad
hl.monitor(
    {
        output   = "HDMI-A-1",
        mode     = "1920x1080@60.00",
        position = "0x2530",
        scale    = 1,
        vrr      = 1,
    }
)

-- Spare Asus on Left
hl.monitor(
    {
        output    = "DP-1",
        mode      = "3440x1440@143.92",
        position  = "1080x610",
        bitdepth  = 10,
        vrr       = 1,
    }
)

-- Main LG Monitor (non spyware)
hl.monitor(
    {
        output    = "DP-2",
        mode      = "1920x1080@119.98",
        position  = "0x610",
        scale     = 1,
        transform = 1,
        vrr       = 1,
    }
)

-- MSI Vertical Right
hl.monitor(
    {
        output    = "DP-3",
        mode      = "2560x1440@120",
        position  = "4520x0",
        scale     = 1,
        transform = 3,
        vrr       = 1,
    }
)

-- Default
hl.monitor(
    {
        output    = "", --fallback rule setter
        mode      = "preferred",
        position  = "auto",
    }
)