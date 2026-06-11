from app.core.dependencies import get_settings

settings=get_settings()

print(settings.PROJECT_NAME)
print(settings.API_VERSION)