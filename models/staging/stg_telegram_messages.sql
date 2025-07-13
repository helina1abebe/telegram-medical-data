with raw as (
  select 
    message_json ->> 'id' as message_id,
    message_json ->> 'message' as text,
    message_json ->> 'date' as sent_at,
    message_json -> 'media' is not null as has_image,
    message_json ->> 'peer_id' as channel_id
  from raw.telegram_messages
)
select 
  cast(message_id as bigint) as message_id,
  cast(channel_id as text) as channel_id,
  cast(sent_at as timestamp) as sent_at,
  text,
  has_image
from raw
