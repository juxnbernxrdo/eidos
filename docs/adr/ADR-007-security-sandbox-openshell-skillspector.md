# ADR-007: Multi-Layer Security Architecture: Skill Auditing and Execution Sandboxing

**Status:** Accepted  
**Date:** 2024-09-30 (Updated 2026)  
**Deciders:** Juan Bernardo Ordóñez (Author), AI Agent Systems Architecture Team  

---

## Context
Autonomous agents equipped with shell tools and dynamic skill loading represent a major attack surface:
1. **Malicious Tool Skills**: Community packages downloaded via registries may contain prompt injection payloads, obfuscated credential harvesting, or unauthorized reverse shells (as documented by NVIDIA SkillSpector).
2. **Adversarial Repository Files**: Files in public or unvetted repos can inject instructions that trick the agent into executing destructive commands (`rm -rf`, modifying git history, exfiltrating `.env` secrets).
3. **Conversational Guardrail Failure**: Natural language instructions ("do not run malicious commands") are fundamentally unreliable against direct or indirect prompt injections.

## Decision
Eidos adopts a **Defense-in-Depth Security Model** with two distinct enforcement gates:

### Gate 1: Pre-Installation Skill Security Inspection (SkillSpector Model)
Before any skill or tool extension is installed or registered in Eidos:
1. **Static Analysis**: The skill directory (`SKILL.md`, scripts, configs) is scanned using AST pattern matching and YARA signatures to detect dangerous system calls (`os.system`, `subprocess.Popen`, network socket manipulation, environment variable harvesting).
2. **Provenance & License Check**: Evaluates author reputation, repository provenance, install counts, and license compatibility.
3. **Risk Scoring**: Computes an automated Risk Score $\in [0, 100]$. Any skill scoring $> 25$ requires explicit human override; skills scoring $> 75$ are unconditionally rejected.

### Gate 2: Runtime Sandbox Isolation ("Policy-as-Physics" / OpenShell Model)
During task execution and automated verification:
1. **Filesystem Confinement**: Agents are confined to the workspace root using OS primitives (Linux Landlock or container namespaces). Access to `/etc`, `~/.ssh`, `~/.aws`, or parent directories is structurally denied by the operating system kernel.
2. **Network Egress Filtering**: Verification processes and untrusted subagents have network egress blocked by default, preventing data exfiltration during test execution.
3. **Process Sandboxing**: Commands are executed under unprivileged worker user IDs with strict execution timeouts.

## Consequences

### Positive
- Robust defense against supply-chain attacks from community skill registries.
- Immune to conversational jailbreaks attempting to access sensitive host files.
- Enterprise-compliant security posture suitable for auditing.

### Negative
- Landlock requires Linux kernel 5.13+ (gracefully degrades to standard container or process-level isolation on macOS/Windows).
- Pre-install skill scanning introduces a minor verification delay during skill installation.
