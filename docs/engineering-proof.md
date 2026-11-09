# Engineering Proof of Work — Kevin Marville

**Public technical case study · 9 November 2026**

[Portfolio public](https://kvnbbg.github.io/PersonalPortfolio/engineering-proof.html) · [Profil GitHub](https://github.com/Kvnbbg) · [Workflow documentaire public](../.github/workflows/engineering-proof.yml)

> This document is a deliberately limited, privacy-safe account of engineering work. It does not claim that private tests are passing, that a private repository is publicly inspectable, or that a Vercel build proves business acceptance. The **document and its workflow source are public**, while the SaaS source repository and private logs are not.

## Scope

| Discipline | Engineering work | Evidence classification |
| --- | --- | --- |
| Full-stack & product | React/TypeScript interfaces, account recovery, readable Pro pages | Private project · summarized |
| DevOps / CI/CD | Versioned workflows, release checks, Vercel previews, diagnostic timeline | Public documentary workflow; private build outcome summarized |
| Security | Server-authoritative entitlements, Stripe callback treated as untrusted, sign-out/account-switch isolation | Private project · summarized, not security-certified |
| Quality | Regression tests authored for session restoration, stale tiers, network errors, and account switching | Tests **written**, execution **not confirmed** |
| Operations | Incident notes with evidence, unknowns, acceptance criteria, and follow-up | This public record and Git history |

## Case study 01 — A Pro interface must remain readable

**Problem.** A subscription-verification screen could replace content during session refreshes, while an RPG onboarding message appeared on a login flow. This was a UX and resilience defect, not proof that Stripe payments had failed.

**Approach.**
1. Separate the public pricing page from the Stripe re-synchronization call.
2. Keep protected access server-authoritative; a checkout success URL is not an entitlement.
3. Prevent a previously verified identity or tier from being reused for a different account.
4. Keep billing errors from becoming misleading “Active Pro” labels.
5. Replace a noisy spinner with a static, accessible session-checking message.
6. Add regression tests for identity changes, incomplete verification, and network errors.

**Current evidence and limitations.** The relevant code and PRs are in a **private repository**. The implementation and tests were authored there; a publicly viewable review and green test report have **not** been established. This note is a technical narrative, not a substitute for access to that repository.

## Case study 02 — Distinguishing a build from CI

**Timestamp:** observed on 8–9 November 2026; not a live monitor.

- **Vercel:** the relevant preview build was reported **READY** for the inspected commit.
- **GitHub Actions:** four workflows were reported **failure**. They terminated before steps became accessible through the available integration.
- **Logs:** log download returned **404 BlobNotFound**, so no failing test assertion could be confirmed.
- **Diagnosis:** runner initialization, repository Actions permissions, and billing/quota settings are **hypotheses**, not established root causes. Additional TypeScript diagnostics in unrelated modules are a separate concern.
- **Resolution:** **open** at the last observation. Never print a green CI badge or claim a passing suite until a genuine run shows that result.

### Incident-response decision record

| Stage | Evidence | Next action |
| --- | --- | --- |
| Triage | Workflow failure; steps unavailable | Review run annotations in GitHub UI |
| Isolation | Vercel preview reached READY | Verify compiler vs test runner outcomes independently |
| Platform | Failure before job execution possible; cause unknown | Review Actions settings, quota/billing and permissions |
| Quality | Regression tests committed but not yet confirmed executed | Run Node/typecheck/Vitest on a permitted runner |
| Release | Private CI not green | Keep changes out of production until validated |

## This public workflow

The repository has a lightweight [engineering-proof workflow](../.github/workflows/engineering-proof.yml). Its purpose is **not to pretend it tests a private SaaS**. It validates that this public document maintains minimum disclosure rules: incident state, a private-source disclaimer, relevant links, and no direct link to private GitHub PRs or credentials.

Inspect the workflow source and future run outcomes [here](https://github.com/Kvnbbg/kvnbbg/actions/workflows/engineering-proof.yml). If it has not run or fails, its existence is source evidence, **not** execution success.

**Publicly verified run, 9 November 2026:** [GitHub Actions run 42568715441](https://github.com/Kvnbbg/kvnbbg/actions/runs/42568715441) finished **success**. Its visible steps — checkout, offline evidence/privacy contract, whitespace validation, and completion — all concluded successfully. This is a real **public documentation CI** result, **not** an assertion that the private SaaS tests or payment security gates passed.

## Acceptance criteria for a future green report

- [ ] Workflows execute actual steps and publish readable logs.
- [ ] Unit/integration tests and security gates complete successfully.
- [ ] Server entitlement checks remain in force for sign-out, checkout returns, and account switching.
- [ ] Pro UI reads without verification flicker on real mobile and desktop sessions.
- [ ] Only then update this public page with dated, inspectable success evidence.

## Privacy, scope and reuse

This report excludes private repository identifiers, private PR URLs, internal job logs, user emails, Stripe IDs, webhook secrets, tokens, unpublished client work, and individual account records. Claims are bounded by available evidence as of the stated date.

For public code, see [commits](https://github.com/Kvnbbg/kvnbbg/commits/main), [workflow source](../.github/workflows/engineering-proof.yml) and [workflow runs](https://github.com/Kvnbbg/kvnbbg/actions/workflows/engineering-proof.yml).

**Document version:** 2026-11-09 · Editorial snapshot, no automatic status feed.
