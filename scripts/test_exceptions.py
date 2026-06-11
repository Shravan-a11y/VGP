from app.core.expectations import ResourceNotFound

try:
    raise ResourceNotFound(
        "Visitor not found"
    )
except ResourceNotFound as error:
    print(error)