import logging
import grpc
from concurrent import futures

import vocab_pb2_grpc

from service.grpc_service import Vocab
from config.config import GRPC_PORT


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vocab_pb2_grpc.add_VocabServiceServicer_to_server(Vocab(), server)

    server.add_insecure_port(GRPC_PORT)

    server.start()

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
