SELECT
    u.first_name ||' '|| u.last_name as full_name,
    e.description,
    g.title,
    e.date,
    e.time,
    u.id as user_id
FROM levelupapi_event_attendees a
JOIN auth_user u
ON u.id = a.gamer_id
JOIN levelupapi_event e
ON a.event_id = e.id
JOIN levelupapi_game g
ON e.game_id = g.id