import { Astal, Gtk, Gdk } from "ags/gtk4"
import Bar from "../widget/barWidget/Bar"

export default function DP3(gdkmonitor: Gdk.Monitor) {
  const { TOP, LEFT, RIGHT } = Astal.WindowAnchor

  let mainBar = (
    <Bar anchor={TOP | LEFT | RIGHT} gdkmonitor={gdkmonitor} height="10" />
  )
  return <box />
}
