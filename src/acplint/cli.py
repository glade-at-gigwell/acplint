"""CLI entry point for acplint."""

from __future__ import annotations

import argparse
import sys

from acplint import __version__
from acplint.report import ConformanceLevel
from acplint.runner import ALL_CATEGORIES, ConformanceRunner


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="acplint",
        description="acplint - The linter for the Agent Client Protocol (ACP)",
    )
    parser.add_argument("--version", action="version", version=f"acplint {__version__}")
    parser.add_argument(
        "--agent",
        required=True,
        help="Command to start the ACP agent (e.g., 'claude-code', 'my-agent')",
    )
    parser.add_argument(
        "--agent-args",
        default="",
        help="Additional arguments to pass to the agent command",
    )
    parser.add_argument(
        "--cwd",
        default=None,
        help="Working directory for the agent process and sessions",
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        choices=ALL_CATEGORIES,
        default=None,
        help="Test categories to run (default: all)",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Write output to file instead of stdout",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--no-auto-allow",
        action="store_true",
        help="Don't auto-allow permission requests (queue them instead)",
    )

    args = parser.parse_args(argv)

    # Build agent command
    agent_command = [args.agent]
    if args.agent_args:
        agent_command.extend(args.agent_args.split())

    runner = ConformanceRunner(
        agent_command=agent_command,
        cwd=args.cwd,
        categories=args.categories,
        timeout=args.timeout,
        auto_allow_permissions=not args.no_auto_allow,
    )

    report = runner.run_all()

    # Output
    if args.output == "json":
        output = report.to_json()
    else:
        output = None  # Rich handles its own output

    if args.output == "text":
        report.print_summary()
    elif args.output == "json":
        if args.output_file:
            with open(args.output_file, "w") as f:
                f.write(output)
        else:
            print(output)

    # Exit code based on conformance level
    if report.conformance_level == ConformanceLevel.NON_CONFORMANT:
        return 2
    elif report.conformance_level == ConformanceLevel.PARTIAL:
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
