import sys
import os
import shutil
from oneline import ol
class Runtime(object):
	def __init__(self, args):
		self.args = args
		self.type = 'SERVER'
		self.port = 9000 
		self.ip = "127.0.0.1"
		a = self.args
		for _i in range(0, len(a)):
			i = a[_i]
			try:
				j = a[_i + 1]
			except:
				j = a[_i]
				
			if i in ['-c', '--client']:
				self.type = 'CLIENT'
			if i in ['-s', '--server']:
				self.type = 'SERVER'
			if i in ['-h', '--help']:
				self.help = True
			if i in ['-g', '--graceful']:
				self.graceful = True
			if i in ['-r', '--restart']:
				self.restart = True
			if i in ['-s', '--start']:
				self.start = True
			if i in ['-st', '--stop']:
				self.stop = True
			if i in ['init', '--init']:
				self.init = j 
			if i in ['-p', '--port']:
				self.port = j
			if i in ['-i', '--ip']:
				self.ip = j
			if i in ['-d', '--daemon']:
				self.daemon = True

			
		if 'help' in dir(self):
			self._help()
			return

		self.perform()

	def perform(self):
		if self.type == 'CLIENT':
			if 'init' in dir(self):
				print os.getcwd()
				""" initialize a new module """

				print "Starting an empty module.. "

				path_of_mod = os.getcwd()

				module_name = self.init


				""" navigate to conf, make a link """
				""" navigat to modules, make a link """

				path = os.getcwd()

				localpath = "/usr/local/oneline/"
				confpath = "/usr/local/oneline/conf/"
				modpath = "/usr/local/oneline/modules/"
				os.chdir(confpath)
				f = open(path_of_mod + "/" + module_name + ".conf", "w+")

				print "Linking " + module_name + "'s config..."

				f.write("""
Config for {0} Module
===========================================

db_type = 'mysql'
db_table = 'example'
db_user = 'root'
db_pass = '__test__'
db_database = '__example_edit_me__'
db_host = '127.0.0.1'
ol_broadcast = 'singular'
ol_memcached = 'on'

==========================================
				""".format(module_name))

				os.system('sudo ln -s {0}/{1}.conf > /dev/null 2>&1 &'.format(path_of_mod, module_name))
				f.close()

				os.chdir(modpath)
				f = open(path_of_mod + "/" + module_name + ".py", "w+")

				f.write("""

##############################################################################
# Factory created module. Edit 
# as you like 
##############################################################################

from oneline import ol

class {0}(ol.module):
    def start(self):
	self.pipeline = ol.stream()
	
    def receiver(self, message):
	self.pipeline.run(message)
""".format(module_name))
				print "Linking " + module_name + "'s module..."
				os.system('sudo ln -s {0}/{1}.py > /dev/null 2>&1 &'.format(path_of_mod, module_name))
				f.close()

				f = open(path_of_mod + "/" + module_name + ".html", "w+")
				f.write("""
<!DOCTYPE html>
<html class="no-js" lang="en-US"> <!--<![endif]-->
    <body>
      <script type='application/javascript' src='./oneline.min.js'></script>
      <script type='application/javascript'>
	  Oneline.setup({ server: '{0}', freq: 10 });
	  Oneline.pipeline(agent, [], function(res) {
	      console.log(res):
	  }).run();
    </script>
  </body>
		</html>
				""".replace("{0}", module_name))
				f.close()

				""" move a javascript client relative to this directory. """
				""" if we already have one, skip """

				if not os.path.isfile(path_of_mod + "/oneline.min.js"):
					print "copying javascript client to this directory.."
					shutil.copy(localpath + "oneline.min.js", path_of_mod + "/oneline.min.js")

				
				print "All done! you can now start writing code"
				#os.system("sudo ln -s " + 

		if self.type == 'SERVER':
			if 'start' in dir(self):
				""" start as daemon or regular? """
				ol.server(self.ip,int(self.port)).start()
			if 'stop' in dir(self):
				os.system("pkill -f 'python /usr/bin/oneline-cli.py'")
			if 'restart' in dir(self):
				""" TODO add graceful shutdown """
				print "Stopping server.."
				os.system("pkill -f 'python /usr/bin/oneline-cli.py'")

				time.sleep(1)
				ol.server().start()

				quit()
 
				exit()
			if 'graceful' in dir(self):
				print "Stopping Oneline server"
				os.system("pkill -f 'python ./ol.py --server'")
				os.system("pkill -f 'python /usr/bin/ol.py --server'")
				exit()


	def _help(self):
		print """
usage: oneline [options] required_input required_input2
options:
-c, --client     Run a command as a client
-s, --server     Initiate a server

SERVER SPECIFIC
-g, --graceful  Perform a graceful shutdown
-re, --restart  Restart the server
-st, --start    Start the server
-sp, --stop     Force a shutdown
-st, --status   Is the server running or stopped
"""

if __name__ == '__main__':
	Runtime(sys.argv)