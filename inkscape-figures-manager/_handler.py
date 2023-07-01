import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path
from loguru import logger

from _inkscape import launcher, export_pdf_latex

# https://stackoverflow.com/questions/32923451
class Watcher:
    def __init__(self, figure_path):
        self.observer = Observer()
        self.figure_path = figure_path
        self.launcher = launcher(self.figure_path)

    def run(self):
        process = self.launcher
        logger.info("Open Inkscape")
        event_handler = Handler(self.figure_path)
        self.observer.schedule(event_handler, str(Path(self.figure_path).parent),
                               recursive=True)
        self.observer.start()
        while True:
            time.sleep(1)
            output, _ = process.communicate()
            if not output:
                process.terminate()
                self.observer.stop()
                logger.info("Process completed")
                break
        self.observer.join()

# https://stackoverflow.com/questions/11883336/detect-file-creation-with-watchdog
class Handler(PatternMatchingEventHandler):
    def __init__(self, figure_path):
        self.figure_path = figure_path
        self.export_pdf_latex = export_pdf_latex(self.figure_path)
        # Set the patterns for PatternMatchingEventHandler
        PatternMatchingEventHandler.__init__(
            self,
            patterns=["*.svg"],
            ignore_directories=True,
            case_sensitive=False,
        )
    def on_any_event(self, event):
        self.export_pdf_latex
