extends CharacterBody3D

# Movement parameters
@export var speed: float = 3.0
@export var turn_speed: float = 1.5
@export var raycast_length: float = 2.0

# Data export
@export var is_exporting: bool = false
var export_data: Array = []
var frame_counter: int = 0

# References
@onready var camera = $Camera3D
@onready var raycast = $RayCast3D

func _ready():
	raycast.target_position = Vector3(0, 0, -raycast_length)
	print("Forklift ready - Use WASD to move, E to export data")

func _physics_process(delta):
	# Get input
	var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	# Movement
	if direction:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)
	
	move_and_slide()
	
	# Rotation
	if input_dir.x != 0:
		rotate_y(input_dir.x * turn_speed * delta)
	
	# Export data if active
	if is_exporting:
		export_current_state()
		frame_counter += 1
		
		# Auto-stop after 500 frames (keeps file size manageable)
		if frame_counter >= 500:
			stop_export()

func export_current_state():
	var state = {
		"frame": frame_counter,
		"timestamp": Time.get_ticks_msec(),
		"position": [position.x, position.y, position.z],
		"rotation": [rotation.x, rotation.y, rotation.z],
		"velocity": [velocity.x, velocity.y, velocity.z],
		"raycast_hit": raycast.is_colliding(),
		"is_moving": velocity.length() > 0.1
	}
	export_data.append(state)
	
	# Save every 100 frames
	if export_data.size() >= 100:
		save_export_data()

func save_export_data():
	var file_path = "user://simulation_data_%d.json" % Time.get_unix_time_from_system()
	var file = FileAccess.open(file_path, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(export_data, "\t"))
		file.close()
		print("Saved %d frames to %s" % [export_data.size(), file_path])
		export_data.clear()
	else:
		print("Error: Could not save export data")

func start_export():
	is_exporting = true
	frame_counter = 0
	export_data.clear()
	print("Started data export - Recording frames...")

func stop_export():
	is_exporting = false
	print("Stopped data export. Total frames: %d" % frame_counter)

func _input(event):
	if event.is_action_pressed("export_data"):
		if is_exporting:
			stop_export()
		else:
			start_export()
	elif event.is_action_pressed("reset"):
		position = Vector3(0, 0.5, 0)
		velocity = Vector3.ZERO
		print("Robot position reset")
