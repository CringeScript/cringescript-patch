<h1 align="center">⚡ Cringescript Patch</h1>

<p align="center">
  <b>Clean, one-click Roblox FPS optimizer for Windows.</b><br>
  Applies an Nvidia GPU profile and injects performance FastFlags.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-blue?style=flat-square" alt="Windows" />
  <img src="https://img.shields.io/badge/Python-3.7%2B-yellow?style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License" />
</p>

<p align="center">
  <i>The name is cringe, the FPS boost is not.</i>
</p>

---

## ✨ Features

- 🖥️ **Nvidia GPU Profile** — Applies performance-tuned settings automatically
- 🎮 **Low-Quality FastFlags** — Gray sky, no shadows, low textures, no post-FX
- 🚀 **Uncapped FPS** — Targets 1000 FPS with Vulkan renderer
- ↩️ **One-Click Undo** — Instantly remove FastFlags
- 🎨 **Clean Dark UI** — No ads, no bloat, just a button and results
- 📦 **Standalone** — Everything included, no setup required

---

## 📥 Download

**[⬇️ Download Latest Release](https://github.com/CringeScript/cringescript-patch/releases/latest)**

Extract the zip, run `CringescriptPatch.exe`, done.

---

## 🛠️ How To Use

1. **Extract** the zip anywhere on your PC
2. **Right-click** `CringescriptPatch.exe` → **Run as Administrator**
3. Wait through the 5-second disclaimer
4. Click **⚡ Bake Patch**
5. Select `RobloxPlayerBeta.exe` from your Roblox version folder
   - Path: `%LocalAppData%\Roblox\Versions\<newest folder>\`
6. Accept the low-quality build prompt for max FPS
7. **Fully close Roblox** (open Task Manager → end all Roblox processes)
8. Launch Roblox — enjoy the boost

### To Undo

Click **↩ Undo Patch** to remove FastFlags.
For Nvidia settings, remove the Roblox profile manually in Nvidia Control Panel.

---

## 📦 What's In The Zip

| File | What It Does |
|------|--------------|
| `CringescriptPatch.exe` | The main app |
| `nvidiaProfileInspector.exe` | GPU profile importer (by Orbmu2k, MIT) |
| `profile.nip` | The Nvidia profile that gets imported |
| `LICENSE.txt` | MIT license text |
| `README.txt` | Simple user instructions |

---

## ⚠️ Important

- **Roblox auto-updates wipe patches** — you must re-run this after every Roblox update
- **Windows SmartScreen may warn you** — this is normal for unsigned .exe files. Click "More info" → "Run anyway"
- **Fully kill Roblox before testing** — yes, even background processes in Task Manager
- **Use at your own risk** — while this is not a cheat and shouldn't cause bans, I'm not responsible for any issues

---

## 🧠 FastFlags Applied

<details>
<summary>Click to view the full JSON</summary>

```json
{
  "DFIntTaskSchedulerTargetFps": 1000,
  "DFIntTextureQualityOverride": 0,
  "DFFlagTextureQualityOverrideEnabled": true,
  "FFlagDisablePostFx": true,
  "FIntRenderShadowIntensity": 0,
  "DFIntDebugFRMQualityLevelOverride": 1,
  "FFlagDebugSkyGray": true,
  "FIntFRMMinGrassDistance": 0,
  "FIntFRMMaxGrassDistance": 0,
  "FIntRobloxGuiBlurIntensity": 0,
  "FFlagDebugGraphicsPreferVulkan": true
}
```

</details>

---

## 🏗️ Build From Source

```bash
git clone https://github.com/CringeScript/cringescript-patch.git
cd cringescript-patch
pip install pyinstaller
pyinstaller --onefile --noconsole --name "CringescriptPatch" cringescript_patch.py
```

Your `.exe` will be in `dist/`.

---

## 📜 License

MIT License — see [LICENSE](LICENSE).

Bundles [Nvidia Profile Inspector](https://github.com/Orbmu2k/nvidiaProfileInspector) by **Orbmu2k**, also MIT licensed. *(Already included in the zip.)*

---

## 🙌 Credits

- **Orbmu2k** — Nvidia Profile Inspector
- **CringeScript** — Everything else

---

<p align="center">
  Made with ⚡ for the Roblox community • Free forever
</p>
