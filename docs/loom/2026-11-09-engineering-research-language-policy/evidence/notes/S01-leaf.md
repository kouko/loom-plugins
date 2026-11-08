---
title: "Leaf 2017: double-buffer rationale and outage headroom"
type: loom-research
status: concluded
created: 2026-11-09
updated: 2026-11-09
tags:
  - loom/research
---

# Leaf 2017: double-buffer rationale and outage headroom

## Question and scope

Why did the original 2017 Leaf design add a second segment buffer, when was it loaded, and what database-outage headroom did its authors claim? This informs whether the pattern is a useful reference for low tail latency during brief database interruptions. Historical attribution only; no implementation or publication is authorized.

## Method and rationale

Direct inspection of the original engineering article answers this attribution question; a brief failure-boundary analysis separates the historical statement from present guarantees. Existing MySQL AUTO_INCREMENT evidence explains a different mechanism and cannot establish Leaf-specific intent. Exploratory English, Japanese and Chinese queries ran together; Chinese was included immediately because Meituan's original account uses Chinese. Only the applicable original article was needed; repeated summaries were not treated as independent support. Stop condition: inspect its rationale, refill condition and outage claim in context.

## Findings

The following are **historical author claims**, supported by [Meituan's original article](https://tech.meituan.com/2017/04/21/mt-leaf.html), dated 2017-04-21, by 照东:

- **Why:** fetching only after exhausting a segment blocked request threads on database I/O; network jitter or slow queries produced tail-latency spikes. Asynchronous prefetch into a second buffer aimed to reduce TP999 (99.9th-percentile latency).
- **When:** after **10% of the current segment had been issued**, if the next segment was not updated, a separate thread loaded it. At exhaustion, switching depended on the next segment being ready. Each request checked the next-segment state.
- **Claimed headroom:** with per-business consumption monitoring, they recommended segment length equal to **600 times peak issuing QPS** (ten minutes of IDs), and claimed **10–20 minutes** of unaffected issuance during a database outage.
- **Separate concern:** the article addressed database availability separately through replication and failover; buffering did not remove database dependence.

## Evidence

- **Primary engineering report:** [Leaf——美团点评分布式ID生成系统](https://tech.meituan.com/2017/04/21/mt-leaf.html), author/date above; inspected 2026-11-09. Read the actual page, including “Leaf-segment数据库方案”, “双buffer优化” and “Leaf高可用容灾” (browser extraction lines 145–174). These support the four findings respectively; they are documentation/reported design, not measured behavior here. Authorship/date were visible at lines 2–4.
- The supplied preflight evidence was read and excluded as support for historical attribution. No repository implementation was inspected and no allocator was executed. No benchmark or outage experiment ran.

## Decision impact

**Inference:** the pattern is a credible design reference for hiding refill latency, conditional on prefetch completing before exhaustion. It does not establish that this service will meet its tail-latency or outage target.

For a constant issuing rate, available time is approximately **remaining usable IDs / IDs per second**. This is a capacity calculation, not an additional author guarantee: traffic surges, a failed prefetch, or losing in-memory state can shorten coverage. A nominal ten-minute segment is not a universal minimum outage window.

## Limitations and open questions

This is the currently accessible page carrying the 2017 date, not an archived byte-for-byte 2017 snapshot. Its outage statement is an attributed historical sizing claim, without an inspected outage test or detailed workload distribution. Current Leaf code, releases and deployments remain unverified. Present adoption needs the intended implementation's failure behavior and representative interruption/load measurements; this investigation does not select or validate it for production.
