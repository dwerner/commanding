#!/usr/bin/env python
import os
from subprocess import Popen, PIPE


class Message(object):
   def __init__(self, message):
      self.message = message

   def run(self):
      print self.message


class Command(object):

   def __init__(self, cmd):
      self.command = cmd

   def run(self):
      Message(self.command).run()
      self.process_options = {"shell":True, "stdout":PIPE, "stderr":PIPE}
      self.process = Popen([self.command], **self.process_options)
      self.stdout, self.stderr = self.process.communicate()
      self.process.wait()
      return self

   def first(self):
      return self.stdout.rstrip()

   def matches(self, match):
      return match in self.run().first()

   def isnt(self, match):
      return match in self.run().first()

   def __str__(self):
      return '"{}"'.format(self.command)


class Where(Command):
   def __init__(self, test):
      super(Where, self).__init__("which {}".format(test))

class Wget(Command):
   def __init__(self, url):
      self.command = "wget {}".format(url)

class AptPPA(Command):
   def __init__(self, ppa):
      self.command = "sudo add-apt-repository -y {}".format(ppa)

class Apt(Command):
   def __init__(self, pkg):
      self.command = "sudo apt-get install -y {}".format(pkg)

class AptUpdate(Command):
   def __init__(self):
      self.command = "sudo apt-get update"

class Pip(Command):
   def __init__(self, pkg):
      self.command = "sudo pip install {}".format(pkg)

class Unzip(Command):
   def __init__(self, archive, dest):
      self.command = "unzip {} {}".format(archive, dest)

class Brew(Command):
   def __init__(self, pkg):
      self.command = "sudo brew install {}".format(pkg)

class Task(object):
   def __init__(self, *args):
      self.tasks = args

   def run(self):
      print "Running task"
      for task in self.tasks:
         task.run()

   def __str__(self):
      return " -> ".join(["{}".format(s) for s in self.tasks])

class Do(object):
   def __init__(self, condition, command):
      self.condition = condition
      self.command = command

   def run(self):
      if self.condition:
         self.command.run()
      else:
         Message("Won't Do : {}".format(self.command)).run()

   def __str__(self):
      return "Conditional: {}".format(self.command)

if __name__ == "__main__":
   t = Task(
         Do(
            Where("uname -s").matches("Darwin"),
            Do(
               not os.path.exists("/Applications/iTerm 2.app"),
               Task(
                  Wget("http://www.iterm2.com/downloads/stable/iTerm2_v1_0_0.zip"),
                  Unzip("iTerm2_v1_0_0.zip", "./tmp")
               )
            )
         ),
         Do(
            Where("brew").matches("not found"),
            Command('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"'),
         ),
         Do(
            Where("pip").matches("not found"),
            Task(
               Do(
                  Where("uname -s").matches("Darwin"),
                  Task(
                     ("pip")
                  )
               ),
               Do(
                  Where("uname -s").matches("Linux"),
                  Apt("python-pip")
               )
            )
         ),
         Do(
            Where("node").matches("not found"),
            Task(
               Do(
                  Where("uname -s").matches("Darwin"),
                  Brew("node")
               ),
               Do(
                  Where("uname -s").matches("Linux"),
                  Task(
                     AptPPA("ppa:chris-lea/node.js"),
                     AptUpdate(),
                     Apt("nodejs")
                  )
               )
            )
         ),
         Do(
            Where("zsh").matches("not found"),
            Command("curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh")
         )
      )
   t.run()

