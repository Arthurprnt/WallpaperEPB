import datetime, pygame, threading, socket, urllib.request, json
from btpygame import pygameimage, pygamebutton, collide, showtext

ping = 36000
response = urllib.request.urlopen(f"https://api4.my-ip.io/ip.json")
data_json = json.loads(response.read())
ip = data_json["ip"]
response = urllib.request.urlopen(f"http://ip-api.com/json/{ip}")
data_json = json.loads(response.read())
lat = data_json["lat"]
lon = data_json["lon"]
response = urllib.request.urlopen(f"https://api.open-meteo.com/v1/meteofrance?latitude={lat}&longitude={lon}&hourly=temperature_2m")
data_json = json.loads(response.read())
temperature = data_json["hourly"]["temperature_2m"][-1]

circle_liste = []

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption('Wallpaper')
clock = pygame.time.Clock()
running = True

screen_x, screen_y = screen.get_size()
background = pygameimage(pygame.transform.scale(pygame.image.load("assets/wallpaper.jpg"), (screen_x, screen_y)), (0, 0))

while running:

    current_time = datetime.datetime.now()
    day = datetime.datetime.now().strftime('%A')
    if ping == 0:
        ping = 36000
        response = urllib.request.urlopen(f"https://api4.my-ip.io/ip.json")
        data_json = json.loads(response.read())
        ip = data_json["ip"]
        response = urllib.request.urlopen(f"http://ip-api.com/json/{ip}")
        data_json = json.loads(response.read())
        lat = data_json["lat"]
        lon = data_json["lon"]
        response = urllib.request.urlopen(f"https://api.open-meteo.com/v1/meteofrance?latitude={lat}&longitude={lon}&hourly=temperature_2m")
        data_json = json.loads(response.read())
        temperature = data_json["hourly"]["temperature_2m"][-1]

    screen.blit(background.image, background.pos)

    circlesize = 10
    mousecoord = pygame.mouse.get_pos()
    circle_liste = [(mousecoord[0], mousecoord[1])] + circle_liste
    if len(circle_liste) > circlesize:
        circle_liste.pop(-1)
    surface = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
    for i in range(len(circle_liste)):
        pygame.draw.circle(surface, (255, 255, 255, 128), circle_liste[i], circlesize, 0)
        if i < len(circle_liste)-1:
            pygame.draw.circle(surface, (255, 255, 255, 128), ((circle_liste[i][0]+circle_liste[i+1][0])/2, (circle_liste[i][1]+circle_liste[i+1][1])/2), circlesize-0.5, 0)
        if i < len(circle_liste)-2:
            pygame.draw.circle(surface, (255, 255, 255, 128), ((circle_liste[i][0]+circle_liste[i+1][0]+circle_liste[i+2][0])/3, (circle_liste[i][1]+circle_liste[i+1][1]+circle_liste[i+2][1])/3), circlesize-0.33, 0)
        if i < len(circle_liste)-3:
            pygame.draw.circle(surface, (255, 255, 255, 128), ((circle_liste[i][0]+circle_liste[i+1][0]+circle_liste[i+2][0]+circle_liste[i+3][0])/4, (circle_liste[i][1]+circle_liste[i+1][1]+circle_liste[i+2][1]+circle_liste[i+3][1])/4), circlesize-0.25, 0)
        circlesize -= 1
    screen.blit(surface, (0, 0))

    hour = current_time.hour
    minute = current_time.minute
    if len(str(hour)) == 1:
        hour = f"0{hour}"
    if len(str(minute)) == 1:
        minute = f"0{minute}"
    timeshowed = f"{hour}:{minute}"
    if timeshowed == "18:30":
        timeshowed = "18:29"
    showtext(screen, timeshowed, "assets/ARIBL0.ttf", 90, (screen_x//2, screen_y//4.7-5), (255, 255, 255), "center")
    showtext(screen, f"{day[:3]} {current_time.day} {datetime.datetime.now().strftime('%B')}", "assets/ARIBL0.ttf", 30, (screen_x//2, screen_y//4.7+55), (255, 255, 255), "center")
    showtext(screen, f"{temperature}°C", "assets/ARIBL0.ttf", 27, (screen_x//2, screen_y//4.7+102), (255, 255, 255), "center")
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screen_x//2-200/2, screen_y//4.7+81, 200, 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ping -= 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()