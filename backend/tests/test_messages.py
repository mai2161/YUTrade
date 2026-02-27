# Assigned to: Raj (Rajendra Brahmbhatt)
# Phase: 3 (B3.6)

from app.models.listing import Listing
from app.models.user import User


def _create_listing(db_session, seller_id: int) -> Listing:
    """Helper to insert a listing directly via ORM (listing router not yet implemented)."""
    listing = Listing(
        seller_id=seller_id,
        title="Test Textbook",
        description="A test listing",
        price=25.00,
        category="Textbooks",
    )
    db_session.add(listing)
    db_session.commit()
    db_session.refresh(listing)
    return listing


def _get_user_id(db_session, email: str) -> int:
    """Look up a user's ID by email."""
    return db_session.query(User).filter(User.email == email).first().id


def test_send_message_to_seller(client, db_session, auth_headers, second_auth_headers):
    """User B sends a message to User A's listing. Receiver should be the seller."""
    seller_id = _get_user_id(db_session, "testuser@my.yorku.ca")
    listing = _create_listing(db_session, seller_id)

    resp = client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "Is this still available?"},
        headers=second_auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["listing_id"] == listing.id
    assert data["receiver_id"] == seller_id
    assert data["content"] == "Is this still available?"


def test_seller_reply(client, db_session, auth_headers, second_auth_headers):
    """After a buyer messages, the seller can reply back to that buyer."""
    seller_id = _get_user_id(db_session, "testuser@my.yorku.ca")
    buyer_id = _get_user_id(db_session, "testuser2@my.yorku.ca")
    listing = _create_listing(db_session, seller_id)

    # Buyer sends first message
    client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "Hi, is this available?"},
        headers=second_auth_headers,
    )

    # Seller replies
    resp = client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "Yes it is!"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["sender_id"] == seller_id
    assert data["receiver_id"] == buyer_id


def test_get_messages(client, db_session, auth_headers, second_auth_headers):
    """Participants can retrieve messages in chronological order."""
    seller_id = _get_user_id(db_session, "testuser@my.yorku.ca")
    listing = _create_listing(db_session, seller_id)

    # Exchange messages
    client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "First message"},
        headers=second_auth_headers,
    )
    client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "Second message"},
        headers=auth_headers,
    )

    # Buyer fetches messages
    resp = client.get(
        f"/listings/{listing.id}/messages/",
        headers=second_auth_headers,
    )
    assert resp.status_code == 200
    messages = resp.json()["messages"]
    assert len(messages) == 2
    assert messages[0]["content"] == "First message"
    assert messages[1]["content"] == "Second message"


def test_send_message_unauthorized(client, db_session, auth_headers):
    """Sending a message without auth returns 401."""
    seller_id = _get_user_id(db_session, "testuser@my.yorku.ca")
    listing = _create_listing(db_session, seller_id)

    resp = client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "No auth"},
    )
    assert resp.status_code == 401


def test_send_message_listing_not_found(client, second_auth_headers):
    """Messaging a non-existent listing returns 404."""
    resp = client.post(
        "/listings/99999/messages/",
        json={"content": "Hello?"},
        headers=second_auth_headers,
    )
    assert resp.status_code == 404


def test_cannot_message_self(client, db_session, auth_headers):
    """Seller cannot start a thread on their own listing with no prior buyer message."""
    seller_id = _get_user_id(db_session, "testuser@my.yorku.ca")
    listing = _create_listing(db_session, seller_id)

    resp = client.post(
        f"/listings/{listing.id}/messages/",
        json={"content": "Talking to myself"},
        headers=auth_headers,
    )
    assert resp.status_code == 400
