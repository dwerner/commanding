#!/usr/bin/env python
import os
import subprocess
import pdb

def find_which_or_install(exists_cmd, not_found_command):
   exists = run("which "+exists_cmd)
   installed = False
   while exists_cmd + " not found" == exists or exists == '':

      print "Attempting to run command: " + not_found_command
      run(not_found_command)
      installed = True
      exists = run("which "+exists_cmd)

   if installed:
      print "Installed : " + exists
   else:
      print "Found preinstalled: " + exists
   #return result from last `which`
   return exists


def run(cmd_with_options):
   result = os.popen(cmd_with_options)
   return result.readline().rstrip()

def wget(link):
   subprocess.call("wget "+ link)

class InstallTarget():

   def __init__(self):
      print "Examining the system..."

      #find uname -s
      self.uname = run("uname -s")
      self.homedir = run("echo $HOME")

      os.chdir(self.homedir)
      if not os.path.exists("tmp"):
         os.mkdir("tmp")

      #determine shell
      self.shell = run("echo $SHELL")

      self.pip_cmd = "sudo pip install "


   def install(self):
      print "Found " + self.uname
      if "Darwin" in self.uname:
         self.osx_specific()

      elif "Linux" in self.uname:
         self.linux_specific()

      else:
         pass #... other (windows?)

      #platform agnostic packages
      self.pkg_install("git")
      self.pkg_install("wget")
      self.pkg_install("curl")
      self.express = find_which_or_install("express", "sudo npm install -g express")
      #self.django = find_which_or_install("django-admin.py", self.pip_cmd + "django")

      if "Darwin" in self.uname:
         if not os.path.exists("/Applications/iTerm 2.app"):
            wget("http://www.iterm2.com/downloads/stable/iTerm2_v1_0_0.zip")
            subprocess.call("unzip iTerm2_v1_0_0.zip /Applications")

      self.zsh = find_which_or_install("zsh", "curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh")

      if not os.path.exists("dotfiles"):
         print "Checking out 'dotfiles'"
         run("git clone https://github.com/olivier-o/dotfiles")
         run("sh dotfiles/makesymlinks.sh")

      print "Complete."


   def osx_specific(self):
      print "Installing OSX Specific packages..."

      #todo: detect Xcode command line tools
      self.brew = find_which_or_install("brew", 'ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
      self.install_cmd = "sudo brew install "

      self.pip = find_which_or_install("pip", "sudo easy_install pip")
      self.pkg_install("node")


   def linux_specific(self):
      print "Installing Linux Specific packages..."

      self.install_cmd = "sudo apt-get install -y "
      apt_ppa_cmd = "sudo add-apt-repository -y "

      def add_ppa(ppa):
         print "Adding PPA: " + ppa
         run(apt_ppa_cmd + ppa)

      find_which_or_install("pip", self.install_cmd+ "python-pip")

      #PPAs
      add_ppa("ppa:chris-lea/node.js") #nodejs
      run("sudo apt-get update")

      find_which_or_install("node", self.install_cmd+ "nodejs")

   def pkg_install(self, pkg):
      """
      Install a package using the system package manager (homebrew, apt-get)
      """
      find_which_or_install(pkg, self.install_cmd + pkg)


   def pip_install(self, module):
      """
      Install a python module using pip
      """
      run(self.pip_cmd + module)

if __name__ == "__main__":
   target = InstallTarget()
   target.install()
