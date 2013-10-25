#!/usr/bin/env python
import os
from commanding.commands import *

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

