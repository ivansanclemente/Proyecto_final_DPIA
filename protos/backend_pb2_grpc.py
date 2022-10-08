# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import backend_pb2 as backend__pb2


class BackendService(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.load_image = channel.unary_unary(
                '/Backend/load_image',
                request_serializer=backend__pb2.img_path.SerializeToString,
                response_deserializer=backend__pb2.image.FromString,
                )


class BackendServicer(object):
    """Missing associated documentation comment in .proto file."""

    def load_image(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BackendServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'load_image': grpc.unary_unary_rpc_method_handler(
                    servicer.load_image,
                    request_deserializer=backend__pb2.img_path.FromString,
                    response_serializer=backend__pb2.image.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Backend', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Backend(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def load_image(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Backend/load_image',
            backend__pb2.img_path.SerializeToString,
            backend__pb2.image.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
