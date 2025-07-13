select distinct
  channel_id,
  'Hardcoded name for now' as channel_name  -- replace if you have actual metadata
from {{ ref('stg_telegram_messages') }}
where channel_id is not null
  and channel_id != ''
  and channel_id != '0'
  and channel_id != 'null'
  and channel_id != 'None'
  and channel_id != 'undefined'
  and channel_id != '[]'
  and channel_id != '{}'
  and channel_id != '""'
  and channel_id != 'false'
  and channel_id != 'True'
  and channel_id != 'False';    