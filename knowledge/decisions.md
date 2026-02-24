# Decisions Log

## Architecture Decisions

### 2026-02-24: Memory System Design
- **Decision:** Create ErkMemory as GitHub repo
- **Reasoning:** Ericka wants persistent learning across sessions, GitHub provides version control and accessibility
- **Structure:** Organized by core/knowledge/patterns/logs/meta

### 2026-02-24: Credential Storage
- **Decision:** Store at ~/.config/clawdbot/credentials (chmod 600)
- **Reasoning:** Balance between security and accessibility
- **Note:** Also persist in .bashrc for env vars

## Business Decisions

*(Will be logged as made)*
