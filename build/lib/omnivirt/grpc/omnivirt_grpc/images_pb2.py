# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: images.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cimages.proto\x12\x08omnivirt\x1a\x1bgoogle/protobuf/empty.proto\"{\n\x11ListImageResponse\x12\x37\n\x06result\x18\x01 \x03(\x0b\x32\'.omnivirt.ListImageResponse.ResultEntry\x1a-\n\x0bResultEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32S\n\x0bGrpcService\x12\x44\n\x0blist_images\x12\x16.google.protobuf.Empty\x1a\x1b.omnivirt.ListImageResponse\"\x00\x42\x03\x80\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'images_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\200\001\001'
  _LISTIMAGERESPONSE_RESULTENTRY._options = None
  _LISTIMAGERESPONSE_RESULTENTRY._serialized_options = b'8\001'
  _LISTIMAGERESPONSE._serialized_start=55
  _LISTIMAGERESPONSE._serialized_end=178
  _LISTIMAGERESPONSE_RESULTENTRY._serialized_start=133
  _LISTIMAGERESPONSE_RESULTENTRY._serialized_end=178
  _GRPCSERVICE._serialized_start=180
  _GRPCSERVICE._serialized_end=263
# @@protoc_insertion_point(module_scope)