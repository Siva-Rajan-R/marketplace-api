import uuid

def generate_uuid() -> str:
    return str(
        uuid.uuid5(
            namespace=uuid.uuid4(),
            name=str(uuid.uuid4())
        )
    )