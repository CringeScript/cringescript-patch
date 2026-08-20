"""
Cringescript Patch - Roblox Performance Optimizer
Compatible: Python 3.7 - 3.14 / Windows
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox


FASTFLAGS = {
    "DFIntTaskSchedulerTargetFps": 1000,
    "DFIntTextureQualityOverride": 0,
    "DFFlagTextureQualityOverrideEnabled": "True",
    "FFlagDisablePostFx": "True",
    "FIntRenderShadowIntensity": 0,
    "DFIntDebugFRMQualityLevelOverride": 1,
    "FFlagDebugSkyGray": "True",
    "FIntFRMMinGrassDistance": 0,
    "FIntFRMMaxGrassDistance": 0,
    "FIntRobloxGuiBlurIntensity": 0,
    "FFlagDebugGraphicsPreferVulkan": "True",
}


BG_PRIMARY     = "#0D0D0D"
BG_SECONDARY   = "#161616"
BG_CARD        = "#1A1A1A"
BG_HOVER       = "#242424"
ACCENT         = "#6C63FF"
ACCENT_HOVER   = "#5A52E0"
TEXT_PRIMARY   = "#F0F0F0"
TEXT_SECONDARY = "#888888"
TEXT_MUTED     = "#555555"
DANGER         = "#FF4757"
DANGER_HOVER   = "#E03A4A"
SUCCESS        = "#2ED573"
WARNING        = "#FFA502"
BORDER         = "#2A2A2A"
FONT           = "Segoe UI"
FONT_MONO      = "Consolas"



def resource_path(relative):
    """
    Resolves a file path relative to the .exe (when built with PyInstaller)
    or relative to the .py script when run directly.
    nvidiaProfileInspector.exe and profile.nip must sit NEXT TO the .exe/.py.
    """
    if hasattr(sys, "_MEIPASS"):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative)


def get_roblox_versions_path():
    local = os.environ.get("LOCALAPPDATA", "")
    path = os.path.join(local, "Roblox", "Versions")
    return path if os.path.isdir(path) else os.path.expanduser("~")


def validate_folder(folder):
    return os.path.isfile(os.path.join(folder, "RobloxPlayerBeta.exe"))


def find_inspector():
    """Look for nvidiaProfileInspector.exe (or old nvidiaInspector.exe) next to the app."""
    candidate = resource_path("nvidiaProfileInspector.exe")
    if os.path.isfile(candidate):
        return candidate
    candidate = resource_path("nvidiaInspector.exe")
    if os.path.isfile(candidate):
        return candidate
    found = shutil.which("nvidiaProfileInspector.exe")
    if found:
        return found
    found = shutil.which("nvidiaInspector.exe")
    return found


def get_nip_path():
    """Returns the expected path of profile.nip next to the app."""
    return resource_path("profile.nip")



def apply_nvidia_profile(exe_path):
    """
    Reads profile.nip from the app folder and imports it via
    nvidiaProfileInspector.exe.
    Returns (success: bool, message: str).
    """

    inspector = find_inspector()
    if not inspector:
        msg = (
            "nvidiaProfileInspector.exe was NOT found next to CringescriptPatch.exe.\n\n"
            "To apply the Nvidia profile:\n"
            "1. Download Nvidia Profile Inspector from:\n"
            "   github.com/Orbmu2k/nvidiaProfileInspector/releases\n"
            "2. Place  nvidiaProfileInspector.exe  in the same folder as\n"
            "   CringescriptPatch.exe\n"
            "3. Run Cringescript Patch again.\n\n"
            "The FastFlags patch still works without it."
        )
        return False, msg

    nip_path = get_nip_path()
    if not os.path.isfile(nip_path):
        msg = (
            "profile.nip was NOT found next to CringescriptPatch.exe.\n\n"
            "Make sure  profile.nip  is in the same folder as\n"
            "CringescriptPatch.exe and try again.\n\n"
            "The FastFlags patch still works without it."
        )
        return False, msg

    try:
        try:
            with open(nip_path, "r", encoding="utf-16") as f:
                nip_content = f.read()
        except UnicodeError:
            with open(nip_path, "r", encoding="utf-8") as f:
                nip_content = f.read()
    except Exception as exc:
        return False, "Could not read profile.nip:\n" + str(exc)

    tmp_path = ""
    try:
        fd, tmp_path = tempfile.mkstemp(suffix=".nip")
        with os.fdopen(fd, "w", encoding="utf-16") as f:
            f.write(nip_content)

        result = subprocess.run(
            [inspector, "-import", tmp_path],
            capture_output=True,
            timeout=30,
        )

        if result.returncode == 0:
            return True, "Nvidia profile applied successfully."
        else:
            stderr = (result.stderr or b"").decode(errors="replace").strip()
            stdout = (result.stdout or b"").decode(errors="replace").strip()
            detail = stderr or stdout or "No output from Inspector."
            return False, "Nvidia Inspector returned an error:\n" + detail

    except subprocess.TimeoutExpired:
        return False, "Nvidia Inspector timed out after 30 seconds."
    except Exception as exc:
        return False, "Failed to run Nvidia Inspector:\n" + str(exc)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def apply_fastflags(version_folder):
    """
    Creates ClientSettings/ClientAppSettings.json with performance flags.
    Returns (success: bool, message: str).
    """
    cs_dir = os.path.join(version_folder, "ClientSettings")
    json_path = os.path.join(cs_dir, "ClientAppSettings.json")
    try:
        os.makedirs(cs_dir, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(FASTFLAGS, f, indent=2)
        return True, json_path
    except PermissionError:
        return False, (
            "Permission denied writing to:\n" + cs_dir +
            "\n\nTry running CringescriptPatch.exe as Administrator."
        )
    except Exception as exc:
        return False, "Could not write FastFlags:\n" + str(exc)


def remove_client_settings(version_folder):
    """
    Deletes the ClientSettings folder from the version directory.
    Returns (success: bool, message: str).
    """
    cs_dir = os.path.join(version_folder, "ClientSettings")
    if not os.path.exists(cs_dir):
        return False, (
            "ClientSettings folder not found in:\n" + version_folder +
            "\n\nNothing to remove."
        )
    try:
        shutil.rmtree(cs_dir)
        return True, "ClientSettings folder deleted successfully."
    except PermissionError:
        return False, (
            "Permission denied deleting:\n" + cs_dir +
            "\n\nTry running as Administrator."
        )
    except Exception as exc:
        return False, "Could not delete folder:\n" + str(exc)



class RoundedButton(tk.Frame):
    """
    Simple flat button using Frame + Label.
    100% Python 3.14 compatible.
    """

    def __init__(
        self,
        parent,
        text,
        command=None,
        w=210,
        h=50,
        fill_color=ACCENT,
        hover_fill=ACCENT_HOVER,
        fg_color=TEXT_PRIMARY,
        font_size=11,
        **_ignored,
    ):
        tk.Frame.__init__(
            self,
            parent,
            width=w,
            height=h,
            bg=fill_color,
            highlightthickness=0,
            borderwidth=0,
        )
        self.pack_propagate(False)

        self._cmd = command
        self._fill = fill_color
        self._hover = hover_fill

        self._label = tk.Label(
            self,
            text=text,
            bg=fill_color,
            fg=fg_color,
            font=(FONT, font_size, "bold"),
            cursor="hand2",
        )
        self._label.pack(expand=True, fill="both")

        for widget in (self, self._label):
            widget.bind("<Enter>", self._enter)
            widget.bind("<Leave>", self._leave)
            widget.bind("<Button-1>", self._click)

    def _enter(self, _e):
        self.config(bg=self._hover)
        self._label.config(bg=self._hover)

    def _leave(self, _e):
        self.config(bg=self._fill)
        self._label.config(bg=self._fill)

    def _click(self, _e):
        if self._cmd:
            self._cmd()


class StatusBar(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg=BG_SECONDARY, height=26)
        self.pack_propagate(False)
        self._lbl = tk.Label(
            self,
            text="Ready",
            bg=BG_SECONDARY,
            fg=TEXT_MUTED,
            font=(FONT, 8),
            anchor="w",
            padx=14,
        )
        self._lbl.pack(fill="x", expand=True)

    def set(self, text, color=TEXT_MUTED):
        self._lbl.config(text=text, fg=color)
        self._lbl.update_idletasks()



class DisclaimerScreen:
    """
    Splash window shown before the main app.
    5 second countdown, then auto launches main.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cringescript Patch")
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(False, False)
        self.root.overrideredirect(True)

        WIN_W, WIN_H = 520, 340
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WIN_W)
        y = (sh - WIN_H)
        self.root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

        self._seconds_left = 5
        self._build()
        self._tick()

    def _build(self):
        root = self.root

        tk.Frame(root, bg=DANGER, height=3).pack(fill="x")

        body = tk.Frame(root, bg=BG_PRIMARY, padx=40, pady=30)
        body.pack(fill="both", expand=True)

        title_row = tk.Frame(body, bg=BG_PRIMARY)
        title_row.pack(fill="x", pady=(0, 6))

        tk.Label(
            title_row,
            text="⚠",
            bg=BG_PRIMARY,
            fg=DANGER,
            font=(FONT, 22, "bold"),
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            title_row,
            text="Disclaimer",
            bg=BG_PRIMARY,
            fg=TEXT_PRIMARY,
            font=(FONT, 20, "bold"),
        ).pack(side="left")

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=(8, 18))

        disclaimer_text = (
            "Cringescript Patch is provided as-is for educational\n"
            "and personal use only.\n\n"
            "The developers are NOT responsible for any damages,\n"
            "bans, data loss, or system issues that may arise\n"
            "from using this software.\n\n"
            "Use of this tool is entirely at your own risk.\n"
            "By continuing you agree to these terms."
        )

        tk.Label(
            body,
            text=disclaimer_text,
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY,
            font=(FONT, 10),
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(0, 20))

        self._countdown_var = tk.StringVar(value="Continuing in 5 seconds...")
        self._countdown_lbl = tk.Label(
            body,
            textvariable=self._countdown_var,
            bg=BG_PRIMARY,
            fg=TEXT_MUTED,
            font=(FONT, 8, "italic"),
            anchor="w",
        )
        self._countdown_lbl.pack(fill="x")

        progress_bg = tk.Frame(body, bg=BORDER, height=3)
        progress_bg.pack(fill="x", pady=(6, 0))

        self._progress_bar = tk.Frame(progress_bg, bg=DANGER, height=3)
        self._progress_bar.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        tk.Frame(root, bg=BG_SECONDARY, height=1).pack(fill="x", side="bottom")

    def _tick(self):
        if self._seconds_left <= 0:
            self._launch_main()
            return

        self._countdown_var.set(
            f"Continuing in {self._seconds_left} second{'s' if self._seconds_left != 1 else ''}..."
        )

        progress = self._seconds_left / 5.0
        self._progress_bar.place(relwidth=progress)

        if self._seconds_left <= 2:
            self._countdown_lbl.config(fg=WARNING)

        self._seconds_left -= 1
        self.root.after(1000, self._tick)

    def _launch_main(self):
        self.root.destroy()
        main_app = App()
        main_app.run()

    def run(self):
        self.root.mainloop()



