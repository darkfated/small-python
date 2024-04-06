import matplotlib.pyplot as plt
import numpy as np


def can_place_item(inventory, item, start_row, start_col):
    """ Проверяет, можно ли разместить элемент в инвентаре, начиная с позиции (start_row, start_col) """
    for x, y in item:
        # Проверяем, не выходит ли элемент за границы инвентаря и свободно ли место
        if start_row + y >= len(inventory) or start_col + x >= len(inventory[0]) or inventory[start_row + y][
            start_col + x] != 0:
            return False
    return True


def place_item(inventory, item, start_row, start_col, item_id):
    """ Размещает элемент в инвентаре, начиная с позиции (start_row, start_col), с уникальным идентификатором для цвета """
    for x, y in item:
        inventory[start_row + y][start_col + x] = item_id
    return inventory


inventory_size = (8, 5)
existing_items = [{'test1': [[0, 0], [1, 0], [0, 1], [2, 0]]}]
next_items = [
    {'test2': [[0, 0], [0, 1], [1, 1]]},
    {'test3': [[0, 0], [0, 1], [1, 0]]}
]

# Создаем матрицу инвентаря, заполненную нулями
inventory_matrix = np.zeros((inventory_size[0], inventory_size[1]))

# Заполняем инвентарь существующими предметами
item_id = 1  # Начинаем с 1, так как 0 - это пустое место
for item in existing_items:
    for item_name, pixels in item.items():
        inventory_matrix = place_item(inventory_matrix, pixels, 0, 0, item_id)
        item_id += 1

# Пытаемся разместить каждый предмет из next_items в инвентаре
for item in next_items:
    for item_name, pixels in item.items():
        item_placed = False
        for row in range(inventory_size[0]):
            for col in range(inventory_size[1]):
                if can_place_item(inventory_matrix, pixels, row, col):
                    inventory_matrix = place_item(inventory_matrix, pixels, row, col, item_id)
                    item_placed = True
                    break
            if item_placed:
                break
        if item_placed:  # Увеличиваем item_id только если предмет был размещен
            item_id += 1


def draw_inventory():
    def draw_grid(ax, inventory_size, data_size):
        # Рисуем сетку
        for x in range(data_size[1] + 1):
            ax.axvline(x - 0.5, lw=2, color='black', zorder=5)
        for y in range(data_size[0] + 1):
            ax.axhline(y - 0.5, lw=2, color='black', zorder=5)
        # Рисуем границу инвентаря
        ax.add_patch(
            plt.Rectangle((-0.5, -0.5), inventory_size[1], inventory_size[0], fill=None, edgecolor='black', lw=3,
                          zorder=10))

    # Определяем размер данных
    data_size = (len(inventory_matrix), len(inventory_matrix[0]))
    fig, ax = plt.subplots(figsize=(10, 6))
    # Рисуем инвентарь с использованием colormap 'tab20' для различения цветов предметов
    cmap = plt.cm.get_cmap('tab20', item_id)  # генерируем colormap с нужным количеством цветов
    ax.imshow(inventory_matrix, cmap=cmap, interpolation='nearest', zorder=0)
    ax.axis('off')
    draw_grid(ax, inventory_size, data_size)
    ax.set_xlim(-0.5, inventory_size[1] - 0.5)
    ax.set_ylim(inventory_size[0] - 0.5, -0.5)
    ax.set_title('Инвентарь с объектами и сеткой')
    plt.show()


draw_inventory()
