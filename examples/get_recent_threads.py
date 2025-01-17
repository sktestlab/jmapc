#!/usr/bin/env python3

import os
from datetime import datetime, timedelta, timezone

from jmapc import (
    Client,
    Comparator,
    EmailQueryFilterCondition,
    MailboxQueryFilterCondition,
    ResultReference,
)
from jmapc.methods import (
    EmailGet,
    EmailQuery,
    MailboxGet,
    MailboxQuery,
    ThreadGet,
)

# Create and configure client
client = Client(
    host=os.environ["JMAP_HOST"],
    user=os.environ["JMAP_USER"],
    password=os.environ["JMAP_PASSWORD"],
)

# Retrieve the Mailbox ID for the Inbox
results = client.method_calls(
    [
        MailboxQuery(filter=MailboxQueryFilterCondition(name="Inbox")),
        MailboxGet(
            ids=ResultReference(
                name=MailboxQuery.name,
                path="/ids",
                result_of="0",
            ),
        ),
    ]
)
# From results, second result, result object, retrieve Mailbox data
mailbox_data = results[1][1].data
if not mailbox_data:
    raise Exception("Inbox not found on the server")

# From the first mailbox result, retrieve the Mailbox ID
mailbox_id = mailbox_data[0].id
assert mailbox_id

print(f"Inbox has Mailbox ID {mailbox_id}")

# Search for the 5 most recent thread IDs in the Inbox, limited to emails
# received within the last 7 days
results = client.method_calls(
    [
        # Find email IDs for emails in the Inbox
        EmailQuery(
            collapse_threads=True,
            filter=EmailQueryFilterCondition(
                in_mailbox=mailbox_id,
                after=datetime.now(tz=timezone.utc) - timedelta(days=7),
            ),
            sort=[Comparator(property="receivedAt", is_ascending=False)],
            limit=5,
        ),
        # Use Email/query results to retrieve thread IDs for each email ID
        EmailGet(
            ids=ResultReference(
                name=EmailQuery.name,
                path="/ids",
                result_of="0",
            ),
            properties=["threadId"],
        ),
        # Use Email/get results to retrieve email counts for each thread ID
        ThreadGet(
            ids=ResultReference(
                name=EmailGet.name,
                path="/list/*/threadId",
                result_of="1",
            )
        ),
    ]
)

# From results, third result, result object, retrieve Threads data
for thread in results[2][1].data:
    print(f"Thread {thread.id} has {len(thread.email_ids)} emails")

# Example output:
#
# Inbox has Mailbox ID deadbeef-0000-0000-0000-000000000001
# Thread Tdeadbeefdeadbeef has 16 emails
# Thread Tc01dc0ffee15c01d has 2 emails
# Thread Tf00df00df00df00d has 98 emails
# Thread T0ffbea70ddba1100 has 1 emails
# Thread Tf0071e55f007ba11 has 7 emails
