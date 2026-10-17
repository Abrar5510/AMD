"""Prompts and JSON schemas. Constant text goes first so vLLM's prefix cache reuses it across calls."""

VERIFY_SYSTEM = """You check one step of an industrial procedure, seen from a top-down camera.
Report only what is visible. If the parts that matter for the step are not visible, set confidence below 0.4.
started = the trainee is doing this step or has begun it. done = the step's check is met in the newest image.

The full procedure, for context:
{procedure}"""

# "observed" comes first so the model describes the scene before it commits to a verdict.
# ponytail: no min/max/maxLength keywords, not every vLLM guided-decoding backend supports them; clamp in code.
VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "observed": {"type": "string"},
        "started": {"type": "boolean"},
        "done": {"type": "boolean"},
        "confidence": {"type": "number"},
    },
    "required": ["observed", "started", "done", "confidence"],
}


def procedure_text(procedure):
    return "\n".join(f"{s['id']}. {s['title']}: done when {s['visual_check']}" for s in procedure["steps"])


def verify_messages(procedure, step, frame_urls, keyframe_url=None):
    """Messages for one verify call: system (constant per procedure), then the step, then images."""
    if keyframe_url:
        intro = f"Image 1 is the expert doing this step. Images 2-{len(frame_urls) + 1} are the trainee, oldest to newest."
        urls = [keyframe_url, *frame_urls]
    else:
        intro = "The images are the trainee, oldest to newest."
        urls = list(frame_urls)
    text = f"Step {step['id']}: {step['title']}. It is done when: {step['visual_check']}.\n{intro}"
    return [
        {"role": "system", "content": VERIFY_SYSTEM.format(procedure=procedure_text(procedure))},
        {"role": "user", "content": [{"type": "text", "text": text}]
         + [{"type": "image_url", "image_url": {"url": u}} for u in urls]},
    ]


AUTHOR_SYSTEM = """You turn an expert's recorded demonstration into a step-by-step procedure for training new technicians.
You get the expert's narration split into numbered segments with times, and contact sheets with one frame per
segment (the yellow number on each frame is its segment number).

Group consecutive segments into steps. One step = one action a trainee must do and a camera can check.
Use the expert's own words where you can. Skip nothing the expert does.
- title: a few words, imperative ("Hang the tag").
- instruction: one or two sentences telling a trainee what to do.
- visual_check: what a top-down camera sees when the step is done. Concrete: objects, colors, positions.
- safety_critical: true if skipping the step or doing it out of order can hurt someone or damage equipment.
- common_mistake: the likely mistake for this step, or an empty string."""

AUTHOR_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "first_segment": {"type": "integer"},
                    "last_segment": {"type": "integer"},
                    "title": {"type": "string"},
                    "instruction": {"type": "string"},
                    "visual_check": {"type": "string"},
                    "safety_critical": {"type": "boolean"},
                    "common_mistake": {"type": "string"},
                },
                "required": ["first_segment", "last_segment", "title", "instruction", "visual_check",
                             "safety_critical", "common_mistake"],
            },
        },
    },
    "required": ["title", "steps"],
}


def author_messages(segments, texts, sheet_urls):
    """segments: [(start_s, end_s)], texts: narration per segment, sheet_urls: contact sheet data URLs."""
    lines = [f'{i}. [{a:.1f}-{b:.1f}s] "{t or "(no narration)"}"' for i, ((a, b), t) in enumerate(zip(segments, texts), 1)]
    return [
        {"role": "system", "content": AUTHOR_SYSTEM},
        {"role": "user", "content": [{"type": "text", "text": "Segments:\n" + "\n".join(lines)}]
         + [{"type": "image_url", "image_url": {"url": u}} for u in sheet_urls]},
    ]
