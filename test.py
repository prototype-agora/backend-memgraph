import pytest
from schema import schema
from database import init_db


async def createUniqueUser():
    await init_db()
    
    mutation = """
        mutation TestMutation {
            createUniqueappuser(firstName: "Ulf") {
                firstName
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
    )
    return resp.data["createUniqueappuser"], resp.errors


@pytest.mark.asyncio
async def test_create_user_then_get_user_by_name():
    data, errors = await createUniqueUser()
    query = """
        query TestQuery {
            getAppUser(firstName: "Ulf") {
                firstName
                id
            }
        }
    """

    resp = await schema.execute(
        query
    )
    assert resp.errors is None
    assert resp.data["getAppUser"] == {
        "firstName": data["firstName"],
        "id": data["id"]
    }


@pytest.mark.asyncio
async def test_create_unique_user():
    data, errors = await createUniqueUser()
    mutation = """
        mutation TestMutation {
            createUniqueappuser(firstName: "Ulf") {
                firstName
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
    )

    assert resp.errors is None
    assert resp.data["createUniqueappuser"] == {
        "firstName": data["firstName"],
        "id": data["id"]
    }

@pytest.mark.asyncio
async def test_create_source():
    mutation = """
        mutation TestMutation {
            createSource(link: "https://www.nachdenkseiten.de/?p=121861", title: "Gipfel der Ratlosigkeit") {
                id
            }
        }
    """

    resp = await schema.execute(
        mutation,
    )

    assert resp.errors is None

@pytest.mark.asyncio
async def test_create_post_with_known_user():
    data, errors = await createUniqueUser()
    mutation = """
        mutation TestMutation {
            createPost(firstName: "Ulf", commentText:"commentText", link:"https://www.nachdenkseiten.de/?p=121861", quoteText:"quoteText", title:"Gipfel der Ratlosigkeit") {
                appuserId
                commentId
                quoteId
                sourceId
            }
        }
    """
    resp = await schema.execute(
        mutation,
    )
    assert resp.errors is None
    assert data["id"] == resp.data["createPost"]["appuserId"]