import Hyprland from "gi://AstalHyprland"

import { createBinding, createComputed, With } from "ags"

export default function Workspaces(configs: { [key: string]: string }) {
  const hypr = Hyprland.get_default()
  const hyprlandActiveWorkspace = createBinding(hypr, "focused_workspace")
  const monitorName = configs.monitorName
  const align = configs.align

  const workProps: { [key: string]: any } = {
    "DP-1": {
      Workspaces: ["1", "2", "3", "4"],
      CurrentActive: "1",
    },
    "DP-2": {
      Workspaces: ["5", "6"],
      CurrentActive: "5",
    },
    "DP-3": {
      Workspaces: ["7", "8"],
      CurrentActive: "6",
    },
    "eDP-1": {
      Workspaces: ["1", "2", "3", "4", "5"],
      CurrentActive: "1",
    },
  }

  return (
    <box visible halign={align}>
      <With value={hyprlandActiveWorkspace}>
        {() => {
          let currentWorkspaceName = hypr.focused_workspace.name
          let currentMonitor = hypr.focused_monitor.name

          return (
            <box visible class="workspace">
              {workProps[monitorName].Workspaces.map(
                (workspaceName: string) => {
                  if (currentMonitor === monitorName) {
                    workProps[monitorName].CurrentActive = currentWorkspaceName
                  }

                  let icon = createComputed(() => {
                    const isActive =
                      currentWorkspaceName === workspaceName ||
                      workspaceName === workProps[monitorName].CurrentActive
                    return isActive ? "" : ""
                  })

                  return <button visible label={icon}></button>
                },
              )}
            </box>
          )
        }}
      </With>
    </box>
  )
}
