-- Paths
local device_home = "/home/main"

-- Plugins

-- Startup --
hl.on("hyprland.start", function()
    hl.exec_cmd("sudo systemctl enable tlp.service")
    hl.exec_cmd("sudo systemctl enable tlp-pd.service")
    hl.exec_cmd("libinput-gestures-setup start")
end)


-- Appearances --
-- Do these even work?
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_SIZE", "12")
hl.env("HYPRCURSOR_THEME", "Sweet-cursors")
hl.env("XCURSOR_THEME", "Sweet-cursors")


-- Inputs --
hl.config({
    input = {
        accel_profile = "adaptive"
    },

    cursor = {
        default_monitor = "eDP-1"
    }
})


-- Power Hungry --
hl.config({
    decoration = {
        shadow = {
            enabled = false
        },
        blur = {
            enabled = false
        }
    }
})


-- Applications --
_Device_obsidian_path = "/home/main/AppImages/obsidian.appimage"
_Device_godot_path = "/home/main/Applications/AppImages/Godot_v4.6.1-stable_mono_linux.x86_64"

_PhosCli_path = "/home/main/Dev/phos-rice/phoscli/bin/phoscli"


-- Workspace Switcher --
WorkspaceMode = "-s"

hl.workspace_rule({workspace = "1", monitor="eDP-1", default = true, persistent = true})
hl.workspace_rule({workspace = "2", monitor="eDP-1", persistent = true})
hl.workspace_rule({workspace = "3", monitor="eDP-1", persistent = true})
hl.workspace_rule({workspace = "4", monitor="eDP-1", persistent = true})
hl.workspace_rule({workspace = "5", monitor="eDP-1", persistent = true})


-- Monitor Layout --
-- See https://wiki.hypr.land/configuring/core/monitors/
-- hyprctl monitors all
-- wdisplays

hl.monitor(
    {
        output = "eDP-1",
        mode = "2880x1800@120.00",
        scale = 2,
        vrr = 1
    }
)

-- Default
hl.monitor(
    {
        output = "", --fallback rule setter
        mode = "preferred",
        position = auto
    }
)
