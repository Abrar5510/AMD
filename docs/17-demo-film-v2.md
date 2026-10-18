# 17 — Ghost Expert: demo film v2 (script and shot list)

The investor film, about 90 seconds, made entirely from **real footage and real screen recordings**: no animation standing in for the product. Filming happens in Phase 2 of the [roadmap](../ghost-expert/ROADMAP.md). Writing it now means filming day is one session.

**Voice:** HeyGen AI voice (Meredith, Serious & Composed, as in v1). No music.
**The aha moment:** the authoring step: one video in, a training program out.
**Numbers on screen:** only measured ones. If the filmed eval isn't done yet, the "Numbers" beat shows `[PENDING]` and the film doesn't ship.

## Script

| Time | Picture | Voice |
|---|---|---|
| 0–8 s | **S1** An experienced technician at the real machine, mid-job, hands sure. | "Your best technician retires next year. What she knows about this machine leaves with her." |
| 8–30 s | **S2** She films the job once on a phone and talks through it. Cut to **R1**: the upload, then the steps appearing on the timeline. **R2**: she fixes one step title and clicks Approve. Lower third: "Drafted in [N] s on one AMD GPU". | "So she films it once and talks it through. Ghost Expert turns the video into steps, each with a check the camera can see. She fixes one and approves. The procedure is hers. The AI only drafts it." |
| 30–55 s | **S3** A new hire at the same machine, phone on a mount above the work area. **R3**: steps turn green. Then the new hire reaches for the cover screws without testing the machine is dead: **R4**, the red stop banner, and the expert's clip of that step playing. The new hire does the step, and the coach says "Thank you. That's the safe way." | "A new hire does the same job. The coach confirms each step as it happens. Here, he skips testing that the machine is dead. The coach flags it, and shows her doing it, until he does too." |
| 55–68 s | **R5** The training record: time per step against the expert, the mistake caught. A supervisor types her name and clicks Sign off. Then Download xAPI. | "At the end, his supervisor gets a training record: time per step, mistakes caught. She signs it off, and it goes straight into the plant's training system." |
| 68–80 s | **G1** Two numbers on a plain card: filmed verify accuracy, and skipped steps caught vs. false stops on clean runs. Small caption: "Measured on [N] filmed runs." | "Measured on real runs: [X]% of steps checked correctly. Every skipped step caught, no correct trainee stopped." *(Rewrite to say exactly what the filmed eval shows.)* |
| 80–90 s | **S1** again, the expert, then a title card: Ghost Expert + the "try it yourself" link. | "Every plant has someone about to retire. Film them." |

## Shot list

**On the floor (S = shot):**
- **S1** Expert at the machine: 2 wide shots and 2 close-ups of hands, 10 seconds each. Natural light, no staging.
- **S2** Expert filming herself on a phone: one over-the-shoulder shot that shows the phone screen.
- **S3** New hire: one wide shot of the mount and setup, one top-down shot matching the coach camera, and the reach for the screws, filmed twice.

**Screen recordings (R), 1920×1080, browser zoom 100%, no bookmarks bar:**
- **R1** `/?try` → upload → drafting progress → steps appear. Record it all, and cut down in the edit.
- **R2** Edit one step title, then Approve.
- **R3** The coach screen with steps turning green, from a real run, not the mock.
- **R4** The stop: banner, voice, expert clip. Record it from a real skipped-step run.
- **R5** The training record: type the trainee name, the supervisor signs off, click Download xAPI.

**Graphics (G):**
- **G1** A numbers card in the cover's style (`submission/cover.html` colours and fonts).

## Checklist for filming day

- [ ] The real job and machine are agreed, and the expert and new hire have consented to be filmed.
- [ ] The procedure is approved in the app before the new-hire shots.
- [ ] The phone mount is tested: the coach sees the whole work area.
- [ ] Every R recording uses the GPU box, not the mock server.
- [ ] Lighting is checked on the coach screen (the bench strip shows frames/s and Gemma latency).
