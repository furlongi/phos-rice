import { Astal, Gdk } from "ags/gtk4"
import LaptopBar from "../widget/LaptopBar"

export default function eDP1(gdkmonitor: Gdk.Monitor) {
  const { TOP, LEFT, RIGHT } = Astal.WindowAnchor

  let mainBar = (
    <LaptopBar anchor={TOP | LEFT | RIGHT} gdkmonitor={gdkmonitor} height="10" />
  )
  return <box />
}
