import app from "ags/gtk4/app"
import { Astal, Gtk, Gdk } from "ags/gtk4"
import Clock from "./barWidget/Clock"
import Cpu from "./barWidget/Cpu"
import Memory from "./barWidget/Memory"
import Workspaces from "./barWidget/Workspaces"

export default function Bar(configs: { [key: string]: string }) {
  const confAnchor = configs.anchor
  const confMonitor: Gdk.Monitor = configs.gdkmonitor
  const height: Gdk.Monitor = configs.height

  return (
    <window
      visible
      name={`bar-${confMonitor.connector}`}
      class="Bar"
      gdkmonitor={confMonitor}
      exclusivity={Astal.Exclusivity.EXCLUSIVE}
      anchor={confAnchor}
      application={app}
      default-height={height}
    >
      <centerbox
        startWidget={
          <box>
            <Workspaces
              monitorName={confMonitor.connector}
              align={Gtk.Align.Start}
            />
            <Cpu align={Gtk.Align.Start} />
            <Memory align={Gtk.Align.Start} />
          </box>
        }
        centerWidget={
          <box>
            <Clock />
          </box>
        }
        // endWidget=
      />
    </window>
  )
}
