import pygame
import random
import math
import time

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Perguntas de Matemática")
font = pygame.font.Font(None, 30)
font_small = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

def wrap_text(text, font, max_width):
    """Enrola o texto em várias linhas para que se ajuste à largura máxima."""
    lines = []
    words = text.split(' ')
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    if current_line:
        lines.append(current_line)
    return lines

def generate_basic_question(level):
    """Gera uma questão de matemática básica de acordo com o nível."""
    range_max = 10 ** level
    question_type = random.choice(['addition', 'subtraction', 'multiplication', 'division'])
    
    if question_type == 'addition':
        a = random.randint(1, range_max)
        b = random.randint(1, range_max)
        question = f"Qual é a soma de {a} + {b}?\nFórmula: a + b"
        answer = a + b
    
    elif question_type == 'subtraction':
        a = random.randint(1, range_max)
        b = random.randint(1, a)  # Garantir que b <= a para não resultados negativos
        question = f"Qual é a diferença de {a} - {b}?\nFórmula: a - b"
        answer = a - b
    
    elif question_type == 'multiplication':
        a = random.randint(1, 10 + level)
        b = random.randint(1, 10 + level)
        question = f"Qual é o produto de {a} * {b}?\nFórmula: a * b"
        answer = a * b
    
    elif question_type == 'division':
        a = random.randint(1, range_max)
        b = random.randint(1, 10 + level)
        question = f"Qual é o quociente de {a} / {b}?\nFórmula: a / b"
        answer = round(a / b, 2)
    
    return question, answer

def generate_advanced_question(level):
    """Gera uma questão de matemática avançada de acordo com o nível."""
    question_type = random.choice(['quadratic', 'logarithmic', 'trigonometric', 'geometry', 'system'])
    
    if question_type == 'quadratic':
        a = random.randint(1, 5 + level)
        b = random.randint(-10 - level, 10 + level)
        c = random.randint(-10 - level, 10 + level)
        question = (f"Resolva a equação quadrática: {a}x² + {b}x + {c} = 0\n"
                    f"Fórmula: x = (-b ± √(b² - 4ac)) / 2a")
        discriminant = b**2 - 4*a*c
        if discriminant < 0:
            answer = "Não há solução real"
        else:
            root1 = (-b + math.sqrt(discriminant)) / (2*a)
            root2 = (-b - math.sqrt(discriminant)) / (2*a)
            answer = f"{root1:.2f} e {root2:.2f}"
    
    elif question_type == 'logarithmic':
        base = random.choice([2, 10])
        number = random.randint(1, 10**level)
        question = (f"Resolva para x: log_{base}({number})\n"
                    f"Fórmula: x = log_{base}({number})")
        answer = f"{math.log(number, base):.2f}"
    
    elif question_type == 'trigonometric':
        angle = random.choice([30, 45, 60, 90])
        question = (f"Resolva para sin({angle})\n"
                    f"Fórmula: sin({angle}) = {math.sin(math.radians(angle)):.2f}")
        answer = f"{math.sin(math.radians(angle)):.2f}"
    
    elif question_type == 'geometry':
        a = random.randint(1, 10 + level)
        b = random.randint(1, 10 + level)
        question = (f"Calcule a área de um triângulo retângulo com base {a} e altura {b}\n"
                    f"Fórmula: Área = 0,5 * base * altura")
        answer = f"{0.5 * a * b:.2f}"
    
    elif question_type == 'system':
        a1, b1, c1 = random.randint(1, 5 + level), random.randint(-5 - level, 5 + level), random.randint(-10 - level, 10 + level)
        a2, b2, c2 = random.randint(1, 5 + level), random.randint(-5 - level, 5 + level), random.randint(-10 - level, 10 + level)
        question = (f"Resolva o sistema de equações:\n"
                    f"{a1}x + {b1}y = {c1}\n"
                    f"{a2}x + {b2}y = {c2}\n"
                    f"Fórmula: x = (c1*b2 - c2*b1) / (a1*b2 - a2*b1)\n"
                    f"          y = (a1*c2 - a2*c1) / (a1*b2 - a2*b1)")
        # Solução pelo método da eliminação
        det = a1 * b2 - a2 * b1
        if det == 0:
            answer = "Não há solução única"
        else:
            x = (c1 * b2 - c2 * b1) / det
            y = (a1 * c2 - a2 * c1) / det
            answer = f"x = {x:.2f}, y = {y:.2f}"
    
    return question, answer

def generate_question(level):
    """Gera uma questão de matemática aleatória (básica ou avançada) de acordo com o nível."""
    if random.choice([True, False]):
        return generate_basic_question(level)
    else:
        return generate_advanced_question(level)

def display_message(text, color, y_offset, is_small=False):
    """Exibe uma mensagem na tela."""
    current_font = font_small if is_small else font
    lines = wrap_text(text, current_font, SCREEN_WIDTH - 40)
    for i, line in enumerate(lines):
        text_surface = current_font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset + i * 30))
        screen.blit(text_surface, text_rect)

def main():
    level = 1
    score = 0
    max_level = 10
    total_questions = 100
    question_number = 0
    input_text = ''
    current_question = ''
    current_answer = ''
    question_asked = False

    while True:
        screen.fill(BLACK)

        if not question_asked:
            current_question, current_answer = generate_question(level)
            question_number += 1

            if question_number >= total_questions:
                question_number = 0
                if level < max_level:
                    level += 1
                display_message(f"Parabéns! Você avançou para o nível {level}.", WHITE, -50)
                pygame.display.flip()
                time.sleep(2)

            question_asked = True

        # Processa eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        user_answer = input_text.strip()
                        # Verifica a resposta
                        if user_answer.lower() in ["não há solução real", "não há solução única"]:
                            if user_answer.lower() == current_answer.lower():
                                score += 10
                                display_message("Correto! +10 Pontos", WHITE, -50)
                            else:
                                display_message("Incorreto. Tente novamente!", RED, -50)
                                if level > 1:
                                    level -= 1
                        else:
                            if float(user_answer) == float(current_answer):
                                score += 10
                                display_message("Correto! +10 Pontos", WHITE, -50)
                            else:
                                display_message("Incorreto. Tente novamente!", RED, -50)
                                if level > 1:
                                    level -= 1
                    except ValueError:
                        display_message("Resposta inválida. Tente novamente!", RED, -50)

                    input_text = ''
                    question_asked = False

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                elif event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                                   pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    input_text += event.unicode
                elif event.key == pygame.K_PERIOD:
                    input_text += '.'

        # Exibe a questão
        display_message(current_question, WHITE, -100)
        display_message(f"Resposta: {input_text}", WHITE, 50, is_small=True)
        display_message(f"Pontos: {score}", WHITE, 100, is_small=True)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
