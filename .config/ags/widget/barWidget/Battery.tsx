import {
  batteryPercent,
  batteryTime,
  batteryLevel,
  batteryState,
} from "../../services/statwatcher"
import { Gtk } from "ags/gtk4"

import { With, createComputed } from "ags"

//

const battery_levels = ["󰂎", "󰁺", "󰁻", "󰁼", "󰁽", "󰁾", "󰁿", "󰂀", "󰂁", "󰂂", "󰁹"]
const charge_levels = ["󰢟", "󰂆", "󰂆", "󰂇", "󰂈", "󰢝", "󰂉", "󰢞", "󰂊", "󰂋", "󰂅"]

function BarColor(batteryLeft: number): string {
  if (batteryLeft > 50) {
    return "color: #74e628;"
  } else if (batteryLeft > 20) {
    return "color: #fff830;"
  } else {
    return "color: #f71515;"
  }
}

function BatteryIcon(
  batteryStatename: string,
  batteryLevelNum: number,
): string {
  if (batteryStatename === "battery") {
    return battery_levels[batteryLevelNum]
  } else if (batteryStatename === "charge") {
    return battery_levels[batteryLevelNum]
  } else if (batteryStatename === "full") {
    return "󰂄"
  } else {
    return "󰂎"
  }
}

export default function Battery(configs: { [key: string]: string }) {
  const align = configs.align

  const colorClass = createComputed(() => BarColor(batteryPercent.get()))
  const iconSymbol = createComputed(() =>
    BatteryIcon(batteryState.get(), batteryLevel.get()),
  )
  const isCharging = createComputed(() => {
    if (batteryState.get() === "charge" || batteryState.get() === "full") {
      return "󱐋"
    } else if (batteryState.get() === "battery") {
      return ""
    } else {
      return ""
    }
  })

  const hoverText = batteryTime((timeleft) => {
    let descText = ""
    let batState = batteryState.get()
    if (batState === "charge") {
      descText = `Time until full: ${timeleft}`
    } else if (batState === "full") {
      descText = "Battery full"
    } else if (batState === "battery") {
      descText = `Time left: ${timeleft}`
    } else {
      descText = `Loading... (state = ${batState})`
    }

    return '<span size="small" style="italic">' + descText + "</span>"
  })

  return (
    <box class="battery" tooltipMarkup={hoverText}>
      <With value={batteryTime}>
        {() => {
          return (
            <box>
              <label class="status-label" label={isCharging} />
              <overlay>
                <label
                  halign={Gtk.Align.CENTER}
                  valign={Gtk.Align.CENTER}
                  class="back-label"
                  label={iconSymbol}
                  css={colorClass}
                />

                <label
                  $type="overlay"
                  class="top-label"
                  label="󰂎"
                  halign={Gtk.Align.CENTER}
                  valign={Gtk.Align.CENTER}
                />
              </overlay>
            </box>
          )
        }}
      </With>
      <label class="percent-label" label={batteryPercent} />
    </box>
  )
}
