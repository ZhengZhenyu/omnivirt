# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: instances.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0finstances.proto\x12\x08omnivirt\";\n\x08Instance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x12\n\nip_address\x18\x03 \x01(\t\"\x16\n\x14ListInstancesRequest\">\n\x15ListInstancesResponse\x12%\n\tinstances\x18\x01 \x03(\x0b\x32\x12.omnivirt.Instance2b\n\x0bGrpcService\x12S\n\x0elist_instances\x12\x1e.omnivirt.ListInstancesRequest\x1a\x1f.omnivirt.ListInstancesResponse\"\x00\x42\x03\x80\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'instances_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\200\001\001'
  _INSTANCE._serialized_start=29
  _INSTANCE._serialized_end=88
  _LISTINSTANCESREQUEST._serialized_start=90
  _LISTINSTANCESREQUEST._serialized_end=112
  _LISTINSTANCESRESPONSE._serialized_start=114
  _LISTINSTANCESRESPONSE._serialized_end=176
  _GRPCSERVICE._serialized_start=178
  _GRPCSERVICE._serialized_end=276
# @@protoc_insertion_point(module_scope)
