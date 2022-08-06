SELECT
    user.first_name ||' '|| user.last_name as full_name,
    user.id user_id,
    game.*
FROM levelupapi_game game
JOIN auth_user user
ON user.id = game.gamer_id