# Landing-page background video

Put a short, looping, royalty-free clip here named **`airport.mp4`** (aerial airport
or terminal renovation footage works well). The Streamlit landing page
(`app.py` → `render_landing`) plays it full-screen behind the hero text.

- Keep it small (a few MB) and muted-friendly — it autoplays muted and loops.
- Good free sources: Pexels, Coverr, Mixkit (check each clip's license).
- If `airport.mp4` is absent, the landing page falls back to a premium dark gradient
  hero, so the app still looks good with no video.
