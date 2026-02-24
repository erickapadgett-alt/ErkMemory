# 🧠 ErkMemory

Long-term memory and learning system for Ericka's AI assistant.

## Purpose

This repository serves as persistent memory across sessions. The AI assistant reads from and writes to these files to:
- Remember preferences, decisions, and context
- Learn communication style and expectations
- Track projects, patterns, and lessons learned
- Improve over time based on feedback

## Structure

```
ErkMemory/
├── core/
│   ├── identity.md      # Who Ericka is, how to address her
│   ├── preferences.md   # Communication style, pet peeves, likes
│   ├── expectations.md  # Standards, quality expectations, work style
│   └── lessons.md       # Things learned from mistakes/feedback
├── knowledge/
│   ├── projects.md      # Active and past projects
│   ├── contacts.md      # People, relationships, context
│   ├── systems.md       # Infrastructure, accounts, tools
│   └── decisions.md     # Key decisions and their reasoning
├── patterns/
│   ├── requests.md      # Common request patterns
│   ├── workflows.md     # How Ericka likes things done
│   └── language.md      # Speech patterns, terminology
├── logs/
│   └── YYYY-MM-DD.md    # Daily interaction summaries
└── meta/
    └── improvements.md  # Self-improvement tracking
```

## Usage

The assistant automatically:
1. Reads relevant memory files at session start
2. Updates files when learning new information
3. Logs significant interactions daily
4. Reviews and consolidates memory periodically

## Privacy

This is a private knowledge base. Contains personal context and preferences.
