import { Astal, Gdk } from "ags/gtk4"
import Bar from "../widget/Bar"

export default function DP2(gdkmonitor: Gdk.Monitor) {
  const { TOP, LEFT, RIGHT } = Astal.WindowAnchor

  let mainBar = (
    <Bar anchor={TOP | LEFT | RIGHT} gdkmonitor={gdkmonitor} height="10" />
  )
  return <box />
}
