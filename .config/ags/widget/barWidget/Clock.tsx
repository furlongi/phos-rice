import { createPoll } from "ags/time"
import GLib from "gi://GLib?version=2.0"

export default function Clock() {
  const time = createPoll("", 1000, () => {
    return GLib.DateTime.new_now_local().format("%a %I:%M")!
  })

  return (
    <box visible class="Clock" cssName="barClock">
      <label label={time} />
    </box>
  )
}
