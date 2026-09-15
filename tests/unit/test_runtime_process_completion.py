"""Deterministic scheduling of real child completion at the monitor boundary."""

from __future__ import annotations

import linecache
import sys
import threading
import time
from pathlib import Path
from types import FrameType
from typing import TYPE_CHECKING

from flext_tests import tm

from tests import u

if TYPE_CHECKING:
    from _typeshed import TraceFunction


class TestsRuntimeProcessCompletion:
    """A completed child must not wait for its execution deadline."""

    def test_completion_before_wake_clear_returns_promptly(
        self, tmp_path: Path
    ) -> None:
        """Schedule a real waiter at the exact lost-notification boundary.

        Tracing only controls thread scheduling; process creation, events,
        waiting, output and cleanup all use the unmodified public runtime.
        """
        scheduled: list[bool] = []

        def trace(frame: FrameType, event: str, _argument: object) -> TraceFunction:
            if (
                event == "line"
                and frame.f_code.co_name == "_monitor_process"
                and linecache.getline(frame.f_code.co_filename, frame.f_lineno).strip()
                == "wake.clear()"
                and not scheduled
            ):
                done = frame.f_locals["process_done"]
                wake = frame.f_locals["wake"]
                assert isinstance(done, threading.Event)
                assert isinstance(wake, threading.Event)
                assert done.wait(2)
                assert wake.wait(2)
                scheduled.append(True)
            return trace

        previous = sys.gettrace()
        started = time.monotonic()
        try:
            sys.settrace(trace)
            result = u.Cli().run_to_file(
                [sys.executable, "-c", "import time;time.sleep(.1);print('complete')"],
                tmp_path / "completion.log",
                timeout=4,
            )
        finally:
            sys.settrace(previous)
        elapsed = time.monotonic() - started
        outcome = tm.ok(result)
        assert scheduled == [True]
        assert outcome.raw_return_code == 0
        assert not outcome.timed_out
        assert elapsed < 2
        assert (tmp_path / "completion.log").read_text() == "complete\n"
