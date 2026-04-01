import { interval } from "ags/time"
import { exec } from "ags/process"

import { createState } from "ags"

export const [cpuUsage, setCpuUsage] = createState("")
export const [ramUsage, setRamUsage] = createState("")
export const [batteryPercent, setBatteryPercent] = createState("")
export const [batteryTime, setBatteryTime] = createState("")
export const [batteryState, setBatteryState] = createState<string>("")
export const [batteryLevel, setBatteryLevel] = createState<string>(0)

interval(5500, () => {
  let cpuUse = exec("phoscli cpu")
  setCpuUsage(cpuUse + "% ")
})

interval(6500, () => {
  let ramUse = exec("phoscli ram")
  setRamUsage(ramUse + "% ")
})

interval(2300, () => {
  let batteryInf = exec("phoscli battery")
  let jBatteryInf = JSON.parse(batteryInf)

  setBatteryPercent(jBatteryInf["percent"])
  setBatteryTime(jBatteryInf["time"])
  setBatteryState(jBatteryInf["tstate"])
  setBatteryLevel(parseInt(jBatteryInf["percent_level"]))
})
