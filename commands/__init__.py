from commands.channels import setup as setup_channels
from commands.direct_message import setup as setup_direct_message
from commands.fetch import setup as setup_fetch
from commands.general import setup as setup_general
from commands.moderation import setup as setup_moderation
from commands.roles import setup as setup_roles
from commands.roster import setup as setup_roster
from commands.tryout_results import setup as setup_tryout_results

# from commands.ticket_commands import setup as setup_tickets


def setup_all(tree, bot):
    setup_general(tree, bot)
    setup_moderation(tree, bot)
    setup_fetch(tree, bot)
    setup_channels(tree, bot)
    setup_direct_message(tree, bot)
    setup_roles(tree, bot)
    setup_tryout_results(tree, bot)
    setup_roster(tree, bot)
    # setup_tickets(tree, bot)
