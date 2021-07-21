# 03. get_screen.py
# 게임 화면 가져오기
import retro

# 게임 환경 생성
env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
# 새 게임 시작
env.reset()

# 화면 가져오기
screen = env.get_screen()
ram = env.get_ram()

print(screen.shape[0], screen.shape[1])
print(screen)

print(ram.shape[0])
print(ram)

'''
hex = '0x075F'
hex_to_dec = int(hex, 16)
print(str(hex_to_dec))
print(ram[hex_to_dec])
'''

hex = '0x075F'
print(ram[hex])