# Assigned to: Lakshan Kandeepan
# Phase: 2 (B2.6)
#
# TODO: Write tests for listing endpoints.
#
# Test cases to implement:
#
# test_create_listing_success:
#   - POST /listings with auth headers, valid form data (title, price, etc.)
#   - Assert 201 status, response has listing id, title, seller_id
#
# test_create_listing_unauthorized:
#   - POST /listings without auth headers
#   - Assert 401 status
#
# test_get_listings:
#   - Create a few listings
#   - GET /listings
#   - Assert 200 status, response has "listings" array and "total"
#
# test_get_listings_search:
#   - Create listings with different titles
#   - GET /listings?search=keyword
#   - Assert only matching listings returned
#
# test_get_listings_category_filter:
#   - Create listings with different categories
#   - GET /listings?category=Textbooks
#   - Assert only matching listings returned
#
# test_get_listing_by_id:
#   - Create a listing
#   - GET /listings/{id}
#   - Assert 200, response has full listing with images and seller
#
# test_get_listing_not_found:
#   - GET /listings/99999
#   - Assert 404
#
# test_update_listing_owner:
#   - Create listing, then PATCH /listings/{id} with owner's auth
#   - Assert 200, fields are updated
#
# test_update_listing_not_owner:
#   - Create listing as user A, try PATCH with user B's auth
#   - Assert 403
#
# test_create_listing_with_images:
#   - POST /listings with image files attached
#   - Assert images appear in response, files exist on disk

from pathlib import Path


def _create_listing(
    client,
    headers,
    *,
    title="Test Listing",
    price="25.00",
    category="Textbooks",
    description="A test listing",
    files=None,
):
    """
    Helper to create a listing through the real API.

    What it does:
    - Calls POST /listings/ using multipart/form-data
    - Includes auth headers (required by endpoint)
    - Optionally attaches image files via `files=...`

    Why it exists:
    - Many tests need to create listings first; this avoids repeating the same POST call logic.
    """
    return client.post(
        "/listings/",
        data={
            "title": title,
            "description": description,
            "price": price,  # Form fields arrive as strings; FastAPI converts to float internally
            "category": category,
        },
        files=files,
        headers=headers,
    )


