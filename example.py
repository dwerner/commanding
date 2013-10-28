#!/usr/bin/env python
import os
from commanding.commands import *

if __name__ == "__main__":

   sysName = Run('uname -s')
   isMac = sysName.matches("Darwin")
   isLinux = sysName.matches("Linux")
   pipFound = not Exists('pip').matches("not found")

   t = Task(

      When(
         isMac and not os.path.exists("/Applications/iTerm 2.app"),
      ).do(
         Wget("http://www.iterm2.com/downloads/stable/iTerm2_v1_0_0.zip"),
         Unzip("iTerm2_v1_0_0.zip", "./tmp")
      ),

      When(
         isMac and Exists("brew").matches("not found"),
      ).do(
         Run('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
      ),

      When(
         not pipFound and isLinux,
      ).do(
         Apt("python-pip")
      ).elseWhen(
         not pipFound and isMac,
      ).do(
         Brew('pip')
      ),

      When(
         Exists("node").matches("not found"),
      ).do(
            When(
               isMac,
            ).do(
               Brew("node")
            ).elseWhen(
               isLinux,
            ).do(
               AptPPA("ppa:chris-lea/node.js"),
               AptUpdate(),
               Apt("nodejs")
         )
      ),

      When(
         Exists("zsh").matches("not found"),
      ).do(
         Run("curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh")
      )
   )
   t.run()

