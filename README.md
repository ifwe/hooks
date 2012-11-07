This repository provides version controlled hooks for all Tagged git repositories.

# Installation Instructions
```
cd /path/to/repo

# Replace the .git/hooks directory with a clone of the hooks repo
cd .git
rm -rf hooks
git clone https://github.com/tagged/hooks.git

# Create a .git_hooks directory in your repo to store + version control your hooks
cd ..
mkdir .git_hooks
cd .git_hooks

# Mirror the directory structure and create your custom hooks
mkdir pre-receive
cd pre-receive
touch my-hook.sh
chmod u+x my-hook.sh
```
