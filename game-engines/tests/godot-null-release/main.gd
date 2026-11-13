extends Node

func untyped_call():
	var u = null
	u.foo()
	print("UNTYPED: line after error ran")

func typed_call():
	var n: Node = null
	n.get_name()
	print("TYPED: line after error ran")

func prop_access():
	var n: Node = null
	var x = n.name
	print("PROP: line after error ran, x=", x)

func _ready():
	var args = OS.get_cmdline_user_args()
	var which = args[0] if args.size() > 0 else "all"
	print("START ", which)
	if which == "untyped" or which == "all":
		untyped_call()
		print("after untyped_call")
	if which == "typed" or which == "all":
		typed_call()
		print("after typed_call")
	if which == "prop" or which == "all":
		prop_access()
		print("after prop_access")
	await get_tree().create_timer(0.5).timeout
	print("END: game still running after 0.5 s")
	get_tree().quit()
