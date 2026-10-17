"""Frames out of recorded videos with ffmpeg (replay, eval, reference building). JPEG bytes, 512 px wide."""
import subprocess

import numpy as np

SCALE = "scale=512:-2"


def grab(video, t):
    """One JPEG frame at second t."""
    r = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(video),
         "-frames:v", "1", "-vf", SCALE, "-f", "image2pipe", "-vcodec", "mjpeg", "-"],
        capture_output=True,
    )
    if r.returncode or not r.stdout:
        raise ValueError(f"no frame at {t:.1f}s in {video} (past the end?) {r.stderr.decode().strip()[-200:]}")
    return r.stdout


def frames(video, fps, start=0.0, end=None):
    """Yield (t, jpeg) at a fixed rate, like the live camera stream will send."""
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", f"{start:.3f}", "-i", str(video)]
    if end is not None:
        cmd += ["-t", f"{end - start:.3f}"]
    cmd += ["-vf", f"fps={fps},{SCALE}", "-f", "image2pipe", "-vcodec", "mjpeg", "-"]
    data = subprocess.run(cmd, capture_output=True, check=True).stdout
    # ponytail: whole clip in memory and split on JPEG end markers; fine for minute-long runs.
    # 0xFFD9 can't appear inside JPEG entropy data (0xFF is byte-stuffed), so the split is exact.
    for i, chunk in enumerate(data.split(b"\xff\xd9")[:-1]):
        yield start + i / fps, chunk + b"\xff\xd9"


def audio(src, sr=16000):
    """A media file path or raw bytes (any format ffmpeg reads) -> mono float32 samples at sr, for Whisper.
    Empty array if there is no audio."""
    raw = isinstance(src, bytes)
    r = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", "-" if raw else str(src), "-vn", "-ac", "1",
                        "-ar", str(sr), "-f", "f32le", "-"], input=src if raw else None, capture_output=True)
    return np.frombuffer(r.stdout, np.float32) if r.returncode == 0 else np.zeros(0, np.float32)


def duration(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                       capture_output=True, check=True, text=True)
    return float(r.stdout.strip())
