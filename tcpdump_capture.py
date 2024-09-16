import os
import subprocess
import signal
from log_tcp_capture import setup_logger


class TcpdumpCapture:
    def __init__(self, interface='eth0', output_file=None, capture_filter=None):
        """Initialize tcpdump configuration."""
        self.interface = interface
        self.output_file = output_file if output_file else "capture.pcap"
        self.capture_filter = capture_filter
        self.process = None
        self.logger = setup_logger()

    def _build_command(self):
        """Build the tcpdump command based on options."""
        command = ['tcpdump', '-i', self.interface, '-w', self.output_file]
        if self.capture_filter:
            command.extend(self.capture_filter.split())
        return command

    def start_capture(self):
        """Start the tcpdump process."""
        try:
            command = self._build_command()
            self.logger.info(f"Starting tcpdump with command: {' '.join(command)}")
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            self.logger.error(f"Failed to Start tcpdump: {e}")

    def stop_capture(self):
        """Stop the tcpdump process."""
        if self.process is None:
            self.logger.info("There is no Such Process Ongoing..")
        try:
            self.logger.info("Stopping tcpdump...")
            os.kill(self.process.pid, signal.SIGINT)
            self.process.wait()
        except Exception as e:
            # raise TcpdumpError(f"Failed to stop tcpdump: {e}")
            self.logger.error(f"Unable to Stop tcpdump process: {e}")

    def configure(self, interface=None, output_file=None, capture_filter=None):
        """Configure options for the tcpdump capture."""
        if interface:
            self.interface = interface
        if output_file:
            self.output_file = output_file
        if capture_filter:
            self.capture_filter = capture_filter
        self.logger.info(
            f"Configuration updated: Interface={self.interface}, "
            f"Output File={self.output_file}, Filter={self.capture_filter}")

    def get_status(self):
        """Check if the tcpdump process is running."""
        if self.process and self.process.poll() is None:
            self.logger.debug("tcpdump is running")
            return True
        self.logger.debug("tcpdump is not running")
        return False
