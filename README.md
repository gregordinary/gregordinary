## Hi, I'm Greg

I build open tooling for running mainline Linux on ARM boards, mostly Rockchip: flashing, bring-up, image building, and running models on the NPU. Along the way I write rootless Rust tools that are useful on any Linux machine.

### Rocket NPU

These projects run inference on the RK3588's NPU through the mainline `rocket` DRM-accel driver.

<p>
<a href="https://github.com/gregordinary/ggml-rocket"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/ggml-rocket-dark.svg"><img src="cards/ggml-rocket-light.svg" alt="ggml-rocket: Drop-in ggml backend that runs llama.cpp and whisper.cpp prefill on the RK3588 NPU" width="49%"></picture></a>
<a href="https://github.com/gregordinary/rocket-userspace"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/rocket-userspace-dark.svg"><img src="cards/rocket-userspace-light.svg" alt="rocket-userspace: librocketnpu, the userspace driver, matmul and on-NPU op library" width="49%"></picture></a>
</p>

<p>
<a href="https://github.com/gregordinary/ort-rocket"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/ort-rocket-dark.svg"><img src="cards/ort-rocket-light.svg" alt="ort-rocket: ONNX Runtime provider for vision transformers" width="49%"></picture></a>
<a href="https://github.com/gregordinary/tflite-rocket"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/tflite-rocket-dark.svg"><img src="cards/tflite-rocket-light.svg" alt="tflite-rocket: TensorFlow Lite delegate for NPU object detection" width="49%"></picture></a>
</p>

<p>
<a href="https://github.com/gregordinary/rknpu-submit"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/rknpu-submit-dark.svg"><img src="cards/rknpu-submit-light.svg" alt="rknpu-submit: Runs the open NPU stack on a stock vendor BSP kernel" width="49%"></picture></a>
<a href="https://github.com/gregordinary/patches"><picture><source media="(prefers-color-scheme: dark)" srcset="cards/patches-dark.svg"><img src="cards/patches-light.svg" alt="patches: Out-of-tree rocket driver and hardware video-transcode patch sets" width="49%"></picture></a>
</p>

<details>
<summary>How the stack fits together</summary>

```mermaid
flowchart TB
  ggml["ggml-rocket<br/>llama.cpp · whisper.cpp"]
  ort["ort-rocket<br/>ONNX Runtime"]
  tfl["tflite-rocket<br/>TFLite · Frigate"]
  rus["rocket-userspace<br/>librocketnpu"]
  ggml & ort & tfl --> rus
  rus -->|mainline kernel| rocket["rocket DRM-accel driver"]
  rus -->|vendor BSP kernel| rkn["rknpu-submit"]
  rkn --> rknpu["rknpu driver"]
  pat["patches"] -. clock + latency .-> rocket
  rocket & rknpu --> npu[("RK3588 NPU")]
  notes["rockchip-npu-notes"] -. documents .-> npu
```

</details>

---

### Device Bring-up

Getting an OS onto a board: build the image, then flash it.

<dl>
<dt><a href="https://github.com/gregordinary/boot2deb"><b>boot2deb</b></a> <picture><source media="(prefers-color-scheme: dark)" srcset="cards/boot2deb-lang-dark.svg"><img src="cards/boot2deb-lang-light.svg" alt="Rust" height="16" align="absmiddle"></picture></dt>
<dd>Builds a bootable Debian image for an SBC, laptop or tablet from layered TOML config, without root.</dd>
<dt><a href="https://github.com/gregordinary/pyrographer"><b>pyrographer</b></a> <picture><source media="(prefers-color-scheme: dark)" srcset="cards/pyrographer-lang-dark.svg"><img src="cards/pyrographer-lang-light.svg" alt="Rust" height="16" align="absmiddle"></picture></dt>
<dd>Flashes and recovers Rockchip, StarFive JH7110 and Ingenic devices, from a CLI or a GUI.</dd>
</dl>

---

### Rootless Rust Tooling

Filesystems, sandboxes and packages, all built without root.

<dl>
<dt><a href="https://github.com/gregordinary/ferrosys"><b>ferrosys</b></a> <picture><source media="(prefers-color-scheme: dark)" srcset="cards/ferrosys-lang-dark.svg"><img src="cards/ferrosys-lang-light.svg" alt="Rust" height="16" align="absmiddle"></picture></dt>
<dd>Formats and reads ext2/3/4, FAT, exFAT and btrfs images in userspace, with byte-reproducible output.</dd>
<dt><a href="https://github.com/gregordinary/ferroday-cage"><b>ferroday-cage</b></a> <picture><source media="(prefers-color-scheme: dark)" srcset="cards/ferroday-cage-lang-dark.svg"><img src="cards/ferroday-cage-lang-light.svg" alt="Rust" height="16" align="absmiddle"></picture></dt>
<dd>An unprivileged Linux sandbox that can bootstrap a Debian, Alpine or Gentoo root.</dd>
<dt><a href="https://github.com/gregordinary/src2deb"><b>src2deb</b></a> <picture><source media="(prefers-color-scheme: dark)" srcset="cards/src2deb-lang-dark.svg"><img src="cards/src2deb-lang-light.svg" alt="Rust" height="16" align="absmiddle"></picture></dt>
<dd>Builds <code>.deb</code> packages from source inside a sandbox and writes a provenance manifest for each run.</dd>
</dl>

---

### Hardware References

Research notes written to be reused by anyone working with these chips.

<dl>
<dt><a href="https://github.com/gregordinary/rockchip-npu-notes"><b>rockchip-npu-notes</b></a></dt>
<dd>The RK3588 NPU and its regcmd interface, from research and reverse engineering.</dd>
<dt><a href="https://github.com/gregordinary/device-ref"><b>device-ref</b></a></dt>
<dd>RK3288, RK3576 and RK3588 boards on mainline Linux: boot chains, device trees and errata, with every claim graded by its evidence.</dd>
</dl>
