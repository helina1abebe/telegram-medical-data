select
  msg.message_id,
  msg.channel_id,
  d.date_id,
  msg.sent_at,
  msg.text,
  length(msg.text) as message_length,
  msg.has_image
from {{ ref('stg_telegram_messages') }} msg
join {{ ref('dim_dates') }} d
  on msg.sent_at::date = d.date
