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
