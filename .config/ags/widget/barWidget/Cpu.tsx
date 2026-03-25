import { cpuUsage } from "../../services/statwatcher"

export default function Cpu(configs: { [key: string]: string }) {
  const align = configs.align

  return (
    <box visible class="cpu" cssName="barCpu" halign={align}>
      <label label={cpuUsage} />
    </box>
  )
}
