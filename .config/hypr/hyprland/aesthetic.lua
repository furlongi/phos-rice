-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#general
hl.config({
    general = {
        layout = "dwindle",

        border_size = 3,
        gaps_in = 5,
        gaps_out = 10,
        float_gaps = 10,
        gaps_workspaces = 5,

        -- TODO - Dynamic color
        -- https://wiki.hyprland.org/Configuring/Variables/#variable-types
        -- Example: rgba(33ccffee) rgba(00ff99ee) 45deg
        col = {
            -- inactive_border = "rgba(75,75,75,0.8)",
            -- active_border = {
                -- colors = { "rgb(79,47,102)", "rgb(80,145,169)" },
                -- angle = 45,
            -- },
            -- nogroup_border = "0xffffaaff",
        },

        resize_on_border = true,
        extend_border_grab_area = 15,
        hover_icon_on_border = true,
        resize_corner = 0, -- All corners can be resized

        no_focus_fallback =  false,

        -- https://wiki.hypr.land/0.56.0/Configuring/Advanced-and-Cool/Tearing/
        -- Not needed for my use cases
        allow_tearing = false,

        snap = {
            enabled = true,
            window_gap = 40,
            monitor_gap = 40,

            border_overlap = true,
            respect_gaps = true,
        },
    }
})

-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#decoration
hl.config({
    decoration = {
        rounding = 10,
        rounding_power = 2.0,

        -- Defaults --
        active_opacity = 1,
        inactive_opacity = 1,
        fullscreen_opacity = 1,

        dim_modal = true,
        dim_inactive = false,
        dim_strength = 0.5,
        dim_special = 0.2,
        dim_around = 0.4,
        screen_shader = "",
        border_part_of_window = true,

        shadow = {
            range = 10,
            render_power = 2,
            sharp = false,
            -- TODO: Maybe make this dynamic color
            -- https://rgbacolorpicker.com/
            -- https://rgbacolorpicker.com/rgba-to-hex
            -- color = "0xee1a1a1a",
            offset = {0, 0},
            scale = 1.0,
        },

        blur = {
            brightness = 0.8,
            size = 4,
            vibrancy = 0.1696
        }
    }
})

-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#decoration
hl.config({
    animations = {
        enabled = true,
        workspace_wraparound = false,

        -- https://wiki.hypr.land/Configuring/Animations/#curves
        -- https://www.cssportal.com/css-cubic-bezier-generator/
        -- https://easings.net/
        
        -- Curves --
        -- x0, y0, x1, y1
        hl.curve( "easeInOutBack", { type = "bezier", points = { { 0.68, -0.6 }, { 0.32, 1.6 } } }),
        hl.curve( "easeOutCubic",  { type = "bezier", points = { { 0.33,    1 }, { 0.68,   1 } } }),
        hl.curve( "easeInCubic",   { type = "bezier", points = { { 0.32,    0 }, { 0.67,   0 } } }),
        hl.curve( "emphasizedAccel", { type = "bezier", points = { {  0.3,   0 }, { 0.8, 0.15 } } }),
        hl.curve( "emphasizedDecel", { type = "bezier", points = { { 0.05, 0.7 }, { 0.1,    1 } } }),
        hl.curve( "bounce", { type = "bezier", points = { {  0.0, 1.59 }, { 0.57, 0.69 } } }),
        hl.curve( "linear", { type = "bezier", points = { {    0,    0 }, {    1,    1 } } }),
        hl.curve( "quick",  { type = "bezier", points = { { 0.15,    0 }, {  0.1,    1 } } }),
        hl.curve( "almostLinear", { type = "bezier", points = { { 0.5, 1 }, { 0.89, 1 } } }),

        -- Animations --
        hl.animation({ leaf = "global", enabled = 1, speed = 7, bezier = "default"}),
            hl.animation({ leaf = "windows", enabled = 1, speed = 4, bezier = "easeOutCubic"}),
                hl.animation({ leaf = "windowsIn", enabled = 1, speed = 2, bezier = "emphasizedAccel", style = "popin 30%"}),
                hl.animation({ leaf = "windowsOut", enabled = 1, speed = 5, bezier = "easeOutCubic", style = "slide"}),
                hl.animation({ leaf = "windowsMove", enabled = 1, speed = 7, bezier = "emphasizedDecel"}),
            hl.animation({ leaf = "layers", enabled = 1, speed = 4, bezier = "easeOutCubic"}),
                hl.animation({ leaf = "layersIn", enabled = 1, speed = 4, bezier = "easeOutCubic", style = "fade"}),
                hl.animation({ leaf = "layersOut", enabled = 1, speed = 1.5, bezier = "linear", style = "fade"}),
            hl.animation({ leaf = "fade", enabled = 1, speed = 3, bezier = "quick"}),
                hl.animation({ leaf = "fadeIn", enabled = 1, speed = 3, bezier = "emphasizedAccel"}),
                hl.animation({ leaf = "fadeOut", enabled = 1, speed = 2.5, bezier = "almostLinear"}),
                hl.animation({ leaf = "fadeDim", enabled = 1, speed = 6, bezier = "default"}),
                hl.animation({ leaf = "fadeLayers", enabled = 1, speed = 5, bezier = "default"}),
                    hl.animation({ leaf = "fadeLayersIn", enabled = 1, speed = 2, bezier = "almostLinear"}),
                    hl.animation({ leaf = "fadeLayersOut", enabled = 1, speed = 2, bezier = "almostLinear"}),
                hl.animation({ leaf = "fadePopups", enabled = 1, speed = 4, bezier = "easeOutCubic"}),
                hl.animation({ leaf = "fadeDpms", enabled = 1, speed = 10, bezier = "easeOutCubic"}),
            hl.animation({ leaf = "border", enabled = 1, speed = 3, bezier = "easeOutCubic"}),
            hl.animation({ leaf = "workspaces", enabled = 1, speed = 2, bezier = "almostLinear", style = "fade"}),
                hl.animation({ leaf = "specialWorkspace", enabled = 1, speed = 5, bezier = "easeInOutBack", style = "slidevert -30%"}),
    }
})
