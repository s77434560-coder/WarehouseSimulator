extends Node3D

@export var pallet_scene: PackedScene
@export var shelf_scene: PackedScene
@export var num_pallets: int = 15
@export var num_shelves: int = 5

func _ready():
	randomize()
	spawn_pallets()
	spawn_shelves()
	print("Spawned %d pallets and %d shelves" % [num_pallets, num_shelves])

func spawn_pallets():
	if not pallet_scene:
		print("Warning: No pallet scene assigned")
		return
	
	for i in range(num_pallets):
		var pallet = pallet_scene.instantiate()
		var x = randf_range(-8, 8)
		var z = randf_range(-5, 5)
		pallet.position = Vector3(x, 0.05, z)
		add_child(pallet)

func spawn_shelves():
	if not shelf_scene:
		print("Warning: No shelf scene assigned")
		return
	
	for i in range(num_shelves):
		var shelf = shelf_scene.instantiate()
		var x = randf_range(-7, 7)
		var z = randf_range(-4, 4)
		shelf.position = Vector3(x, 0.5, z)
		add_child(shelf)
