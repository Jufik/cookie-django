from django.core.management.base import BaseCommand
from django.core import management

import pymysql
from users.models import User
from companies.models import Company
from yards.models import Yard, Building

COMPANIES = {c.old_id: c for c in Company.objects.all()}


class Command(BaseCommand):
    """
    Sample Command
    Use it your own way
    """

    def handle(self, **options):
        management.call_command("load_companies")
        management.call_command("load_yards")
        management.call_command("load_lots")
        management.call_command("load_performances")
        management.call_command("load_levels")
        management.call_command("load_interventions")
        management.call_command("load_document_natures")
        management.call_command("load_users")
        management.call_command("load_documents")
        management.call_command("load_documents_interventions")
        management.call_command("load_versions")
        management.call_command("load_functions")
        management.call_command("load_contracts")
        management.call_command("load_teams")
        management.call_command("load_members")
