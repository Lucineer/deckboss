# Deckboss

> Build phase. Design your robot's brain, then hand it off to Cocapn for service.

**Deckboss.ai** — the chatbot for developing robotic systems. A technician starts here: describe what you need, riff with the AI, develop the git-agent fleet that becomes the robot's intelligence. Once development is done and the robot goes into service, Deckboss powers down to cold storage and **Cocapn** takes over.

## The Lifecycle

```
Build Phase                    Service Phase
───────────                    ─────────────
Deckboss.ai (cloud/localhost) ──hand off──► Cocapn (on device)
  • Design systems                               • Run autonomously
  • Develop git-agent fleets                     • Monitor & alert
  • Vibe-code physical solutions                 • Learn from operation
  • Test & validate                              • Maintenance logging
  • Generate installation manuals                • Self-improve via PRs
                                                        │
                                              Cocapn.ai ◄─┘
                                              (web interface)
                                                        │
                                              Cocapn.com ◄─┘
                                              (membership/billing)
```

## Try Free → Buy Hardware

1. **Start at Deckboss.ai** — connected to cloud services, no hardware needed
2. **Build your brain** — develop git-agent fleet for your specific use case
3. **Buy a Deckboss unit** — [Deckboss.net](https://deckboss.net) — preloaded, plug and play
4. **Hand off to Cocapn** — your fleet deploys to the hardware
5. **Robot goes into service** — Cocapn runs it, monitors it, learns
6. **Capitaine.ai** — premium tier: mobile, dojos, bootcamps, white-glove

## The Moat

People use the software for free. They build something that works. Then the next job comes and they don't have time to fork/clone/curate what works best on a 2-Jetson array or a 4-Raspberry Pi setup. They buy the hardware because it just works. Job after job.

## Hardware Options

| Unit | Specs | Use Case |
|------|-------|----------|
| Deckboss Nano | Raspberry Pi 5 8GB | Simple monitoring, single sensor |
| Deckboss Standard | Jetson Super Orin Nano 8GB | Multi-sensor, vision, STT/TTS |
| Deckboss Pro | 2× Jetson Orin Nano | Complex robotics, parallel inference |
| Deckboss Enterprise | 4× Raspberry Pi 5 array | Distributed sensor networks |

All units ship preloaded with:
- Deckboss (build phase, cold storage until needed)
- Cocapn runtime (service phase, ready to activate)
- Capitaine (cold, premium features unlockable)
- Local models: Whisper, Piper, Phi-3-mini
- Base git-agent fleet templates

## For Content Creators

Deckboss isn't just for robots. A content creator uses Deckboss.ai to build a Cocapn that manages their content pipeline:
- Drop content into folders in a private repo
- Folder structure = role definition (posts, stories, replies, analytics)
- Each folder has priority and schedule
- Cocapn develops its own posting strategy via PRs
- The Cocapn IS the social media manager

## For Engineers

An engineer uses Deckboss.ai to build a Cocapn for AR-assisted work:
- Glasses with cameras feed vision models
- Real-time suggestions displayed on screen
- Cocapn develops display pipelines and summaries
- Feedback loop: engineer corrects, Cocapn adapts
- The app evolves through PRs based on usage

## Architecture

```
Deckboss.ai (Cloudflare Worker)
├── Chat interface (Telegram/Discord/Web)
├── Git-agent fleet builder
├── Vibe-coding engine (text + vision)
├── Hardware profile generator
├── Installation manual builder
├── BYOK cloud services (free tier)
└── Handoff tool → exports fleet to Cocapn format
```

## Tech Stack

- Cloudflare Workers (free tier viable)
- DeepSeek / z.ai / DeepInfra (BYOK)
- Git-native (every design decision is a commit)
- Fork-first (templates for common patterns)
- Zero dependencies for core

## Open Source

Everything is open source. Buy the hardware for convenience. Fork and build your own if you want. The moat isn't lock-in — it's trust, accumulated knowledge, and time.

---

## Brand Family

| Domain | Role |
|--------|------|
| **Deckboss.ai** | Build-phase chatbot (this repo) |
| **Deckboss.net** | Physical hardware store |
| **Cocapn.ai** | Runtime agent web interface |
| **Cocapn.com** | Company, membership, billing |
| **Capitaine.ai** | Premium platform, education, mobile |

---

<i>Built by [Superinstance](https://github.com/superinstance) & [Lucineer](https://github.com/Lucineer) (DiGennaro et al.)</i>
