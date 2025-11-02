import pygame
import random
import math
import asyncio
import sys   

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = BLACK

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 16)
    LARGE_FONT = pygame.font.SysFont('comicsans', 32)

    SIDE_PAD = 200
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor(
            (self.height - self.TOP_PAD) / (self.max_val - self.min_val + 1)
        )
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", True, draw_info.GREEN
    )
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 10))

    controls = draw_info.FONT.render(
        "R - Reset | SPACE - Start | A/D - Asc/Desc", True, draw_info.WHITE
    )
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 50))

    sorting = draw_info.FONT.render(
        "I-Insertion | B-Bubble | S-Selection | M-Merge | Q-Quick | L-Bogo", True, draw_info.WHITE
    )
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (
            draw_info.SIDE_PAD // 2,
            draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD,
        )
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]
        if i in color_positions:
            color = color_positions[i]
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def display_performance(draw_info, exec_time, memory_used_kb):
    text_time = draw_info.FONT.render(f"Time Taken: {exec_time:.2f} s", True, (255, 255, 255))
    text_mem = draw_info.FONT.render(f"Approx. Memory: {memory_used_kb:.1f} KB", True, (255, 255, 255))

    draw_info.window.blit(
        text_time, (draw_info.width / 2 - text_time.get_width() / 2, 110)
    )
    draw_info.window.blit(
        text_mem, (draw_info.width / 2 - text_mem.get_width() / 2, 135)
    )
    pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]

def approx_memory_kb_of_list(lst):
    try:
        total = sys.getsizeof(lst)
        for item in lst:
            total += sys.getsizeof(item)
        return total / 1024.0
    except Exception:
        return len(lst) * 8.0



# Sorting Algorithms 
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1, num2 = lst[j], lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i -= 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)):
        min_index = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                min_index = j
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            yield True
        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
        yield True
    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursive(lst, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        yield from merge_sort_recursive(lst, left, mid)
        yield from merge_sort_recursive(lst, mid + 1, right)
        yield from merge(lst, left, mid, right)

    def merge(lst, left, mid, right):
        left_part = lst[left:mid + 1]
        right_part = lst[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            if (left_part[i] <= right_part[j] and ascending) or (left_part[i] >= right_part[j] and not ascending):
                lst[k] = left_part[i]
                i += 1
            else:
                lst[k] = right_part[j]
                j += 1
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            yield True
            k += 1
        while i < len(left_part):
            lst[k] = left_part[i]
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            yield True
            i += 1
            k += 1
        while j < len(right_part):
            lst[k] = right_part[j]
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            yield True
            j += 1
            k += 1

    yield from merge_sort_recursive(lst, 0, len(lst) - 1)
    return lst

def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
        yield True
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            partition_gen = partition(low, high)
            while True:
                try:
                    yield next(partition_gen)
                except StopIteration as e:
                    pivot_index = e.value  
                    break 
            yield from quick_sort_recursive(low, pivot_index - 1)
            yield from quick_sort_recursive(pivot_index + 1, high)

    yield from quick_sort_recursive(0, len(lst) - 1)
    return lst



def bogo_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def is_sorted(lst):
        return all(
            (lst[i] <= lst[i + 1] if ascending else lst[i] >= lst[i + 1])
            for i in range(len(lst) - 1)
        )

    while not is_sorted(lst):
        random.shuffle(lst)
        draw_list(draw_info, {}, True)
        yield True
    return lst


async def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False
    ascending = True
    show_stats = False
    stats = None
    measuring = False

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    start_ticks = 0

    while run:
        clock.tick(60)
        await asyncio.sleep(0)  
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:  
                
                sorting = False
                if measuring:
                    end_ticks = pygame.time.get_ticks()
                    exec_time = (end_ticks - start_ticks) / 1000.0
                    mem_kb = approx_memory_kb_of_list(draw_info.lst)
                    stats = {"time": exec_time, "mem_kb": mem_kb}
                    show_stats = True
                    measuring = False

        draw(draw_info, sorting_algo_name, ascending)

        
        if show_stats and stats is not None:
            display_performance(draw_info, stats["time"], stats["mem_kb"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
                measuring = False
                show_stats = False
                stats = None

        
            elif event.key == pygame.K_SPACE and not sorting:
                show_stats = False
                stats = None
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                start_ticks = pygame.time.get_ticks()
                measuring = True

            
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_l and not sorting:
                sorting_algorithm = bogo_sort
                sorting_algo_name = "BogoSort"

    pygame.quit()



if __name__ == "__main__":
    asyncio.run(main())
