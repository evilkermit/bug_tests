"""Loads the main view and starts the Trame server."""

from bug_test.views import TestApp


def main() -> None:
    app = TestApp()
    app.server.start(server=True)


if __name__ == "__main__":
    main()
