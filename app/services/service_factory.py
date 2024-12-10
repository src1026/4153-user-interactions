from framework.services.data_access.MySQLRDBDataService import MySQLRDBDataService
from app.services.user_interaction_service import UserInteractionDataService

class ServiceFactory:
    @classmethod
    def get_service(cls, service_name: str):
        if service_name == 'UserInteractionDataService':
            context = dict(
                user="jigglypuff7",
                password="Jigglypuff7!",
                host="jigglypuff7.c7s86kaawl6v.us-east-2.rds.amazonaws.com",
                port=3306,
                database="user_interactions"
            )
            db_service = MySQLRDBDataService(context=context)
            return UserInteractionDataService(db=db_service)
        else:
            raise ValueError(f"Unknown service name: {service_name}")
