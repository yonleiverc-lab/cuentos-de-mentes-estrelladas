from components.entity import Entity
from components.sprite import Sprite
from components.player import Player
from components.physics import Body
from components.teleporter import Teleporter
from components.animator import Animator
from components.jump_trigger import JumpTrigger
from components.npc import NPC, NPCBehavior


entity_factories = [

#===================================
#--------------TABERNA--------------
#===================================
    # 0 - Jugador
    lambda args:Entity(Player(movement_speed=200), 
    Animator('assets/Character', scale_factor=1.0),
    Sprite("assets/Character/Idle/Front.png", base_scale=0.1, depth_scale=True),
    Body(50,50,16,16)),

    # 1 - Columna
    lambda args:Entity(Sprite("assets/Background/Tavern/tavern_colum.png", base_scale=0.3, depth_scale=True),
    Body(30,40,60,20)),

    # 2 - Barra
    lambda args: Entity(
    Sprite("assets/Background/Tavern/tavern_bar.png", base_scale=0.2, depth_scale=True), 
    Body(-240,-260,550,320)),

    # 3 - Mesa
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_table.png", base_scale=0.13, depth_scale=True),
    Body(-120,0,365,100)),

    # 4 - Piano
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_piano.png", base_scale=0.14, depth_scale=True),
    Body(-80,0,282,100)),

    # 5 - Silla 1
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_chair.png", base_scale=0.1, depth_scale=True),
    Body(40,0,30,60)),

    # 6 - Iluminación1
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_light1.png", base_scale=0.15, depth_scale=True, draw_order_override=961),
    Body()),

    # 7 - Iluminación2
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_light2.png", base_scale=0.18, depth_scale=True),
    Body()),

    # 8 - Iluminación3
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_light3.png", base_scale=0.35, depth_scale=True, draw_order_override=701),
    Body()),

    # 9 - Iluminación4
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_light4.png", base_scale=0.15, depth_scale=True, draw_order_override=1051),
    Body()),
    # 10 - Radio
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_radio.png", base_scale=0.13, depth_scale=True, draw_order_override=961),
    Body()),

    # 11 - Cerveza
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_beer.png", base_scale=0.1, depth_scale=True, draw_order_override=1051),
    Body()),

    # 12 - Cartel caza sombras
    lambda args: Entity(Sprite("assets/Background/Tavern/tavern_poster.png", base_scale=0.08, depth_scale=True, draw_order_override=601),
    Body()),

    # 13 Teletransportación a Villa
    lambda args: Entity(
        Teleporter(
            area_file=args[3],          # 1. Nombre del archivo (ej: 'village.map')
            x=int(args[4]),             # 2. Offset X de la colisión (ej: -20)
            y=int(args[5]),             # 3. Offset Y de la colisión (ej: 15)
            width=int(args[6]),         # 4. Ancho de la colisión (ej: 50)
            height=int(args[7])         # 5. Alto de la colisión (ej: 20)
        ), 
        Sprite("assets/Background/Tavern/tavern_door.png", base_scale=0.2, depth_scale=True)
    ),
    
    # 14 - Paredes de colisión genéricas
    lambda args: Entity(
        Body(
            int(args[3]) if len(args) > 3 else 0,    # offset x
            int(args[4]) if len(args) > 4 else 0,    # offset y
            int(args[5]) if len(args) > 5 else 50,   # width (default: 50)
            int(args[6]) if len(args) > 6 else 50    # height (default: 50)
        )
    ),

