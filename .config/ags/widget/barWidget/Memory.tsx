import { ramUsage } from "../../services/statwatcher"

export default function Memory(configs: { [key: string]: string }) {
  const align = configs.align

  return (
    <box visible class="cpu" cssName="barCpu" halign={align}>
      <label label={ramUsage} />
    </box>
  )
}
