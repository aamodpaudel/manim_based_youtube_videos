#  Rendering Tips for Manim Scripts

A quick reference for getting the best output from these animation scripts.

## Quality Flags

| Flag | Quality | Resolution | Use Case |
|------|---------|------------|----------|
| `-ql` | Low | 480p | Quick preview |
| `-qm` | Medium | 720p | Draft review |
| `-qh` | High | 1080p | YouTube upload |
| `-qk` | 4K | 2160p | High-res export |

## Recommended Render Commands

```bash
# Quick preview (fastest)
manim -pql script.py SceneName

# Final YouTube export (1080p)
manim -qh script.py SceneName

# Render without opening preview (for batch)
manim -qh --disable_caching script.py SceneName
```

## Saving Output

By default, Manim saves output to:
```
media/videos/<script_name>/<quality>/
```

## Tips

- Use `-n 5,20` to render only frames 5–20 for faster debugging
- Add `--save_sections` if your scene uses `self.next_section()`
- Use `config.background_color = WHITE` in code for light-themed videos
