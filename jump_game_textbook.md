# ジャンプゲームを作ろう！

## 目標

スペースキーでジャンプして、山をよけるゲームを作ります。

---

## 画面イメージ

![ゲーム画面](image.png)

- **プレイヤー**：赤い丸
- **山**：緑色の三角
- 山にぶつかるとゲームオーバー！

---

## 遊び方

| キー | 動作 |
|:----:|:-----|
| スペース | ジャンプ |
| スペース | リスタート（ゲームオーバー時） |

---

## 準備

ゲームを動かす前に、コマンドプロンプトで次を実行してください。

```
pip install pygame
```

---

## プログラム

```python
   1: import pygame, sys, random
   2:
   3: pygame.init()
   4: W, H = 480, 300
   5: screen = pygame.display.set_mode((W, H))
   6: pygame.display.set_caption("Jump!")
   7: font = pygame.font.SysFont("msgothic,yugothic,ipagothic,applegothic", 28)
   8: clk   = pygame.time.Clock()
   9:
  10: # ===== 設定 =====
  11: GY       = 0.5   # 重力
  12: JUMP     = -12   # ジャンプ力
  13: GROUND   = H - 60
  14: SPEED    = 5     # 山の速さ
  15:
  16: # ===== 状態 =====
  17: py, vy   = GROUND, 0   # プレイヤーY座標・速度
  18: on_ground = True
  19: mountains = []
  20: score    = 0
  21: frame    = 0
  22: state    = "play"
  23:
  24: def new_mountain():
  25:     h = random.randint(30, 80)
  26:     return {"x": W, "h": h}
  27:
  28: mountains.append(new_mountain())
  29:
  30: while True:
  31:     for event in pygame.event.get():
  32:         if event.type == pygame.QUIT:
  33:             pygame.quit(); sys.exit()
  34:         if event.type == pygame.KEYDOWN:
  35:             if event.key == pygame.K_SPACE:
  36:                 if state == "play" and on_ground:
  37:                     vy = JUMP; on_ground = False
  38:                 elif state == "over":
  39:                     py, vy, on_ground = GROUND, 0, True
  40:                     mountains = [new_mountain()]
  41:                     score, frame = 0, 0
  42:                     state = "play"
  43:
  44:     if state == "play":
  45:         frame += 1
  46:         score += 1
  47:
  48:         # 重力・ジャンプ
  49:         vy += GY
  50:         py += vy
  51:         if py >= GROUND:
  52:             py, vy, on_ground = GROUND, 0, True
  53:
  54:         # 山を動かす
  55:         for m in mountains:
  56:             m["x"] -= SPEED + score // 200  # 徐々に加速
  57:
  58:         # 画面外の山を消す
  59:         mountains = [m for m in mountains if m["x"] > -60]
  60:
  61:         # 山を追加（間隔ランダム）
  62:         if frame % random.randint(60, 120) == 0:
  63:             mountains.append(new_mountain())
  64:
  65:         # 当たり判定
  66:         px1, px2 = 60, 90   # プレイヤーのX範囲
  67:         for m in mountains:
  68:             mx1, mx2 = m["x"], m["x"] + 40
  69:             my_top   = GROUND - m["h"] + 60
  70:             if px2 > mx1 and px1 < mx2 and py + 40 > my_top:
  71:                 state = "over"
  72:
  73:     # ===== 描画 =====
  74:     screen.fill((30, 30, 50))
  75:
  76:     # 地面
  77:     pygame.draw.rect(screen, (80, 120, 60), (0, GROUND + 40, W, 60))
  78:
  79:     # 山（三角形）
  80:     for m in mountains:
  81:         bx, bw, bh = m["x"], 40, m["h"]
  82:         base_y = GROUND + 40
  83:         pygame.draw.polygon(screen, (100, 160, 100), [
  84:             (bx + bw // 2, base_y - bh),  # 頂点
  85:             (bx,           base_y),        # 左下
  86:             (bx + bw,      base_y),        # 右下
  87:         ])
  88:
  89:     # プレイヤー（丸）
  90:     pygame.draw.circle(screen, (255, 107, 107), (70, int(py) + 20), 20)
  91:
  92:     # スコア
  93:     screen.blit(font.render(f"スコア: {score}", True, (255,255,255)), (10, 10))
  94:
  95:     # ゲームオーバー
  96:     if state == "over":
  97:         screen.blit(font.render("ゲームオーバー！", True, (255,220,50)), (160, 110))
  98:         screen.blit(font.render("スペースでリスタート", True, (255,220,50)), (140, 145))
  99:
 100:     pygame.display.flip()
 101:     clk.tick(60)
```

---

## 打ち込みの注意

| 注意 | 説明 |
|:-----|:-----|
| **スペース（空白）** | 行の始めのスペースは **半角スペース4つ** でそろえる |
| **全角・半角** | 英語・数字・記号は **半角** で入力する |
| **大文字・小文字** | `True` `False` `QUIT` など、大文字と小文字を間違えない |
| **カッコの形** | `( )` `[ ]` `{ }` を間違えない |
| **コロンを忘れずに** | `if` `for` `def` `while` の行の最後は `:` |

---

## 実行方法

ファイルを `jump_game.py` という名前で保存して、次のコマンドで実行します。

```
python jump_game.py
```

---

がんばって打ち込んでみよう！
