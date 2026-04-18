import pygame, sys, random

pygame.init()
W, H = 480, 300
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Jump!")
font = pygame.font.SysFont("msgothic,yugothic,ipagothic,applegothic", 28)
clk   = pygame.time.Clock()

# ===== 設定 =====
GY       = 0.5   # 重力
JUMP     = -12   # ジャンプ力
GROUND   = H - 60
SPEED    = 5     # 山の速さ

# ===== 状態 =====
py, vy   = GROUND, 0   # プレイヤーY座標・速度
on_ground = True
mountains = []
score    = 0
frame    = 0
state    = "play"

def new_mountain():
    h = random.randint(30, 80)
    return {"x": W, "h": h}

mountains.append(new_mountain())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == "play" and on_ground:
                    vy = JUMP; on_ground = False
                elif state == "over":
                    py, vy, on_ground = GROUND, 0, True
                    mountains = [new_mountain()]
                    score, frame = 0, 0
                    state = "play"

    if state == "play":
        frame += 1
        score += 1

        # 重力・ジャンプ
        vy += GY
        py += vy
        if py >= GROUND:
            py, vy, on_ground = GROUND, 0, True

        # 山を動かす
        for m in mountains:
            m["x"] -= SPEED + score // 200  # 徐々に加速

        # 画面外の山を消す
        mountains = [m for m in mountains if m["x"] > -60]

        # 山を追加（間隔ランダム）
        if frame % random.randint(60, 120) == 0:
            mountains.append(new_mountain())

        # 当たり判定
        px1, px2 = 60, 90   # プレイヤーのX範囲
        for m in mountains:
            mx1, mx2 = m["x"], m["x"] + 40
            my_top   = GROUND - m["h"] + 60
            if px2 > mx1 and px1 < mx2 and py + 40 > my_top:
                state = "over"

    # ===== 描画 =====
    screen.fill((30, 30, 50))

    # 地面
    pygame.draw.rect(screen, (80, 120, 60), (0, GROUND + 40, W, 60))

    # 山（三角形）
    for m in mountains:
        bx, bw, bh = m["x"], 40, m["h"]
        base_y = GROUND + 40
        pygame.draw.polygon(screen, (100, 160, 100), [
            (bx + bw // 2, base_y - bh),  # 頂点
            (bx,           base_y),        # 左下
            (bx + bw,      base_y),        # 右下
        ])

    # プレイヤー（丸）
    pygame.draw.circle(screen, (255, 107, 107), (70, int(py) + 20), 20)

    # スコア
    screen.blit(font.render(f"スコア: {score}", True, (255,255,255)), (10, 10))

    # ゲームオーバー
    if state == "over":
        screen.blit(font.render("ゲームオーバー！", True, (255,220,50)), (160, 110))
        screen.blit(font.render("スペースでリスタート", True, (255,220,50)), (140, 145))

    pygame.display.flip()
    clk.tick(60)