with open('app_recovered.js', 'r') as f:
    content = f.read()

start = content.find('/* PLAY & WIN GAME LOGIC */')
end = content.find('/* ==========================================================================\n   GLOBAL VARIABLES & STATE', start)

if start != -1 and end != -1:
    game_logic = content[start:end]
    print("Found game logic, length:", len(game_logic))
    with open('game_logic.js', 'w') as f:
        f.write(game_logic)
else:
    print("Could not find boundaries")
