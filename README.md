# About
This is a simple python script that creates logs to monitorize CPU usage on multicore machines. It works with the help of `top`, so of course, you will need to adapt the parser to your top output. 

You can launch the script at any moment, it will take the data from the `top` command and store it in memory. When you press `ctrl+c` the executions of the script will stop and two files will be created. One of them contain a detailed dump with the 10 programs that were using the CPU the most on the moment of the meassure, a list with all the core level of usage and a date and time string. The other one will be formated as CSV, ready to be loaded on some ploting tool to display the core usage. 

# Improvements
There are a lot of things to improve here, but this is not the first thing on my list so... Anyway, here you have the main features that should be added.

- Code again the parser part to make it modular and develop a way to easy select the parser, or even create one. 
- Replace the memory storage for the meassures. A better option will be using a db to store the information. 
- The way of finishing the script is not the best. 

# License
 Copyright (C) 2017  Iván Rodríguez Torres

> This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

> This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

> You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
