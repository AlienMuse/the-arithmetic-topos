# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Fair finite proof-search and tactic-scheduling interfaces.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: breadth-first search over a finite transition system,
best-first scheduling, budgets, and replayable traces.
Interface-only: Lean tactics are delegated through lean_bridge.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from heapq import heappop, heappush
from typing import Callable, Generic, Hashable, Iterable, Protocol, TypeVar

State = TypeVar("State", bound=Hashable)


@dataclass(frozen=True)
class SearchBudget:
    max_nodes: int = 10_000
    max_depth: int = 50


@dataclass(frozen=True)
class SearchStep(Generic[State]):
    tactic: str
    state: State


@dataclass(frozen=True)
class SearchResult(Generic[State]):
    found: bool
    path: tuple[SearchStep[State], ...]
    explored: int
    reason: str


Transition = Callable[[State], Iterable[tuple[str, State]]]


def breadth_first_search(
    initial: State,
    goal: Callable[[State], bool],
    transition: Transition[State],
    budget: SearchBudget = SearchBudget(),
) -> SearchResult[State]:
    queue = deque([(initial, ())])
    seen = {initial}
    explored = 0
    while queue and explored < budget.max_nodes:
        state, path = queue.popleft()
        explored += 1
        if goal(state):
            return SearchResult(True, path, explored, "goal reached")
        if len(path) >= budget.max_depth:
            continue
        for tactic, successor in transition(state):
            if successor in seen:
                continue
            seen.add(successor)
            queue.append((successor, (*path, SearchStep(tactic, successor))))
    reason = "node budget exhausted" if queue else "finite search space exhausted"
    return SearchResult(False, (), explored, reason)


def best_first_search(
    initial: State,
    goal: Callable[[State], bool],
    transition: Transition[State],
    heuristic: Callable[[State], float],
    budget: SearchBudget = SearchBudget(),
) -> SearchResult[State]:
    counter = 0
    heap: list[tuple[float, int, State, tuple[SearchStep[State], ...]]] = []
    heappush(heap, (heuristic(initial), counter, initial, ()))
    best_depth = {initial: 0}
    explored = 0
    while heap and explored < budget.max_nodes:
        _, _, state, path = heappop(heap)
        explored += 1
        if goal(state):
            return SearchResult(True, path, explored, "goal reached")
        if len(path) >= budget.max_depth:
            continue
        for tactic, successor in transition(state):
            depth = len(path) + 1
            if depth >= best_depth.get(successor, budget.max_depth + 1):
                continue
            best_depth[successor] = depth
            counter += 1
            new_path = (*path, SearchStep(tactic, successor))
            heappush(heap, (depth + heuristic(successor), counter, successor, new_path))
    return SearchResult(False, (), explored, "budget or search space exhausted")
