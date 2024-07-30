import grpc
import logging

from auth_pb2_grpc import AuthenticationServiceStub
from auth_pb2 import TokenRequest, UserIdResponse


def get_user_id(client: AuthenticationServiceStub, req: TokenRequest) -> UserIdResponse:
    try:
        res = client.GetUserId(req)
        return res
    except grpc.RpcError as e:
        logging.error(f"Error happened while getting id from token: {e}")
        raise Exception("Error happened while getting id from token") from e
