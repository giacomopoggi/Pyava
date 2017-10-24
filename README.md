# Pyava
Pyava is a simple emulator launcher written in Python. It's a portable and convenient menu to run all your games from a single place.
Its creation was inspired by [Yava](https://github.com/Beluki/Yava).

![alt text](https://raw.githubusercontent.com/giacomopoggi/Pyava/master/screenshots/screenshot.png)

## Keyboard shortcuts
| Key         | Use                                              |
| ----------- | ------------------------------------------------ |
| Esc         | Close the program.                               |
| Tab         | Change between the left and right panel.         |
| Control + A | Show an information message.                     |
| Control + R | Reload information config.ini.                   |
| Control + S | Set a custom separator for splitting parameters. |

## Configuration
Pyava is configured using a file named "config.ini". This file contains everything Pyava needs to know about the folders
and files it will launch.

Here is an example:
```ini
[Game Boy]
games = C:\Games\Game Boy\
executable = C:\Emulators\BGB\bgb.exe
extensions = .zip, .gb

[Nintendo Entertainment System]
games = C:\Games\Nintendo Entertainment System\
executable = C:\Emulators\Mesen\Mesen.exe
extensions = .7z
parameters = /fullscreen, /DoNotSaveSettings
```
Parameters and extensions are separated by ",". You can set a custom separator using the apposite keyboard shortcut, but it
resets to "," every time you select a different platform from the list.
