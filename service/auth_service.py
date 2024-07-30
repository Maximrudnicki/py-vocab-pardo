import logging
import grpc

from auth_pb2 import TokenRequest
from auth_pb2_grpc import AuthenticationServiceStub

from utils.auth import get_user_id

from config.config import AUTH_SERVICE


class AuthenticationService:
    def connect_to_auth_service(self):
        try:
            return grpc.insecure_channel(AUTH_SERVICE)
        except Exception as e:
            logging.error(f"Failed to connect to auth service: {e}")
            raise Exception("Failed to connect to auth service") from e

    def get_user_id(self, req: TokenRequest):
        with self.connect_to_auth_service() as channel:
            client = AuthenticationServiceStub(channel)
            try:
                user_id_response = get_user_id(client, req)
                return user_id_response.user_id
            except Exception as e:
                logging.error(f"Get id from token failed: {e}")
                raise Exception("Invalid token") from e
