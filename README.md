#  Manim-Based YouTube Videos

A collection of Python scripts used to create mathematical and AI-concept animations for YouTube, powered by **[Manim Community Edition](https://www.manim.community/)**.

##  Scripts Overview

| File | Topic |
|------|-------|
| `1_Fine_Tuning.py` | Fine-tuning large language models |
| `2_Semantic_Search.py` | Semantic search explained visually |
| `2_VectorEmbedding1.py` | Introduction to vector embeddings |
| `2_Vector_Embedding2.py` | Vector embeddings — deeper dive |
| `2_Vector_Placeholder.py` | Vector placeholder animations |
| `3_How_Chatgpt_Works_1.py` | How ChatGPT works — Part 1 |
| `3_How_Chatgpt_Works_2.py` | How ChatGPT works — Part 2 |
| `4_RAG_Updated_Version.py` | RAG pipeline — updated version |
| `4_RAG_pipeline.py` | Retrieval-Augmented Generation (RAG) pipeline |
| `5_Understanding_The_Vector_Databases.py` | Understanding vector databases |

---

##  Prerequisites

Before running any of the scripts, you need to install the following tools:

1. **Python 3.8+**
2. **Manim Community Edition**
3. **MiKTeX (LaTeX)**
4. **FFmpeg**

---

##  1. Installing Manim

Manim is a Python library for creating mathematical animations. We use the **Community Edition**.

### Step 1 — Install Python

Download and install Python 3.8 or later from [python.org](https://www.python.org/downloads/).

>  During installation, check **"Add Python to PATH"**.

### Step 2 — Install Manim via pip

```bash
pip install manim
```

To verify the installation:

```bash
manim --version
```

### Step 3 — Render a Scene

To render any of the scripts in this repo, use the following command:

```bash
manim -pql <script_name>.py <SceneClassName>
```

**Flags:**
- `-p` — Preview the rendered video automatically
- `-q l` — Low quality (faster preview); replace with `m` (medium) or `h` (high) for production

**Example:**

```bash
manim -pql 1_Fine_Tuning.py FineTuningScene
```

---

##  2. Installing LaTeX (MiKTeX on Windows)

Manim uses **LaTeX** to render mathematical equations and text. Without it, any scene using `MathTex`, `Tex`, or `$$...$$` will fail.

### Why MiKTeX?

**MiKTeX** is the recommended LaTeX distribution for Windows. It is lightweight and installs missing packages automatically on demand — perfect for Manim workflows.

### Step 1 — Download MiKTeX

Go to [miktex.org/download](https://miktex.org/download) and download the **Windows installer**.

### Step 2 — Install MiKTeX

Run the installer and follow the setup wizard. Key settings during installation:

- **Install for:** "Just for me" (or "All users" if on a shared machine)
- **Preferred paper:** Letter or A4
- **Install missing packages on-the-fly:** Select **"Yes"** 

>  The "install on-the-fly" setting lets MiKTeX automatically download any LaTeX package that Manim needs the first time it's used, so you don't have to manage packages manually.

### Step 3 — Update MiKTeX

After installation, open **MiKTeX Console** (search for it in Start Menu) and click **"Check for updates"** → then **"Update now"**.

### Step 4 — Verify Installation

Open a new terminal and run:

```bash
pdflatex --version
```

You should see version information confirming the install.

>  After installing MiKTeX, **restart your terminal** (or even your machine) so that the `PATH` is picked up correctly.

---

##  3. Why FFmpeg is Necessary

**FFmpeg** is a free, open-source multimedia framework used to encode and export video and audio. Manim depends on FFmpeg to:

- **Compile animation frames** into a video file (`.mp4`)
- **Handle audio** if you add voiceover or sound effects
- **Control video quality and codecs** (e.g., H.264 for YouTube-compatible output)

Without FFmpeg, Manim can render individual frames but **cannot produce a video file**.

### Installing FFmpeg on Windows

#### Option A — Using the bundled version (recommended for this repo)

This repository includes a local copy of FFmpeg (`ffmpeg-8.0.1/`) in the `Scripts` folder. To use it, add the `bin` folder inside it to your system `PATH`:

1. Open **System Properties** → **Advanced** → **Environment Variables**
2. Under **System Variables**, find `Path` and click **Edit**
3. Click **New** and add the full path, e.g.:
   ```
   D:\0_Github_Repos\manim\Scripts\ffmpeg-8.0.1\bin
   ```
4. Click **OK** and close all dialogs
5. Open a new terminal and verify:
   ```bash
   ffmpeg -version
   ```

#### Option B — Install via winget (Windows 10/11)

```bash
winget install Gyan.FFmpeg
```

#### Option C — Manual Download

1. Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Download the latest **Windows build** (e.g., from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/))
3. Extract the archive and add the `bin/` folder to your system `PATH` as shown in Option A

---

##  Quick Start Checklist

- [ ] Python 3.8+ installed and in PATH
- [ ] `pip install manim` completed successfully
- [ ] MiKTeX installed with "install missing packages on-the-fly" enabled
- [ ] FFmpeg installed and accessible via `ffmpeg -version`
- [ ] Clone this repo and `cd` into `Scripts/`
- [ ] Run a test render: `manim -pql 1_Fine_Tuning.py FineTuningScene`

---

##  Resources

- [Manim Community Docs](https://docs.manim.community/)
- [MiKTeX Download](https://miktex.org/download)
- [FFmpeg Official Site](https://ffmpeg.org/)
- [Manim Installation Guide (Official)](https://docs.manim.community/en/stable/installation.html)

---

##  License

This project is open-source. Feel free to use and adapt these scripts for your own educational content.
