SELECT * FROM {{ ref('stg_telegram_messages') }}
WHERE text IS NULL OR length(trim(text)) = 0
