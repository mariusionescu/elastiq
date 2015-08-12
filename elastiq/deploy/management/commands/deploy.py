from django.core.management.base import BaseCommand, CommandError
from console.models import Node
from console.sshclient import FlatSSH
from django.template.loader import render_to_string


class Command(BaseCommand):
    help = 'Deploy nodes'

    def handle(self, *args, **options):
        ssh = FlatSSH(
            hostname='main.elastiq.io',
            port=22,
            username='elastiq',
            password='Kevizu3'
        )
        for node in Node.objects.filter(status='pending'):
            node.status = 'deployed'
            commands = render_to_string('deploy.sh', {'node': node})
            ssh.run(commands, timeout=50)
            node.save()
