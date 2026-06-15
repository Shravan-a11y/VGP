from app.core.exceptions import ResourceNotFound

try:
    raise ResourceNotFound(
        "Visitor not found"
    )
except ResourceNotFound as error:
    print(error)