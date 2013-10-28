commanding
======

A simple, and easily extensible, internal python DSL for performing command line operations.

### Example:
```python

#!/usr/bin/env python
import os
from commanding.commands import *

if __name__ == "__main__":

   sysName = Run('uname -s')
   pipFound = not Exists('pip').matches("not found")

   When(sysName.matches("Darwin")).do(

      When(
         not os.path.exists("/Applications/iTerm 2.app")
      ).do(
         Wget("http://www.iterm2.com/downloads/stable/iTerm2_v1_0_0.zip"),
         Unzip("iTerm2_v1_0_0.zip", "./tmp")
      ),

      When(
         Exists("brew").matches("not found")
      ).do(
         Run('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
      ),

      When(not pipFound).do(
         Brew('pip')
      ),

      When(
         Exists("node").matches("not found")
      ).do(
         Brew("node")
      ),

      When(
         Exists("zsh").matches("not found")
      ).do(
         Run("curl -L https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh | sh")
      )

   ).elseWhen(sysName.matches("Linux")).do(

      When(
         not pipFound
      ).do(
         Apt("python-pip")
      )

   ).run()

```
