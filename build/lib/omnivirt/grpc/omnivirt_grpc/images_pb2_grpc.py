# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from omnivirt.grpcs.omnivirt_grpc import images_pb2 as images__pb2


class GrpcServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list_images = channel.unary_unary(
                '/omnivirt.GrpcService/list_images',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=images__pb2.ListImageResponse.FromString,
                )


class GrpcServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def list_images(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GrpcServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'list_images': grpc.unary_unary_rpc_method_handler(
                    servicer.list_images,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=images__pb2.ListImageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'omnivirt.GrpcService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GrpcService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def list_images(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/omnivirt.GrpcService/list_images',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            images__pb2.ListImageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)