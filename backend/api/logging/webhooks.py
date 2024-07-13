from discord_webhook import DiscordWebhook
from api.config.config import Config


WEBHOOK_FUNCTIONS = {
    'submit': 'submission',
    'edit_submission': 'submission',
    'approve_submission': 'submission',
    'deny_submission': 'submission',
    'request_namechange': 'namechange',
    'approve_namechange': 'namechange',
    'deny_namechange': 'namechange'
}

# Sends a webhook to the webhook channel indicating that an audited function was performed
def send_webhook(function_name, audit_id, *args):
    webhook_type = WEBHOOK_FUNCTIONS[function_name]

    message = f'function={function_name}|audit_id={audit_id}|'
    if webhook_type == 'namechange':
        discord_id, old_name, new_name, namechange_id = args
        message += f'discord_id={discord_id}|old_name={old_name}|new_name={new_name}|_id={namechange_id}'

    else:
        submission, = args

        submission_components = []
        for key, value in submission.items():
            submission_components.append(f'{key}={value}')
        message += '|'.join(submission_components)

    DiscordWebhook(url=Config.WEBHOOK_URL,
                   content=message
                   ).execute()