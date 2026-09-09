import pytest

from topoprofile.workers.worker import SequentialWorker


def test_sequential_worker_executes_tasks_in_order() -> None:
    worker = SequentialWorker()

    execution_order = []

    def first_task() -> str:
        execution_order.append("first")
        return "first-result"

    def second_task() -> str:
        execution_order.append("second")
        return "second-result"

    results = worker.execute(
        [
            first_task,
            second_task,
        ]
    )

    assert execution_order == [
        "first",
        "second",
    ]
    assert results == [
        "first-result",
        "second-result",
    ]


def test_sequential_worker_propagates_task_error() -> None:
    worker = SequentialWorker()

    def failing_task() -> None:
        raise RuntimeError(
            "task failure"
        )

    with pytest.raises(
            RuntimeError,
            match="task failure",
    ):
        worker.execute(
            [failing_task]
        )
