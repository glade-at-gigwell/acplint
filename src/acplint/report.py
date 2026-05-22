"""Conformance test report and result types."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


class TestStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    ERROR = "ERROR"


class ConformanceLevel(str, Enum):
    FULL = "Full Conformance"
    PARTIAL = "Partial Conformance"
    NON_CONFORMANT = "Non-Conformant"


@dataclass
class TestResult:
    name: str
    category: str
    status: TestStatus
    duration_ms: float = 0.0
    message: str | None = None
    details: dict[str, Any] | None = None

    @property
    def passed(self) -> bool:
        return self.status == TestStatus.PASS


@dataclass
class CategorySummary:
    name: str
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errored: int = 0

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.skipped + self.errored

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.passed / self.total


class ConformanceReport:
    def __init__(self, agent_info: dict[str, Any] | None = None) -> None:
        self.results: list[TestResult] = []
        self.agent_info: dict[str, Any] = agent_info or {}
        self.findings: list[str] = field(default_factory=list) if False else []

    def add(self, result: TestResult) -> None:
        self.results.append(result)

    @property
    def passed(self) -> list[TestResult]:
        return [r for r in self.results if r.status == TestStatus.PASS]

    @property
    def failed(self) -> list[TestResult]:
        return [r for r in self.results if r.status == TestStatus.FAIL]

    @property
    def errors(self) -> list[TestResult]:
        return [r for r in self.results if r.status == TestStatus.ERROR]

    @property
    def skipped(self) -> list[TestResult]:
        return [r for r in self.results if r.status == TestStatus.SKIP]

    @property
    def conformance_level(self) -> ConformanceLevel:
        core_categories = {
            "initialization",
            "session_lifecycle",
            "streaming",
            "tool_calls",
            "schema_validation",
        }
        core_results = [r for r in self.results if r.category in core_categories]
        if not core_results:
            return ConformanceLevel.NON_CONFORMANT

        core_passed = sum(1 for r in core_results if r.status == TestStatus.PASS)
        core_total = len(core_results)
        core_rate = core_passed / core_total if core_total > 0 else 0

        all_passed = sum(1 for r in self.results if r.status == TestStatus.PASS)
        all_total = len(self.results)
        all_rate = all_passed / all_total if all_total > 0 else 0

        if core_rate >= 0.95 and all_rate >= 0.8:
            return ConformanceLevel.FULL
        elif core_rate >= 0.7:
            return ConformanceLevel.PARTIAL
        else:
            return ConformanceLevel.NON_CONFORMANT

    def category_summaries(self) -> dict[str, CategorySummary]:
        summaries: dict[str, CategorySummary] = {}
        for result in self.results:
            if result.category not in summaries:
                summaries[result.category] = CategorySummary(name=result.category)
            summary = summaries[result.category]
            if result.status == TestStatus.PASS:
                summary.passed += 1
            elif result.status == TestStatus.FAIL:
                summary.failed += 1
            elif result.status == TestStatus.SKIP:
                summary.skipped += 1
            elif result.status == TestStatus.ERROR:
                summary.errored += 1
        return summaries

    def print_summary(self, console: Console | None = None) -> None:
        console = console or Console()

        # Header
        level = self.conformance_level
        level_color = {
            ConformanceLevel.FULL: "green",
            ConformanceLevel.PARTIAL: "yellow",
            ConformanceLevel.NON_CONFORMANT: "red",
        }[level]

        console.print()
        console.print(Panel.fit(
            f"[{level_color}]{level.value}[/{level_color}]",
            title="ACP Conformance Result",
            border_style=level_color,
        ))

        # Agent info
        if self.agent_info:
            console.print(f"\nAgent: {self.agent_info.get('name', 'unknown')} v{self.agent_info.get('version', '?')}")

        # Category table
        table = Table(title="\nTest Results by Category", show_lines=True)
        table.add_column("Category", style="bold")
        table.add_column("Passed", justify="right", style="green")
        table.add_column("Failed", justify="right", style="red")
        table.add_column("Skipped", justify="right", style="dim")
        table.add_column("Errors", justify="right", style="red bold")
        table.add_column("Pass Rate", justify="right")

        for name, summary in sorted(self.category_summaries().items()):
            rate_color = "green" if summary.pass_rate >= 0.95 else "yellow" if summary.pass_rate >= 0.7 else "red"
            table.add_row(
                name,
                str(summary.passed),
                str(summary.failed),
                str(summary.skipped),
                str(summary.errored),
                f"[{rate_color}]{summary.pass_rate:.0%}[/{rate_color}]",
            )

        console.print(table)

        # Totals
        total_passed = len(self.passed)
        total_failed = len(self.failed)
        total_errors = len(self.errors)
        total_skipped = len(self.skipped)
        total = len(self.results)
        overall_rate = total_passed / total if total > 0 else 0

        console.print(f"\nTotal: {total} tests | {total_passed} passed | {total_failed} failed | {total_errors} errors | {total_skipped} skipped")
        console.print(f"Overall pass rate: {overall_rate:.1%}")

        # Failed test details
        if self.failed or self.errors:
            console.print("\n[bold red]Failed Tests:[/bold red]")
            for result in self.failed + self.errors:
                icon = "✗" if result.status == TestStatus.FAIL else "⚠"
                console.print(f"  {icon} [{result.category}] {result.name}: {result.message or 'N/A'}")

        # Findings — capabilities not supported
        if self.findings:
            console.print("\n[bold yellow]Findings:[/bold yellow]")
            for finding in self.findings:
                console.print(f"  {finding}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "conformance_level": self.conformance_level.value,
            "agent_info": self.agent_info,
            "findings": self.findings,
            "results": [
                {
                    "name": r.name,
                    "category": r.category,
                    "status": r.status.value,
                    "duration_ms": r.duration_ms,
                    "message": r.message,
                    "details": r.details,
                }
                for r in self.results
            ],
            "summary": {
                name: {
                    "passed": s.passed,
                    "failed": s.failed,
                    "skipped": s.skipped,
                    "errored": s.errored,
                    "pass_rate": s.pass_rate,
                }
                for name, s in self.category_summaries().items()
            },
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
