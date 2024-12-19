from core.text_comparer import TextComparer
from thread_runner.thread_runner import ThreadRunner


def debug() -> None:
    text_comparer: TextComparer = TextComparer()

    print(
        ThreadRunner.run_function(
            function=text_comparer.compare_similarity,
            language="en_core_web_sm",
            source="Hello",
            target="World",
        )
    )


if __name__ == "__main__":
    debug()
