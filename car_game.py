import pygame
from pygame.locals import *
import random

pygame.init()

# ფანჯრის შექმნა
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# ფერები
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# გზის და მარკერის ზომები
road_width = 300
marker_width = 10
marker_height = 50

# ზოლის კოორდინატები
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# გზის და კიდეების მარკერები
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# ზოლის მარკერების მოძრაობის ანიმაციისთვის
lane_marker_move_y = 0

# მოთამაშის საწყისი კოორდინატები
player_x = 250
player_y = 400

# ჩარჩოს პარამეტრები
clock = pygame.time.Clock()
fps = 120

# თამაშის პარამეტრები
gameover = False
speed = 2
score = 0

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # შეამცირეთ სურათი ისე, რომ არ იყოს უფრო ფართო ვიდრე ზოლი
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('car.png')
        super().__init__(image, x, y)
        
# sprite ჯგუფები
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# შექმენით მოთამაშის მანქანა
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# ჩატვირთეთ მანქანის სურათები
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load(image_filename)
    vehicle_images.append(image)
    
# ჩატვირთეთ ავარიის სურათი
crash = pygame.image.load('crash.png')
crash_rect = crash.get_rect()

# თამაშის მარყუჟი
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # გადაიტანეთ მოთამაშის მანქანა მარცხენა და მარჯვენა ისრიანი ღილაკების გამოყენებით
        if event.type == KEYDOWN:
            
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # შეამოწმეთ არის თუ არა გვერდითი დარტყმის შეჯახება ზოლის შეცვლის შემდეგ
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    
                    gameover = True
                    
                    # მოათავსეთ მოთამაშის მანქანა სხვა მანქანის გვერდით
                    # და განსაზღვრეთ სად უნდა განთავსდეს ავარიის სურათი
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
            
    # დახატე ბალახი
    screen.fill(green)
    
    # დახაზეთ გზა
    pygame.draw.rect(screen, gray, road)
    
    # დახაზეთ კიდეების მარკერები
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    
    # დახაზეთ ზოლის მარკერები
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    # დახატეთ მოთამაშის მანქანა
    player_group.draw(screen)
    
    # მანქანის დამატება
    if len(vehicle_group) < 2:
        
        # უზრუნველყოს საკმარისი უფსკრული მანქანებს შორის
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            
            # აირჩიეთ შემთხვევითი ზოლი
            lane = random.choice(lanes)
            
            # აირჩიეთ მანქანის შემთხვევითი სურათი
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # მანქანების მოძრაობა
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # ამოიღეთ მანქანა ეკრანიდან გასვლის შემდეგ
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # ქულის დამატება
            score += 1
            
            # დააჩქარეთ თამაში 5 მანქანის გავლის შემდეგ
            if score > 0 and score % 5 == 0:
                speed += 1
    
    # დახაზეთ მანქანები
    vehicle_group.draw(screen)
    
    # ქულების ჩვენება
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    
    # შეამოწმეთ არის თუ არა თავი შეჯახებისას
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
            
    # თამაშის ჩვენება დასრულდა
    if gameover:
        screen.blit(crash, crash_rect)
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
            
    pygame.display.update()

    # დაელოდეთ მომხმარებლის შეყვანის ხელახლა დაკვრას ან გასვლას
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # მიიღეთ მომხმარებლის შეყვანა (y ან n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # თამაშის გადატვირთვა
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # მარყუჟებიდან გასვლა
                    gameover = False
                    running = False

pygame.quit()