class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cringescript Patch")
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(False, False)

        WIN_W, WIN_H = 490, 640
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - WIN_W)
        y = (sh - WIN_H)
        self.root.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

        icon_path = resource_path("icon.ico")
        if os.path.isfile(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        self._cached_folder = None
        self._build()


    def _build(self):
        root = self.root

        tk.Frame(root, bg=ACCENT, height=3).pack(fill="x")

        body = tk.Frame(root, bg=BG_PRIMARY, padx=36, pady=28)
        body.pack(fill="both", expand=True)

        title_row = tk.Frame(body, bg=BG_PRIMARY)
        title_row.pack(fill="x")

        tk.Label(
            title_row,
            text="Cringescript",
            bg=BG_PRIMARY,
            fg=ACCENT,
            font=(FONT, 28, "bold"),
            anchor="w",
        ).pack(anchor="w")

        tk.Label(
            title_row,
            text="Patch",
            bg=BG_PRIMARY,
            fg=TEXT_PRIMARY,
            font=(FONT, 28),
            anchor="w",
        ).pack(anchor="w")

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=(14, 16))

        tk.Label(
            body,
            text=(
                "Boost Roblox FPS with Nvidia profile tweaks\n"
                "and FastFlag injection — one click."
            ),
            bg=BG_PRIMARY,
            fg=TEXT_SECONDARY,
            font=(FONT, 10),
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(0, 20))

        self._build_file_check_card(body)

        tk.Frame(body, bg=BG_PRIMARY, height=18).pack()

        btn_row = tk.Frame(body, bg=BG_PRIMARY)
        btn_row.pack(fill="x", pady=(6, 0))

        RoundedButton(
            btn_row,
            text="⚡   Bake Patch",
            command=self._bake,
            w=200,
            h=52,
            fill_color=ACCENT,
            hover_fill=ACCENT_HOVER,
            font_size=12,
        ).pack(side="left", padx=(0, 14))

        RoundedButton(
            btn_row,
            text="↩   Undo Patch",
            command=self._undo,
            w=200,
            h=52,
            fill_color=BG_CARD,
            hover_fill=BG_HOVER,
            fg_color=DANGER,
            font_size=12,
        ).pack(side="left")

        tk.Frame(body, bg=BG_PRIMARY).pack(fill="both", expand=True)

        tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=(0, 10))
        tk.Label(
            body,
            text="v1.2  •  Use at your own risk",
            bg=BG_PRIMARY,
            fg=TEXT_MUTED,
            font=(FONT, 8),
            anchor="w",
        ).pack(fill="x")

        self._status = StatusBar(root)
        self._status.pack(fill="x", side="bottom")

    def _build_file_check_card(self, parent):
        card = tk.Frame(parent, bg=BG_CARD, padx=16, pady=14)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Required Files",
            bg=BG_CARD,
            fg=TEXT_PRIMARY,
            font=(FONT, 9, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 8))

        self._build_file_row(
            card,
            label="nvidiaProfileInspector.exe",
            present=find_inspector() is not None,
        )
        self._build_file_row(
            card,
            label="profile.nip",
            present=os.path.isfile(get_nip_path()),
        )

        tk.Label(
            card,
            text="Missing files?  See README.txt for instructions.",
            bg=BG_CARD,
            fg=TEXT_MUTED,
            font=(FONT, 8, "italic"),
            anchor="w",
        ).pack(fill="x", pady=(8, 0))

    def _build_file_row(self, parent, label, present):
        row = tk.Frame(parent, bg=BG_CARD)
        row.pack(fill="x", pady=2)

        dot_color = SUCCESS if present else DANGER
        dot_text  = "●  " + ("Found" if present else "Not found")

        tk.Label(
            row,
            text=dot_text,
            bg=BG_CARD,
            fg=dot_color,
            font=(FONT_MONO, 8),
            width=14,
            anchor="w",
        ).pack(side="left")

        tk.Label(
            row,
            text=label,
            bg=BG_CARD,
            fg=TEXT_SECONDARY,
            font=(FONT_MONO, 8),
            anchor="w",
        ).pack(side="left", padx=(6, 0))


    def _pick_folder(self, show_instructions=True):
        if show_instructions:
            messagebox.showinfo(
                "Select Roblox Executable",
                "Navigate to your Roblox version folder inside:\n\n"
                "  %LocalAppData%\\Roblox\\Versions\\\n\n"
                "Open the latest version folder and select\n"
                "'RobloxPlayerBeta.exe' inside it.",
            )

        initial = get_roblox_versions_path()

        while True:
            chosen = filedialog.askopenfilename(
                title="Select RobloxPlayerBeta.exe",
                initialdir=initial,
                filetypes=[
                    ("Roblox Executable", "RobloxPlayerBeta.exe"),
                    ("All Files", "*.*"),
                ],
            )

            if not chosen:
                return None

            folder = os.path.dirname(chosen)
            fname  = os.path.basename(chosen)

            if fname == "RobloxPlayerBeta.exe" and validate_folder(folder):
                self._cached_folder = folder
                return folder

            retry = messagebox.askretrycancel(
                "Wrong File",
                "That doesn't look right.\n\n"
                "Please select  RobloxPlayerBeta.exe  from inside the\n"
                "Roblox version folder (not a shortcut or other file).",
            )
            if not retry:
                return None


    def _bake(self):
        self._status.set("Waiting for folder selection…", ACCENT)

        folder = self._pick_folder()
        if not folder:
            self._status.set("Cancelled.", TEXT_MUTED)
            return

        exe = os.path.join(folder, "RobloxPlayerBeta.exe")

        self._status.set("Applying Nvidia profile…", ACCENT)
        self.root.update()

        nv_ok, nv_msg = apply_nvidia_profile(exe)

        if nv_ok:
            self._status.set("Nvidia profile applied ✓", SUCCESS)
        else:
            self._status.set("Nvidia profile skipped — see warning.", TEXT_SECONDARY)
            messagebox.showwarning("Nvidia Profile — Action Required", nv_msg)

        want_ff = messagebox.askyesno(
            "Low Quality Build",
            "FPS patch has been baked into Roblox!\n\n"
            "Do you also want the low quality build\n"
            "for even more FPS?\n\n"
            "This writes FastFlags that give you:\n"
            "  • Uncapped FPS (target 1000)\n"
            "  • Lowest possible textures & shadows\n"
            "  • Gray sky, no post-FX, no blur\n"
            "  • Vulkan renderer\n\n"
            "Accept = Yes     Skip = No thanks",
        )

        if not want_ff:
            self._status.set("Done — Nvidia only. Restart Roblox!", SUCCESS)
            messagebox.showinfo(
                "Done!",
                "Nvidia profile applied.\n"
                "Restart Roblox for changes to take effect!",
            )
            return

        self._status.set("Writing FastFlags…", ACCENT)
        self.root.update()

        ff_ok, ff_detail = apply_fastflags(folder)

        if ff_ok:
            self._status.set("All patches applied ✓  — restart Roblox!", SUCCESS)
            messagebox.showinfo(
                "Completed!",
                "Completed! Restart Roblox for changes to take effect!",
            )
        else:
            self._status.set("FastFlags write failed.", DANGER)
            messagebox.showerror("FastFlags Error", ff_detail)


    def _undo(self):
        proceed = messagebox.askyesno(
            "Undo Patch",
            "We can't remove Nvidia settings automatically — doing so\n"
            "without knowing your existing setup risks breaking things.\n\n"
            "You'll need to remove the Roblox profile manually inside\n"
            "Nvidia Control Panel  →  Manage 3D Settings.\n\n"
            "What we CAN do automatically:\n"
            "Delete the ClientSettings folder\n"
            "(gray sky, low textures, no shadows, etc.)\n\n"
            "Do you want to delete ClientSettings now?",
        )
        if not proceed:
            return

        folder = self._cached_folder
        if folder and validate_folder(folder):
            reuse = messagebox.askyesno(
                "Use Previous Location?",
                f"Use the previously selected folder?\n\n{folder}",
            )
            if not reuse:
                folder = None

        if not folder or not validate_folder(folder):
            self._status.set("Waiting for folder selection…", ACCENT)
            folder = self._pick_folder(show_instructions=False)
            if not folder:
                self._status.set("Undo cancelled.", TEXT_MUTED)
                return

        self._status.set("Removing ClientSettings…", ACCENT)
        self.root.update()

        ok, msg = remove_client_settings(folder)

        if ok:
            self._status.set("ClientSettings removed ✓", SUCCESS)
            messagebox.showinfo("Undo Complete", msg)
        else:
            self._status.set("Removal failed.", DANGER)
            messagebox.showerror("Undo Error", msg)


    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    splash = DisclaimerScreen()
    splash.run()