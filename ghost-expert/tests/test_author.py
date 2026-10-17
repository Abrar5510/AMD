"""Authoring logic with no models: segmentation and Gemma-output repair. Run: python -m tests.test_author"""
import numpy as np

from app.author import boundaries, change_points, check_steps, to_steps, transcript_cues


def test_change_points_find_scene_cuts():
    # 3 scenes of 10 s at 2 fps, each a distinct direction plus noise.
    rng = np.random.default_rng(0)
    times = np.arange(60) / 2
    embs = np.repeat(np.eye(8)[:3], 20, axis=0) + rng.normal(0, 0.05, (60, 8))
    cps = change_points(embs, times)
    assert len(cps) == 2 and abs(cps[0] - 10) <= 0.5 and abs(cps[1] - 20) <= 0.5, cps


def test_transcript_cues_words_and_pauses():
    segs = [{"start": 0, "end": 3, "text": "First, switch it off."},
            {"start": 3.2, "end": 5, "text": "it should go dark"},
            {"start": 8, "end": 10, "text": "and the lock goes on"},       # pause of 3 s
            {"start": 10.1, "end": 12, "text": "Poi appendo il cartellino"}]  # Italian cue word
    assert transcript_cues(segs) == [0, 8, 10.1]


def test_boundaries_merge_close_cuts_and_cover_video():
    segs = boundaries([4.0, 4.5, 9.0, 29.5], 30.0)
    assert segs == [(0.0, 4.0), (4.0, 9.0), (9.0, 30.0)], segs  # 4.5 too close, 29.5 too near the end


def test_to_steps_repairs_gaps_overlaps_and_early_stop():
    segments = [(0, 2), (2, 5), (5, 9), (9, 12), (12, 15)]
    base = {"instruction": "", "visual_check": "v", "safety_critical": False, "common_mistake": ""}
    raw = [{**base, "title": "B", "first_segment": 3, "last_segment": 3},   # out of order
           {**base, "title": "A", "first_segment": 1, "last_segment": 1},   # gap: segment 2 belongs to nobody
           {**base, "title": "C", "first_segment": 3, "last_segment": 4}]   # overlaps B; segment 5 missing
    steps = to_steps(raw, segments)
    assert [s["title"] for s in steps] == ["A", "B", "C"]
    assert [s["segments"] for s in steps] == [[1, 1], [2, 3], [4, 5]]
    assert [s["expert_clip"] for s in steps] == [[0, 2], [2, 9], [9, 15]]
    assert [s["must_come_after"] for s in steps] == [[], [1], [2]]


def test_check_steps_rejects_bad_edits():
    good = {"title": "t", "visual_check": "v", "expert_clip": [0, 5]}
    check_steps([good], 10)
    for bad in ({**good, "title": " "}, {**good, "expert_clip": [5, 5]}, {**good, "expert_clip": [0, 99]},
                {**good, "expert_clip": ["0", 5]}, {**good, "expert_clip": None}):
        try:
            check_steps([bad], 10)
        except ValueError:
            continue
        raise AssertionError(f"accepted {bad}")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
