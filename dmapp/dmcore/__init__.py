class ActiveDesktop:

	def __init__(self, desktops, unlabeled = "Other"):
		self.desktops = desktops


	def active_workspace():

	    workspaces = subprocess.check_output(["wmctrl", "-d"]) \
	                           .decode("utf-8").strip("\n").split("\n")

	    for workspace in workspaces:
	        if workspace[3] == "*":
	            return int(workspace[0])