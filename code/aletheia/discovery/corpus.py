# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Typed statement corpus and dependency DAG.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: cycle detection, topological order, transitive impact,
deduplication by canonical hashes, and dependency-status propagation.
Interface-only: semantic equivalence of distinct mathematical statements.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from collections import deque
from typing import Iterable, Iterator, Mapping

from aletheia.verification.status import EpistemicStatus, compose_statuses


class DependencyCycleError(ValueError):
    """The statement graph contains a directed cycle."""


@dataclass(frozen=True)
class Statement:
    identifier: str
    title: str
    text: str
    status: EpistemicStatus
    dependencies: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    reference: str | None = None

    def canonical_payload(self) -> dict[str, object]:
        return {
            "title": " ".join(self.title.split()),
            "text": " ".join(self.text.split()),
            "dependencies": sorted(self.dependencies),
            "tags": sorted(self.tags),
        }

    @property
    def semantic_hash(self) -> str:
        data = json.dumps(
            self.canonical_payload(), sort_keys=True, separators=(",", ":")
        )
        return sha256(data.encode()).hexdigest()


@dataclass
class StatementCorpus:
    statements: dict[str, Statement] = field(default_factory=dict)
    _hash_index: dict[str, str] = field(default_factory=dict)

    def add(self, statement: Statement, *, allow_duplicate_text: bool = False) -> None:
        if statement.identifier in self.statements:
            raise ValueError(f"duplicate statement id {statement.identifier!r}")
        duplicate = self._hash_index.get(statement.semantic_hash)
        if duplicate and not allow_duplicate_text:
            raise ValueError(
                f"statement duplicates canonical payload of {duplicate!r}"
            )
        missing = set(statement.dependencies) - set(self.statements)
        if missing:
            raise KeyError(f"dependencies must be inserted first: {sorted(missing)}")
        self.statements[statement.identifier] = statement
        self._hash_index[statement.semantic_hash] = statement.identifier
        try:
            self.topological_order()
        except DependencyCycleError:
            del self.statements[statement.identifier]
            self._hash_index.pop(statement.semantic_hash, None)
            raise

    def dependents(self) -> dict[str, set[str]]:
        result = {identifier: set() for identifier in self.statements}
        for statement in self.statements.values():
            for dependency in statement.dependencies:
                result[dependency].add(statement.identifier)
        return result

    def topological_order(self) -> tuple[str, ...]:
        indegree = {
            identifier: len(statement.dependencies)
            for identifier, statement in self.statements.items()
        }
        dependents = self.dependents()
        ready = deque(sorted(
            identifier for identifier, degree in indegree.items() if degree == 0
        ))
        order: list[str] = []
        while ready:
            identifier = ready.popleft()
            order.append(identifier)
            for child in sorted(dependents[identifier]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
        if len(order) != len(self.statements):
            cycle_nodes = sorted(
                identifier for identifier, degree in indegree.items() if degree
            )
            raise DependencyCycleError(
                f"dependency cycle includes {cycle_nodes}"
            )
        return tuple(order)

    def validate(self) -> bool:
        missing = {
            dependency
            for statement in self.statements.values()
            for dependency in statement.dependencies
            if dependency not in self.statements
        }
        if missing:
            raise KeyError(f"missing dependency nodes: {sorted(missing)}")
        self.topological_order()
        return True

    def what_breaks_if_false(self, identifier: str) -> tuple[str, ...]:
        if identifier not in self.statements:
            raise KeyError(identifier)
        graph = self.dependents()
        seen: set[str] = set()
        queue = deque([identifier])
        while queue:
            current = queue.popleft()
            for child in graph[current]:
                if child not in seen:
                    seen.add(child)
                    queue.append(child)
        return tuple(
            node for node in self.topological_order() if node in seen
        )

    def dependency_closure(self, identifier: str) -> tuple[str, ...]:
        if identifier not in self.statements:
            raise KeyError(identifier)
        seen: set[str] = set()

        def visit(node: str) -> None:
            for dependency in self.statements[node].dependencies:
                if dependency not in seen:
                    seen.add(dependency)
                    visit(dependency)

        visit(identifier)
        order = self.topological_order()
        return tuple(node for node in order if node in seen)

    def effective_status(self, identifier: str) -> EpistemicStatus:
        statement = self.statements[identifier]
        statuses = [statement.status]
        statuses.extend(
            self.effective_status(dependency)
            for dependency in statement.dependencies
        )
        return compose_statuses(statuses)

    def critical_path(self) -> tuple[str, ...]:
        order = self.topological_order()
        longest: dict[str, tuple[str, ...]] = {}
        for node in order:
            dependencies = self.statements[node].dependencies
            prefix = max(
                (longest[dependency] for dependency in dependencies),
                key=len,
                default=(),
            )
            longest[node] = (*prefix, node)
        return max(longest.values(), key=len, default=())

    def roadmap(self) -> list[dict[str, object]]:
        return [
            {
                "id": identifier,
                "title": self.statements[identifier].title,
                "declared": self.statements[identifier].status.value,
                "effective": self.effective_status(identifier).value,
                "blocked_by": list(self.statements[identifier].dependencies),
                "impact": len(self.what_breaks_if_false(identifier)),
            }
            for identifier in self.topological_order()
        ]
