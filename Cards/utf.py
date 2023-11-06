suits = ['\u2665', '\u2666', '\u2663', '\u2660']  # Hearts, Diamonds, Clubs, Spades in Unicode
ranks = ['\u0032', '\u0033', '\u0034', '\u0035', '\u0036', '\u0037', '\u0038', '\u0039', '\u0031\u0030', '\u004A', '\u0051', '\u004B', '\u0041']  # 2-10, J, Q, K, A in Unicode

for suit in suits:
    for rank in ranks:
        print(f'{rank} of {suit}')

for i in range(0xA0, 0xFF+1):
    card = chr(0x1F000 + i)
    print(card)