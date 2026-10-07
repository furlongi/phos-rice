-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#input
hl.config({
    input = {
        numlock_by_default = true,

        repeat_rate = 35,
        repeat_delay = 500,

        -- Turn off hover focus
        follow_mouse = 2,

        focus_on_close = 1,
        natural_scroll = false,

        touchpad = {
            disable_while_typing = false,
            natural_scroll = false,
            scroll_factor = 1.0,

            middle_button_emulation = true,
            tap_to_click = true,
            drag_lock = 1,
            tap_and_drag = true,
        },
    },

    -- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#group
    group = {
        auto_group = false -- keep it off dont want it
    },

    -- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#binds
    binds = {
        workspace_center_on = 1
    },

    -- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#cursor
    cursor = {
        -- Dont change this one - needed for multi monitor
        no_hardware_cursors = 1,
        no_break_fs_vrr = 0, -- default is 2, check if full screen games are badly affected
        min_refresh_rate = 24, -- default, wont work with above disabled
        hotspot_padding = 1,
        inactive_timeout = 15,
        warp_on_toggle_special = 0,
    }
})