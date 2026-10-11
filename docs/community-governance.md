# Discussions and Community Governance

## Scope and decision boundaries

GitHub Discussions is the public engineering forum; it is not a private support channel, customer ticketing system, hiring portal, investment forum, or venue for certification decisions. Public R1–R7 demonstrations are fabricated teaching cases. Technical proposals do not become project commitments without review and an accepted PR.

| Channel | Appropriate use |
|---|---|
| Announcements | Official updates, release notes, community guidance; restrict new posts to maintainers where supported |
| Q&A | Questions about synthetic scenarios, tests, reproducibility, and contribution setup |
| Ideas & Design | Alternatives, design tradeoffs, and proposals before opening implementation issues |
| Introductions | New members sharing technical interests without personal/contact details |
| Learning & Resources | Public educational materials with sources and licensing |

Create only the categories supported by actual community activity; avoid empty category sprawl. Prefer English for technical threads to support international review; Turkish is welcome, with an English summary for decisions that affect implementation.

## Triage and moderation

1. **Question?** Route to Q&A; mark a helpful verified answer when appropriate.
2. **Reproducible bug or accepted task?** Open an Issue with expected/actual behavior, synthetic reproduction, and acceptance criteria.
3. **Proposed code or documentation change?** Open a PR; link its discussion and issue.
4. **Sensitive information?** Do not quote or reproduce it; use private security reporting and remove exposed material through available platform tools.
5. **Spam, scams, crypto/token or gambling promotion?** Remove/report promptly and restrict repeat or serious offenders, per [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
6. **Moderation appeal?** Ask for a review through a non-sensitive issue or a private channel if disclosure would be unsafe.

Maintainers should distinguish verified facts from assumptions, avoid promising response times, and document substantive engineering decisions in version-controlled artifacts rather than relying on chat history alone.

## Launch checklist

- [ ] Enable Discussions in repository settings (owner action)
- [ ] Publish and pin the welcome Announcement (owner action)
- [ ] Configure Announcements, Q&A, Ideas & Design, Introductions, Learning & Resources as useful (owner action)
- [x] Publish draft conduct policy and governance documentation in PR #13
- [ ] Merge approved policy changes into main after owner review
- [ ] Link Code of Conduct and contribution guide in the welcome discussion
- [ ] Invite first contributors through concrete good-first-issue tasks
- [ ] Review first month of discussion quality and refine categories

**Authority:** Only repository owners or authorized maintainers can enforce moderation or change Discussion settings. This document does not imply those actions have already happened.
