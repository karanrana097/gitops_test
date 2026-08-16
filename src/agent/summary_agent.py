from src.core.models import ProvisioningReport
from src.core.report_generator import generate_cli_report

class SummaryAgent:
    """
    Agent responsible for generating executive-ready, human-readable summary reports
    and enforcing human-in-the-loop governance reminders.
    """
    def generate_summary(self, report: ProvisioningReport) -> str:
        """Generates formatted string summary."""
        return generate_cli_report(report)
