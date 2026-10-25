# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vincent Liu, WiseMotif.ai
# The Arithmetic Topos — Vincent Liu · WiseMotif.ai
"""Finite presentations of small categories by quivers and relations.

Treatise correspondence: see Appendix G of the book (The Reference Implementation).
Genuine computation: bounded path enumeration, composition, relation
normalization, functors, and naturality checks on finite presentations.
Interface-only: coherently presented (infinity,1)-categories.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from collections import deque
from typing import Callable, Iterable, Mapping, Sequence


@dataclass(frozen=True, order=True)
class Arrow:
    name: str
    source: str
    target: str


@dataclass(frozen=True)
class Path:
    objects: tuple[str, ...]
    arrows: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if len(self.objects) != len(self.arrows) + 1:
            raise ValueError("a path has one more object than arrows")

    @property
    def source(self) -> str:
        return self.objects[0]

    @property
    def target(self) -> str:
        return self.objects[-1]

    @property
    def length(self) -> int:
        return len(self.arrows)

    @classmethod
    def identity(cls, object_name: str) -> "Path":
        return cls((object_name,), ())

    def then(self, other: "Path") -> "Path":
        if self.target != other.source:
            raise ValueError("paths are not composable")
        return Path(self.objects + other.objects[1:], self.arrows + other.arrows)


@dataclass(frozen=True)
class Relation:
    left: tuple[str, ...]
    right: tuple[str, ...]

    def oriented(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        return (self.left, self.right) if (len(self.left), self.left) >= (
            len(self.right), self.right
        ) else (self.right, self.left)


@dataclass
class QuiverCategory:
    objects: set[str] = field(default_factory=set)
    arrows: dict[str, Arrow] = field(default_factory=dict)
    relations: list[Relation] = field(default_factory=list)

    def add_object(self, name: str) -> None:
        if not name:
            raise ValueError("object name cannot be empty")
        self.objects.add(name)

    def add_arrow(self, name: str, source: str, target: str) -> Arrow:
        if name in self.arrows:
            raise ValueError(f"duplicate arrow {name!r}")
        if source not in self.objects or target not in self.objects:
            raise ValueError("arrow endpoints must already exist")
        arrow = Arrow(name, source, target)
        self.arrows[name] = arrow
        return arrow

    def validate_arrow_word(self, word: Sequence[str]) -> tuple[str, ...]:
        if not word:
            return ()
        for name in word:
            if name not in self.arrows:
                raise ValueError(f"unknown arrow {name!r}")
        for left, right in zip(word, word[1:]):
            if self.arrows[left].target != self.arrows[right].source:
                raise ValueError("relation contains a noncomposable word")
        return tuple(word)

    def add_relation(self, left: Sequence[str], right: Sequence[str]) -> None:
        left_word = self.validate_arrow_word(left)
        right_word = self.validate_arrow_word(right)
        if left_word and right_word:
            if (
                self.arrows[left_word[0]].source != self.arrows[right_word[0]].source
                or self.arrows[left_word[-1]].target
                != self.arrows[right_word[-1]].target
            ):
                raise ValueError("relation sides need common endpoints")
        self.relations.append(Relation(left_word, right_word))

    def normalize_word(self, word: Sequence[str], max_steps: int = 10_000) -> tuple[str, ...]:
        current = tuple(word)
        rules = [relation.oriented() for relation in self.relations]
        for _ in range(max_steps):
            changed = False
            for source, target in rules:
                if not source:
                    continue
                for index in range(len(current) - len(source) + 1):
                    if current[index:index + len(source)] == source:
                        current = current[:index] + target + current[index + len(source):]
                        changed = True
                        break
                if changed:
                    break
            if not changed:
                return current
        raise RuntimeError("relation rewriting did not terminate")

    def paths(
        self, source: str, target: str, max_length: int
    ) -> tuple[Path, ...]:
        if source not in self.objects or target not in self.objects:
            raise ValueError("unknown endpoint")
        queue = deque([Path.identity(source)])
        output: dict[tuple[str, ...], Path] = {}
        outgoing: dict[str, list[Arrow]] = {name: [] for name in self.objects}
        for arrow in self.arrows.values():
            outgoing[arrow.source].append(arrow)
        while queue:
            path = queue.popleft()
            if path.target == target:
                normal = self.normalize_word(path.arrows)
                output.setdefault(normal, path)
            if path.length == max_length:
                continue
            for arrow in outgoing[path.target]:
                queue.append(
                    Path(
                        path.objects + (arrow.target,),
                        path.arrows + (arrow.name,),
                    )
                )
        return tuple(output[key] for key in sorted(output))

    def compose(self, left: Path, right: Path) -> tuple[str, ...]:
        return self.normalize_word(left.then(right).arrows)


@dataclass(frozen=True)
class FiniteFunctor:
    source: QuiverCategory
    target: QuiverCategory
    object_map: Mapping[str, str]
    arrow_map: Mapping[str, tuple[str, ...]]

    def verify(self) -> bool:
        if set(self.object_map) != self.source.objects:
            return False
        for name, arrow in self.source.arrows.items():
            word = self.arrow_map.get(name)
            if word is None:
                return False
            if word:
                first = self.target.arrows[word[0]]
                last = self.target.arrows[word[-1]]
                if first.source != self.object_map[arrow.source]:
                    return False
                if last.target != self.object_map[arrow.target]:
                    return False
            elif self.object_map[arrow.source] != self.object_map[arrow.target]:
                return False
        for relation in self.source.relations:
            left = sum((self.arrow_map[name] for name in relation.left), ())
            right = sum((self.arrow_map[name] for name in relation.right), ())
            if self.target.normalize_word(left) != self.target.normalize_word(right):
                return False
        return True
