from app.resources.user_interaction_resource import UserInteractionResource
from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService

class ServiceFactory:
    @classmethod
    def get_service(cls, service_name: str):
        if service_name == "UserInteractionDataService":
            # Replace with actual database credentials or connection pooling
            context = {
                "user": "db_user",
                "password": "secure_password",
                "host": "db_host",
                "port": 3306,
                "database": "user_interactions"
            }
            return MySQLRDBDataService(context=context)
        else:
            raise ValueError(f"Unknown service: {service_name}")
