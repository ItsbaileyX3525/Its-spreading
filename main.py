from ursina import *
from ursina.prefabs.platformer_controller_2d import *
import random

class PlayerOne(PlatformerController2d):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = 'quad'
        self.texture = 'assets/playerone.png'
        self.double_sided=True
        self.scale_y=1
        self.scale_x=1
        self.scale=[self.scale_x/2,self.scale_y/2]
        self.z=-.1
        self.color=color.white
        self.jump_height = 2
        self.walk_speed = 4
        self.jump_duration = .25
        
    def input(self, key):
        if key == 'w':
            self.jump()

        if key == 'd':
            self.velocity = 1

        if key == 'd up':
            self.velocity = -held_keys['a']

        if key == 'a':
            self.velocity = -1
        if key == 'a up':
            self.velocity = held_keys['d']
            
    def update(self):
        if player2 != None:
            if boxcast(
                self.position+Vec3(self.velocity * time.dt * self.walk_speed,self.scale_y/2,0),
                direction=Vec3(self.velocity,0,0),
                distance=abs(self.scale_x/2),
                ignore=(self, player2),
                traverse_target=self.traverse_target,
                thickness=(self.scale_x*.9, self.scale_y*.9),
                ).hit == False:

                self.x += self.velocity * time.dt * self.walk_speed

            self.walking = held_keys['a'] + held_keys['d'] > 0 and self.grounded

            if not self.grounded:
                self.animator.state = 'jump'
            else:
                if self.walking:
                    self.animator.state = 'walk'
                else:
                    self.animator.state = 'idle'

            ray = boxcast(
                self.world_position+Vec3(0,.1,0),
                self.down,
                distance=max(.15, self.air_time * self.gravity),
                ignore=(self, player2),
                traverse_target=self.traverse_target,
                thickness=self.scale_x*.9,
                )

            if ray.hit:
                if not self.grounded:
                    self.land()
                self.grounded = True
                self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            if not self.grounded and not self.jumping:
                self.y -= min(self.air_time * self.gravity, ray.distance-.1)
                self.air_time += time.dt*4 * self.gravity


            if self.jumping:
                if boxcast(self.position+(0,.1,0), self.up, distance=self.scale_y, thickness=.95, ignore=(self,player2), traverse_target=self.traverse_target).hit:
                    self.y_animator.kill()
                    self.air_time = 0
                    self.start_fall()

class PlayerTwo(PlatformerController2d):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = 'quad'
        self.texture = 'assets/playertwo.png'
        self.color=None
        self.double_sided=True
        self.scale_y=1
        self.scale_x=1
        self.scale=[self.scale_x/2,self.scale_y/2]
        self.z=-.1
        self.jump_height = 2
        self.walk_speed = 4
        self.jump_duration = .25

    def input(self, key):
        if key == 'up arrow':
            self.jump()

        if key == 'right arrow':
            self.velocity = 1

        if key == 'right arrow up':
            self.velocity = -held_keys['left arrow']

        if key == 'left arrow':
            self.velocity = -1
        if key == 'left arrow up':
            self.velocity = held_keys['right arrow']

    def update(self):
        if player != None:
            if boxcast(
                self.position+Vec3(self.velocity * time.dt * self.walk_speed,self.scale_y/2,0),
                direction=Vec3(self.velocity,0,0),
                distance=abs(self.scale_x/2),
                ignore=(self, player, ),
                traverse_target=self.traverse_target,
                thickness=(self.scale_x*.9, self.scale_y*.9),
                ).hit == False:

                self.x += self.velocity * time.dt * self.walk_speed

            self.walking = held_keys['left arrow'] + held_keys['right arrow'] > 0 and self.grounded

            if not self.grounded:
                self.animator.state = 'jump'
            else:
                if self.walking:
                    self.animator.state = 'walk'
                else:
                    self.animator.state = 'idle'


            ray = boxcast(
                self.world_position+Vec3(0,.1,0),
                self.down,
                distance=max(.15, self.air_time * self.gravity),
                ignore=(self, player, ),
                traverse_target=self.traverse_target,
                thickness=self.scale_x*.9,
                )

            if ray.hit:
                if not self.grounded:
                    self.land()
                self.grounded = True
                self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            if not self.grounded and not self.jumping:
                self.y -= min(self.air_time * self.gravity, ray.distance-.1)
                self.air_time += time.dt*4 * self.gravity

            if self.jumping:
                if boxcast(self.position+(0,.1,0), self.up, distance=self.scale_y, thickness=.95, ignore=(self,player), traverse_target=self.traverse_target).hit:
                    self.y_animator.kill()
                    self.air_time = 0
                    self.start_fall()

class Platform(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.model='quad'
        self.color=color.black
        self.collider='box'
        
        
class platformshandler(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.currentY=5
        
    def update(self):
        for _ in range(random.randint(2,5)):
            e=Platform(x=random.uniform(-6,6), y=self.currentY, scale=[.6,.3])
        self.currentY+=1
        
class lava(Animation):
    def __init__(self, name='assets/AHHHHHH.gif', fps=12, loop=True, autoplay=True, frame_times=None, **kwargs):
        super().__init__(name, fps, loop, autoplay, frame_times, **kwargs)
        self.y=2
        self.scale_x=15
        self.scale_y=.5
        self.z=-1
        self.head = Entity(model='quad',color=color.black,y=self.y+.21,z=-1.1,scale_y=.1,scale_x=100,alpha=.0)
        
    def update(self):
        self.scale_y+=.5*time.dt
        self.head.y+=.25*time.dt
        if self.head.y >= player.y-.2 or self.head.y >= player2.y-.2:
            print("Game over fool")
            application.quit()
    

app=Ursina(title='Look out!',borderless=False,vsync=True)

ground=Entity(model='quad',color=color.gray,scale=[1000,1,1],y=3,collider='box')
invisBarrier = Entity(model="quad",x=-7,scale_y=30,alpha=0)
invisBarrier.collider=BoxCollider(entity=invisBarrier,size=(1.5,1,1))
invisBarrier = Entity(model="quad",x=7,scale_y=30,alpha=0)
invisBarrier.collider=BoxCollider(entity=invisBarrier,size=(1.5,1,1))

player=None
player2=None

player=PlayerOne(y=5)
player2=PlayerTwo(y=5,x=5)
spreadyBoi=lava()
platformshandler()
editMode = EditorCamera(enabled=False)
def input(key):
    if key=='l':
        editMode.enabled = not editMode.enabled   
camera.y=player.y
def update():
    avg = player.y + player2.y / 2
    camera.y = lerp(camera.y, avg, .5*time.dt)


app.run()