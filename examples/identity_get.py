#!/usr/bin/env python3

import os

from jmapc import Client
from jmapc.methods import IdentityGet

# Create and configure client
client = Client(
    host=os.environ["JMAP_HOST"],
    user=os.environ["JMAP_USER"],
    password=os.environ["JMAP_PASSWORD"],
)

# Prepare Identity/get request
# To retrieve all of the user's identities, no arguments are required.
method = IdentityGet()

# Call JMAP API with the prepared request
result = client.method_call(method)

# Print some information about each retrieved identity
for identity in result.data:
    print(
        f"Identity {identity.id} is for "
        f"{identity.name} at {identity.email}"
    )

# Example output:
#
# Identity 12345 is for Ness at ness@onett.example.com
# Identity 67890 is for Ness at ness-alternate@onett.example.com
