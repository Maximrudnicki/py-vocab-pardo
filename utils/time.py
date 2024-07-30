from google.protobuf import timestamp_pb2

def convert_to_timestamp(dt):
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(dt)
    
    return timestamp