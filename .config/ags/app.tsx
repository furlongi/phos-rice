import app from "ags/gtk4/app"

import style from "./styles/main.scss"

import DP1 from "./monitor/dp1"
import DP2 from "./monitor/dp2"
import DP3 from "./monitor/dp3"

app.start({
  css: style,
  main() {
    app.get_monitors().forEach((monitor) => {
      console.log(monitor.connector)
      switch (monitor.connector) {
        case "DP-1":
          DP1(monitor)
          break
        case "DP-2":
          DP2(monitor)
          break
        case "DP-3":
          DP3(monitor)
          break
        default:
          break
      }
    })
  },
})

// Research
// Theme changer with images: https://github.com/0thElement/nixconf
// Change Bar color with themes dynamically: https://github.com/JohnOberhauser/dotfiles
// https://github.com/JohnOberhauser/OkPanel

// https://github.com/thelazt16/dotfiles has some styles for cpu widgets
// Although this one better https://github.com/Jas-SinghFSU/HyprPanel

// Slanted css icons https://github.com/AymanLyesri/ArchEclipse
// Another but better https://github.com/kotontrion/dotfiles

// https://aylur.github.io/astal/guide/introduction
// https://docs.gtk.org/gtk4/css-properties.html
// https://aylur.github.io/libastal/astal4/index.html

// css:
// cssName, Class in the element, and css div.Class > cssName
// labelCss, .cssname
// backgroundCss, .cssname

// paddings: top right bottom left
