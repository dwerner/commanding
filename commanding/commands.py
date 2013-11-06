import os
from subprocess import Popen, PIPE

class Message(object):
   def __init__(self, message):
      self.message = message

   def run(self):
      print self.message


class Run(object):

   hasRun = False

   def __init__(self, cmd, verbose=True):
      self.command = cmd
      self.verbose = verbose

   def run(self):
      if self.hasRun:
         raise Exception("Run has already run! {}".format(self))
      else:
         self.hasRun = True

      self.process_options = {"shell":True, "stdout":PIPE, "stderr":PIPE}
      self.process = Popen([self.command], **self.process_options)
      self.stdout, self.stderr = self.process.communicate()
      self.process.wait()

      if self.verbose:
         Message(self.command).run()
         Message(self.stdout).run()

      return self

   def value(self):
      if not self.hasRun:
         self.run()
      return self.stdout.rstrip()

   def matches(self, match):
      return match in self.value()

   def isnt(self, match):
      return match in self.value()

   def __str__(self):
      return '"{}"'.format(self.command)



class Exists(Run):
   def __init__(self, test):
      super(Exists, self).__init__("which {}".format(test))


class Wget(Run):
   def __init__(self, url):
      self.command = "wget {}".format(url)


class AptPPA(Run):
   def __init__(self, ppa):
      self.command = "sudo add-apt-repository -y {}".format(ppa)


class Apt(Run):
   def __init__(self, pkg):
      self.command = "sudo apt-get install -y {}".format(pkg)


class AptUpdate(Run):
   def __init__(self):
      self.command = "sudo apt-get update"


class Pip(Run):
   def __init__(self, pkg):
      self.command = "sudo pip install {}".format(pkg)

class GitHub(Run):
   def __init__(self, repo):
      self.command = "git clone https://github.com/{}".format(repo)

class Unzip(Run):
   def __init__(self, archive, dest):
      self.command = "unzip {} {}".format(archive, dest)


class Brew(Run):
   def __init__(self, pkg):
      self.command = "sudo brew install {}".format(pkg)

class When(object):

   commands = []
   else_commands = []

   def __init__(self, condition):
      self.condition = condition

   def run(self):
      if self.condition:
         for cmd in self.commands:
           cmd.run()
      else:
         Message("Not executing {}".format(self.commands))

   def do(self, *args):
      self.commands.extend(args)
      return self


   def elseWhen(self, condition):
      return When(condition)

   def __str__(self):
      return "condition:{} commands: {} else: {}".format(self.condition, self.commands, self.else_commands)

