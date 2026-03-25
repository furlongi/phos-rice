import { interval } from "ags/time"
import { exec } from "ags/process"

import { createState } from "ags"

export const [cpuUsage, setCpuUsage] = createState("")
export const [ramUsage, setRamUsage] = createState("")

interval(5000, () => {
  let cpuUse = exec("phoscli cpu")
  setCpuUsage(cpuUse + "% ")
})

interval(5000, () => {
  let ramUse = exec("phoscli ram")
  setRamUsage(ramUse + "% ")
})
