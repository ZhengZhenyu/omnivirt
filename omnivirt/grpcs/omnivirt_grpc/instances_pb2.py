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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0finstances.proto\x12\x08omnivirt\"M\n\x08Instance\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x10\n\x08vm_state\x18\x03 \x01(\t\x12\x12\n\nip_address\x18\x04 \x01(\t\"\x16\n\x14ListInstancesRequest\">\n\x15ListInstancesResponse\x12%\n\tinstances\x18\x01 \x03(\x0b\x32\x12.omnivirt.Instance\"4\n\x15\x43reateInstanceRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\"j\n\x16\x43reateInstanceResponse\x12\x0b\n\x03ret\x18\x01 \x01(\r\x12\x0b\n\x03msg\x18\x02 \x01(\t\x12)\n\x08instance\x18\x03 \x01(\x0b\x32\x12.omnivirt.InstanceH\x00\x88\x01\x01\x42\x0b\n\t_instance2\xc2\x01\n\x13InstanceGrpcService\x12S\n\x0elist_instances\x12\x1e.omnivirt.ListInstancesRequest\x1a\x1f.omnivirt.ListInstancesResponse\"\x00\x12V\n\x0f\x63reate_instance\x12\x1f.omnivirt.CreateInstanceRequest\x1a .omnivirt.CreateInstanceResponse\"\x00\x42\x03\x80\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'instances_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\200\001\001'
  _INSTANCE._serialized_start=29
  _INSTANCE._serialized_end=106
  _LISTINSTANCESREQUEST._serialized_start=108
  _LISTINSTANCESREQUEST._serialized_end=130
  _LISTINSTANCESRESPONSE._serialized_start=132
  _LISTINSTANCESRESPONSE._serialized_end=194
  _CREATEINSTANCEREQUEST._serialized_start=196
  _CREATEINSTANCEREQUEST._serialized_end=248
  _CREATEINSTANCERESPONSE._serialized_start=250
  _CREATEINSTANCERESPONSE._serialized_end=356
  _INSTANCEGRPCSERVICE._serialized_start=359
  _INSTANCEGRPCSERVICE._serialized_end=553
# @@protoc_insertion_point(module_scope)