def test_create_listing_success(client, auth_headers):
    """
    Tests: POST /listings/ (success path)

    Purpose:
    - Ensures an authenticated user can create a listing with valid form data.
    - Verifies the API returns 201 and a ListingOut-shaped response with key fields.
    """
    resp = _create_listing(
        client,
        auth_headers,
        title="My First Listing",
        price="10.50",
        category="Textbooks",
        description="Selling a book",
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    # Basic response sanity checks (ListingOut)
    assert "id" in data
    assert data["title"] == "My First Listing"
    assert "seller_id" in data
    assert "seller" in data
    assert data["seller"]["email"] == "testuser@my.yorku.ca"


def test_create_listing_unauthorized(client):
    """
    Tests: POST /listings/ (unauthorized)

    Purpose:
    - Ensures the endpoint is protected by JWT auth.
    - If no Authorization header is provided, API must return 401.
    """
    resp = client.post(
        "/listings/",
        data={
            "title": "No Auth Listing",
            "description": "Should fail",
            "price": "9.99",
            "category": "Other",
        },
    )
    assert resp.status_code == 401


def test_get_listings(client, auth_headers):
    """
    Tests: GET /listings/ (basic pagination response)

    Purpose:
    - Creates multiple listings
    - Calls GET /listings/
    - Confirms the response includes pagination wrapper fields:
      { listings: [...], total: int, page: int, limit: int }
    """
    _create_listing(client, auth_headers, title="Listing 1", price="5.00", category="Other")
    _create_listing(client, auth_headers, title="Listing 2", price="15.00", category="Textbooks")

    resp = client.get("/listings/")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert "listings" in data
    assert "total" in data
    assert data["page"] == 1
    assert data["limit"] == 20

    # We should see the two listings we created
    titles = [l["title"] for l in data["listings"]]
    assert "Listing 1" in titles
    assert "Listing 2" in titles
    assert data["total"] >= 2


def test_get_listings_search(client, auth_headers):
    """
    Tests: GET /listings/?search=...

    Purpose:
    - Creates listings with different titles
    - Searches for a keyword
    - Confirms only listings matching title/description are returned
    """
    _create_listing(client, auth_headers, title="MacBook Charger", price="20.00", category="Electronics")
    _create_listing(client, auth_headers, title="Textbook Calculus", price="30.00", category="Textbooks")
    _create_listing(client, auth_headers, title="Chair", price="10.00", category="Furniture")

    resp = client.get("/listings/", params={"search": "Textbook"})
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert len(data["listings"]) >= 1
    # Ensure every returned listing matches the search keyword in title OR description
    assert all(
        ("Textbook" in (l.get("title") or "")) or ("Textbook" in (l.get("description") or ""))
        for l in data["listings"]
    )


def test_get_listings_category_filter(client, auth_headers):
    """
    Tests: GET /listings/?category=...

    Purpose:
    - Creates listings across different categories
    - Filters by a category
    - Confirms only listings of that category are returned
    """
    _create_listing(client, auth_headers, title="Book A", price="12.00", category="Textbooks")
    _create_listing(client, auth_headers, title="Laptop", price="200.00", category="Electronics")

    resp = client.get("/listings/", params={"category": "Textbooks"})
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["total"] >= 1
    assert all(l["category"] == "Textbooks" for l in data["listings"])


def test_get_listing_by_id(client, auth_headers):
    """
    Tests: GET /listings/{listing_id}

    Purpose:
    - Creates a listing
    - Fetches it back by ID
    - Confirms the response includes nested seller + images fields as in ListingOut
    """
    create_resp = _create_listing(client, auth_headers, title="Single Listing", price="9.00", category="Other")
    assert create_resp.status_code == 201, create_resp.text
    listing_id = create_resp.json()["id"]

    resp = client.get(f"/listings/{listing_id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()

    assert data["id"] == listing_id
    assert "seller" in data
    assert data["seller"]["email"] == "testuser@my.yorku.ca"
    assert "images" in data
    assert isinstance(data["images"], list)


def test_get_listing_not_found(client):
    """
    Tests: GET /listings/{listing_id} for a non-existent listing

    Purpose:
    - Confirms the API returns a 404 when listing ID does not exist.
    """
    resp = client.get("/listings/99999")
    assert resp.status_code == 404


def test_update_listing_owner(client, auth_headers):
    """
    Tests: PATCH /listings/{listing_id} (owner success)

    Purpose:
    - Owner creates a listing
    - Owner updates it via PATCH
    - Confirms updated fields are reflected in the response
    """
    create_resp = _create_listing(client, auth_headers, title="Old Title", price="10.00", category="Other")
    assert create_resp.status_code == 201, create_resp.text
    listing_id = create_resp.json()["id"]

    patch_resp = client.patch(
        f"/listings/{listing_id}",
        json={"title": "New Title", "status": "sold"},
        headers=auth_headers,
    )
    assert patch_resp.status_code == 200, patch_resp.text
    data = patch_resp.json()

    assert data["title"] == "New Title"
    assert data["status"] == "sold"


def test_update_listing_not_owner(client, auth_headers, second_auth_headers):
    """
    Tests: PATCH /listings/{listing_id} (non-owner forbidden)

    Purpose:
    - User A creates a listing
    - User B attempts to update it
    - API should return 403 because only the seller/owner can update a listing
    """
    create_resp = _create_listing(client, auth_headers, title="Owner Listing", price="10.00", category="Other")
    assert create_resp.status_code == 201, create_resp.text
    listing_id = create_resp.json()["id"]

    patch_resp = client.patch(
        f"/listings/{listing_id}",
        json={"status": "removed"},
        headers=second_auth_headers,
    )
    assert patch_resp.status_code == 403


def test_create_listing_with_images(client, auth_headers):
    """
    Tests: POST /listings/ with images attached

    Purpose:
    - Ensures multipart file upload works for listing creation.
    - Confirms the response includes an images array (ImageOut objects).
    - Confirms the uploaded file is written to disk.

    Note:
    - The API returns file_path like "uploads/<uuid>.jpg".
    - Because the service saves to a relative "uploads/" path, the actual disk location depends
      on the working directory. When running pytest from repo root, the file may be in:
        - repo_root/uploads/...
      When running the app from backend/, it may be in:
        - repo_root/backend/uploads/...
    """
    files = [
        ("images", ("test-image.jpg", b"fake-image-bytes", "image/jpeg")),
    ]

    resp = _create_listing(
        client,
        auth_headers,
        title="Listing With Image",
        price="19.99",
        category="Other",
        description="Has an image",
        files=files,
    )
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert "images" in data
    assert len(data["images"]) == 1

    file_path = data["images"][0]["file_path"]  # e.g. "uploads/<uuid>.jpg"
    assert file_path.startswith("uploads/")

    # Verify file exists on disk in either possible location.
    disk_path_repo_root = Path(file_path)              # uploads/<uuid>.jpg
    disk_path_backend = Path("backend") / file_path    # backend/uploads/<uuid>.jpg

    assert (
        disk_path_repo_root.exists() or disk_path_backend.exists()
    ), f"Expected uploaded file at {disk_path_repo_root} or {disk_path_backend}, but it does not exist."