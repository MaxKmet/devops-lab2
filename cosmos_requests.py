from azure.cosmos import exceptions, CosmosClient, PartitionKey
import uuid

ARRIVAL_STATUS = {"arrived_status": "arrived", "not_arrived": "not arrived"}


def init_container(endpoint, key):
    client = CosmosClient(endpoint, key)

    database_name = 'GuestListDb'
    database = client.create_database_if_not_exists(id=database_name)

    container_name = 'GuestsContainer'
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/first_letter_name"),
        offer_throughput=400
    )

    return container


def add_guest_cosmos(container, guest_name):
    new_guest = {"id": guest_name + str(uuid.uuid4()), "name": guest_name,
                 "arrival_status": ARRIVAL_STATUS["not_arrived"], "first_letter_name": guest_name.lower()[0]}
    container.create_item(body=new_guest)


def get_guest_list_cosmos(container):
    query = "SELECT * FROM c"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    guest_list = []
    for it in items:
        g = {"name": it["name"], "arrival_status": it["arrival_status"]}
        guest_list.append(g)
    return guest_list


def mark_guest_arrived_cosmos(container, guest_name):
    query = f"SELECT * FROM c WHERE c.name='{guest_name}'"

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    for it in items:
        it["arrival_status"] = ARRIVAL_STATUS["arrived_status"]
        container.upsert_item(body=it)
