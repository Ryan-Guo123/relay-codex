# Relay for Codex Launch Playbook

This document is for maintainers. The goal is not “announce the repo.” The goal is to make strangers immediately understand why Relay exists and why they should care.

## Positioning

Do not pitch Relay as:

- another prompt pack
- another agent framework
- another CLI loop

Pitch it as:

- an App-native control layer for Codex
- a repo-local memory and recovery system for long-running work
- a way to stop Codex from drifting, looping, and losing momentum

## The best launch angle

Lead with a real before/after:

- Before: Codex keeps re-running tests and asking the same question.
- After: Relay marks the repo `needs_review`, rewrites the queue, and gives a recovery brief.

That story is much stronger than “here is a plugin with five skills.”

## Assets to prepare before promotion

- a 20 to 40 second screen recording
- one clean screenshot of `.relay/` files in a real repo
- one real stuck-project example with repeated failure events
- one short thread or post explaining the four-state verdict

## Best channels

- X / Twitter
  - short clip plus a single before/after thesis
- GitHub README
  - needs to explain the problem in the first screen
- Hacker News
  - only when you have a real demo and a crisp explanation
- Reddit
  - target communities that care about Codex, agents, and developer workflow
- short YouTube demo
  - useful once the setup story is cleaner

## Star conversion checklist

- the repo description says what it does in one line
- the README hero explains the problem before the implementation
- the first screen shows a visual, not only text
- badges make the repo look maintained
- there is a credible test story
- there is a clear “why this is different” section
- there is a real demo, not only architecture

## First 14 days

### Day 1 to 3

- polish README
- publish the repo
- set repository topics
- make sure Actions are green

### Day 4 to 7

- record a real stuck-project demo
- post the before/after thread
- collect the first feedback and confusion points

### Day 8 to 14

- tighten install steps
- turn repeated feedback into README improvements
- ship one visible improvement quickly

## What usually gets ignored

- distribution matters as much as implementation
- examples matter more than architecture diagrams
- one strong use case beats five vague ones
- “App-native for Codex” is a better message than “Ralph-inspired”
