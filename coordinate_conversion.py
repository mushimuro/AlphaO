def convert_coordinate_format(x,y):
    # 보드판은 1-15, 1-15 까지 받고 있을거임 (코드상 좌표 0,0 이 실제에선 1,1 이 나타나는점 고려)
    # 일반적으로 보드에서 가로가 A-P로 나타나긴 하는데 (좌표를 A,1 방식으로 받으면 )
    new_y = 3-y  # 15-y
    new_x = x-1  # x-1
    return new_y,new_x

# ascii value changing
def convert_alphabet_to_num(alphabet):
    return ord(alphabet) - 64