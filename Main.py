import requests
import json
import datetime

# 🔹 設定（自分の情報を入れる）
STEAM_API_KEY = "YOUR_STEAM_API_KEY"  # ここにSteam APIキーを入れる
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"  # DiscordのWebhook URLを入れる

# 🔹 1ヶ月以内にリリースされたゲームを取得する関数
def get_new_released_games():
    url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    all_games = response.json()["applist"]["apps"]
    
    # 1ヶ月以内のゲームをフィルタリング（※この方法はSteamAPIではなくスクレイピングが必要になるかも）
    recent_games = []  # 仮で空のリスト（ここは後で改善する必要あり）
    return recent_games

# 🔹 SteamDBからプレイヤー数を取得
def get_player_count(appid):
    url = f"https://steamdb.info/api/GetCurrentPlayers/?appid={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("player_count", 0)
    return 0

# 🔹 上位5ゲームをランキングする
def get_top_games():
    new_games = get_new_released_games()
    game_stats = []
    
    for game in new_games:
        player_count = get_player_count(game["appid"])
        game_stats.append({"name": game["name"], "players": player_count})
    
    # プレイヤー数が多い順に並べる
    top_games = sorted(game_stats, key=lambda x: x["players"], reverse=True)[:5]
    return top_games

# 🔹 Discordに送信
def send_to_discord():
    top_games = get_top_games()
    message = "🎮 **最近発売された人気ゲームランキング** 🎮\n"
    for i, game in enumerate(top_games, 1):
        message += f"**{i}. {game['name']}** - {game['players']} 人プレイ中\n"
    
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers={"Content-Type": "application/json"})

# 🔹 実行
if __name__ == "__main__":
    send_to_discord()
