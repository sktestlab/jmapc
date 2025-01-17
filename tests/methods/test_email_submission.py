from datetime import datetime, timezone

import responses

from jmapc import (
    Address,
    Client,
    EmailSubmission,
    Envelope,
    SetError,
    UndoStatus,
)
from jmapc.methods import (
    EmailSetResponse,
    EmailSubmissionSet,
    EmailSubmissionSetResponse,
)

from ..utils import expect_jmap_call

expected_request_create = {
    "emailToSend": {
        "emailId": "#draft",
        "identityId": "1000",
        "envelope": {
            "mailFrom": {
                "email": "ness@onett.example.com",
                "parameters": None,
            },
            "rcptTo": [
                {
                    "email": "ness@onett.example.com",
                    "parameters": None,
                }
            ],
        },
    }
}
email_submission_set_response = {
    "accountId": "u1138",
    "created": {
        "emailToSend": {
            "id": "S2000",
            "sendAt": "1994-08-24T12:01:02Z",
            "undoStatus": "final",
        }
    },
    "updated": None,
    "destroyed": None,
    "oldState": "1",
    "newState": "2",
    "notCreated": None,
    "notUpdated": None,
    "notDestroyed": None,
}


def test_email_submission_set(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                },
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "uno",
            ]
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        EmailSubmissionSet(
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            )
        )
    ) == EmailSubmissionSetResponse(
        account_id="u1138",
        old_state="1",
        new_state="2",
        created=dict(
            emailToSend=EmailSubmission(
                id="S2000",
                undo_status=UndoStatus.FINAL,
                send_at=datetime(1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc),
            ),
        ),
        updated=None,
        destroyed=None,
        not_created=None,
        not_updated=None,
        not_destroyed=None,
    )


def test_email_submission_set_on_success_destroy_email(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                    "onSuccessDestroyEmail": ["#emailToSend"],
                },
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "uno",
            ],
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "oldState": "2",
                    "newState": "3",
                    "created": None,
                    "updated": None,
                    "destroyed": ["Mdeadbeefdeadbeefdeadbeef"],
                    "notCreated": None,
                    "notUpdated": None,
                    "notDestroyed": None,
                },
                "uno",
            ],
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        EmailSubmissionSet(
            on_success_destroy_email=["#emailToSend"],
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            ),
        )
    ) == [
        EmailSubmissionSetResponse(
            account_id="u1138",
            old_state="1",
            new_state="2",
            created=dict(
                emailToSend=EmailSubmission(
                    id="S2000",
                    undo_status=UndoStatus.FINAL,
                    send_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                ),
            ),
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
        EmailSetResponse(
            account_id="u1138",
            old_state="2",
            new_state="3",
            created=None,
            updated=None,
            destroyed=["Mdeadbeefdeadbeefdeadbeef"],
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
    ]


def test_email_submission_set_on_success_update_email(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                    "onSuccessUpdateEmail": {
                        "keywords/$draft": None,
                    },
                },
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "uno",
            ],
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "oldState": "2",
                    "newState": "3",
                    "created": None,
                    "updated": {
                        "Mdeadbeefdeadbeefdeadbeef": None,
                    },
                    "destroyed": None,
                    "notCreated": None,
                    "notUpdated": None,
                    "notDestroyed": None,
                },
                "uno",
            ],
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        EmailSubmissionSet(
            on_success_update_email={
                "keywords/$draft": None,
            },
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            ),
        )
    ) == [
        EmailSubmissionSetResponse(
            account_id="u1138",
            old_state="1",
            new_state="2",
            created=dict(
                emailToSend=EmailSubmission(
                    id="S2000",
                    undo_status=UndoStatus.FINAL,
                    send_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                ),
            ),
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
        EmailSetResponse(
            account_id="u1138",
            old_state="2",
            new_state="3",
            created=None,
            updated={"Mdeadbeefdeadbeefdeadbeef": None},
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
    ]


def test_email_submission_set_update_email_error(
    client: Client, http_responses: responses.RequestsMock
) -> None:
    expected_request = {
        "methodCalls": [
            [
                "EmailSubmission/set",
                {
                    "accountId": "u1138",
                    "create": expected_request_create,
                    "onSuccessUpdateEmail": {
                        "keywords/$draft": None,
                        "mailboxIds/MBX5": None,
                    },
                },
                "uno",
            ]
        ],
        "using": [
            "urn:ietf:params:jmap:core",
            "urn:ietf:params:jmap:submission",
        ],
    }
    response = {
        "methodResponses": [
            [
                "EmailSubmission/set",
                email_submission_set_response,
                "uno",
            ],
            [
                "Email/set",
                {
                    "accountId": "u1138",
                    "oldState": "2",
                    "newState": "3",
                    "created": None,
                    "updated": None,
                    "destroyed": None,
                    "notCreated": None,
                    "notUpdated": {
                        "Mdeadbeefdeadbeefdeadbeef": {
                            "type": "invalidProperties",
                            "properties": ["mailboxIds"],
                        },
                    },
                    "notDestroyed": None,
                },
                "uno",
            ],
        ]
    }
    expect_jmap_call(http_responses, expected_request, response)
    assert client.method_call(
        EmailSubmissionSet(
            on_success_update_email={
                "keywords/$draft": None,
                "mailboxIds/MBX5": None,
            },
            create=dict(
                emailToSend=EmailSubmission(
                    email_id="#draft",
                    identity_id="1000",
                    envelope=Envelope(
                        mail_from=Address(email="ness@onett.example.com"),
                        rcpt_to=[Address(email="ness@onett.example.com")],
                    ),
                )
            ),
        )
    ) == [
        EmailSubmissionSetResponse(
            account_id="u1138",
            old_state="1",
            new_state="2",
            created=dict(
                emailToSend=EmailSubmission(
                    id="S2000",
                    undo_status=UndoStatus.FINAL,
                    send_at=datetime(
                        1994, 8, 24, 12, 1, 2, tzinfo=timezone.utc
                    ),
                ),
            ),
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated=None,
            not_destroyed=None,
        ),
        EmailSetResponse(
            account_id="u1138",
            old_state="2",
            new_state="3",
            created=None,
            updated=None,
            destroyed=None,
            not_created=None,
            not_updated={
                "Mdeadbeefdeadbeefdeadbeef": SetError(
                    type="invalidProperties", description=None
                )
            },
            not_destroyed=None,
        ),
    ]