#===================================
#--------------VILLA--------------
#===================================

    # 15 - Jugador
    lambda args:Entity(Player(movement_speed=200),
    Animator('assets/Character', scale_factor=1.0), 
    Sprite("assets/Character/Idle/Front.png", base_scale=0.05, depth_scale=True),
    Body(50,50,16,16)),

    # 16 - Taberna
    lambda args: Entity(Sprite("assets/Background/Village/Village_Tavern/village_tavern.png", base_scale=0.32, depth_scale=True),
    Body()),

    # 17 Teletransportación a Taberna
    lambda args: Entity(
        Teleporter(
            area_file=args[3],          # 1. Nombre del archivo (ej: 'village.map')
            x=int(args[4]),             # 2. Offset X de la colisión (ej: -20)
            y=int(args[5]),             # 3. Offset Y de la colisión (ej: 15)
            width=int(args[6]),         # 4. Ancho de la colisión (ej: 50)
            height=int(args[7])         # 5. Alto de la colisión (ej: 20)
        ), 
        Sprite("assets/Background/Village/Village_Tavern/village_tavern_door.png", base_scale=0.12, depth_scale=True)
    ),
    # 18 - Taberna/Escaleras
    lambda args: Entity(Sprite("assets/Background/Village/Village_Tavern/village_tavern_stairs.png", base_scale=0.13, depth_scale=True),
    Body()),

     # 19 - Tienda
    lambda args: Entity(Sprite("assets/Background/Village/Village_Shop/village_shop.png", base_scale=0.5, depth_scale=True),
    Body()),

    # 20 Teletransportación a Tienda
    lambda args: Entity(
        Teleporter(
            area_file=args[3],          # 1. Nombre del archivo (ej: 'village.map')
            x=int(args[4]),             # 2. Offset X de la colisión (ej: -20)
            y=int(args[5]),             # 3. Offset Y de la colisión (ej: 15)
            width=int(args[6]),         # 4. Ancho de la colisión (ej: 50)
            height=int(args[7])         # 5. Alto de la colisión (ej: 20)
        ), 
        Sprite("assets/Background/Village/Village_Shop/village_shop_door.png", base_scale=0.08, depth_scale=True, draw_order_override=581)
    ),

    # 21 - Tienda/Escaleras
    lambda args: Entity(Sprite("assets/Background/Village/Village_Shop/village_shop_stairs.png", base_scale=0.13, depth_scale=True),
    Body()),

    # 22 - Estatua
    lambda args: Entity(Sprite("assets/Background/Village/village_statue.png", base_scale=0.15, depth_scale=True),
    Body()),

    # 23 - Casa del leñador
    lambda args: Entity(Sprite("assets/Background/Village/Lumber_House/lumber_house.png", base_scale=0.43, depth_scale=True),
    Body()),

    # 24 Teletransportación a Casa del Leñador
    lambda args: Entity(
        Teleporter(
            area_file=args[3],          # 1. Nombre del archivo (ej: 'village.map')
            x=int(args[4]),             # 2. Offset X de la colisión (ej: -20)
            y=int(args[5]),             # 3. Offset Y de la colisión (ej: 15)
            width=int(args[6]),         # 4. Ancho de la colisión (ej: 50)
            height=int(args[7])         # 5. Alto de la colisión (ej: 20)
        ), 
        Sprite("assets/Background/Village//Lumber_House/lumber_house_door.png", base_scale=0.07, depth_scale=True, draw_order_override=801)
    ),
     # 25 Teletransportación a el bosque
    lambda args: Entity(
        Teleporter(
            area_file=args[3],          # 1. Nombre del archivo (ej: 'village.map')
            x=int(args[4]),             # 2. Offset X de la colisión (ej: -20)
            y=int(args[5]),             # 3. Offset Y de la colisión (ej: 15)
            width=int(args[6]),         # 4. Ancho de la colisión (ej: 50)
            height=int(args[7])         # 5. Alto de la colisión (ej: 20)
        ), 
        Sprite("assets/Background/Village///forest_gate_door.png", base_scale=0.15, depth_scale=True, draw_order_override=0)
    ),

    #===================================
    #--------------FOREST--------------
    #===================================

     # 26 - Jugador
    lambda args:Entity(Player(movement_speed=200),
    Animator('assets/Character', scale_factor=1.0), 
    Sprite("assets/Character/Idle/Front.png", base_scale=0.05, depth_scale=True, draw_order_override=1002),
    Body(50,50,16,16)),
    # 27 - Bosque1
    lambda args: Entity(Sprite("assets/Background/Forest/forest_1.png", base_scale=0.23, depth_scale=True, draw_order_override=1001),
    Body(400, 600,)),
    # 28 - Bosque2
    lambda args: Entity(Sprite("assets/Background/Forest/forest_2.png", base_scale=0.23, depth_scale=True, draw_order_override=1001),
    Body(400, 600,)),
    # 29 - Colina1
    lambda args: Entity(Sprite("assets/Background/Forest/forest_hill1.png", base_scale=0.3, depth_scale=True),
    Body(1500, 600,)),
    # 30 - Colina2
    lambda args: Entity(Sprite("assets/Background/Forest/forest_hill2.png", base_scale=0.35, depth_scale=True),
    Body(1500, 600,)),
    # 31 - Piedra
    lambda args: Entity(Sprite("assets/Background/Forest/forest_rock.png", base_scale=0.1, depth_scale=True),
    Body(800, 500,)),
    # 32 - Tocón
    lambda args: Entity(Sprite("assets/Background/Forest/forest_stump.png", base_scale=0.1, depth_scale=True),
    Body(1200, 700,)),
    # 33 - Arbusto
    lambda args: Entity(Sprite("assets/Background/Forest/forest_bush.png", base_scale=0.1, depth_scale=True),
    Body(500, 900,)),
    # 34 - Flor
    lambda args: Entity(Sprite("assets/Background/Forest/forest_flower.png", base_scale=0.05, depth_scale=True),
    Body(1000, 850)),
    # 35 - Arbol antiguo
    lambda args: Entity(Sprite("assets/Background/Forest/ancien_tree.png", base_scale=0.2, depth_scale=True),
    Body(300, 400,)),


    # 36 Teletransportación a la villa
    lambda args: Entity(
        Teleporter(
            area_file=args[3],          # 1. Nombre del archivo (ej: 'village.map')
            x=int(args[4]),             # 2. Offset X de la colisión (ej: -20)
            y=int(args[5]),             # 3. Offset Y de la colisión (ej: 15)
            width=int(args[6]),         # 4. Ancho de la colisión (ej: 50)
            height=int(args[7])         # 5. Alto de la colisión (ej: 20)
        ), 
        Sprite("assets/Background/Forest///Village_gate_door.png", base_scale=0.07, depth_scale=True, draw_order_override=801)
    ),
    # 37 - Trigger de salto 1 (primer vacío del bosque)
    lambda args: Entity(
        JumpTrigger(
            destination_x=int(args[3]),  # X de destino
            destination_y=int(args[4]),  # Y de destino
            x=int(args[5]) if len(args) > 5 else -25,     # Offset X del trigger
            y=int(args[6]) if len(args) > 6 else -25,     # Offset Y del trigger
            width=int(args[7]) if len(args) > 7 else 50,  # Ancho del trigger
            height=int(args[8]) if len(args) > 8 else 50, # Alto del trigger
            prompt_text=args[9] if len(args) > 9 else "Presiona ESPACIO para saltar")
    ),

    # 38 - NPC Tabernero (ejemplo en taberna)
    lambda args: Entity(
        NPC(
            name="barman",
            dialogues=[
                ("barman", "¡Bienvenido a la taberna, jaime!"),
                ("barman", "Por aquí pasan muchos aventureros..."),
                ("barman", "¿Has oído sobre el caza sombras en el bosque?"),
                ("jaime", "No, cuéntame más sobre eso."),
                ("barman", "Dicen que aparece en las noches sin luna..."),   
                ("jaime", "Suena aterrador, tendré cuidado. Gracias por la advertencia."),
            ],
            interaction_distance=150
        ),
        NPCBehavior(behavior_type="look_at_player"),
        Sprite("assets/NPC/Barman/1.png", base_scale=0.1, depth_scale=True, draw_order_override=961),
        Body(50, 50, 30, 30)
    ),

    # 39 - NPC woman
    lambda args: Entity(
        NPC(
            name="mujer",
            dialogues=[
                ("Aldeano", "Hola, jaime."),
                ("Aldeano", "Ten cuidado en el bosque de noche."),
                ("jaime", "Gracias por el consejo."),
            ],
            interaction_distance=120
        ),
        NPCBehavior(behavior_type="idle"),  # Se queda quieto
        Sprite("assets/NPC/woman/1.png", base_scale=0.05, depth_scale=True),
        Body(50, 50, 30, 30)
    ),

    # 40 - Paredes de colisión genéricas
    lambda args: Entity(
        Body(
            int(args[3]) if len(args) > 3 else 0,    # offset x
            int(args[4]) if len(args) > 4 else 0,    # offset y
            int(args[5]) if len(args) > 5 else 50,   # width (default: 50)
            int(args[6]) if len(args) > 6 else 50    # height (default: 50)
        )
    ),
]


    
def create_entity(id,x,y,data=None):
     factory = entity_factories [id]
     e = factory(data)
     e.x = x
     e.y = y
     return e
     

